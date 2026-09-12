"""
Score the Experiment A benchmark and the negative sets.

Positives: one per case, the injected INGRESS entry in the target run. A case is
  recalled at threshold t if any hit with source_run == A lands on that entry
  with score >= t.
Negatives: every other (source span, target entry) pair in every case, in both
  directions. All runs are solo, so any such hit at score >= t is a false positive.
Convergence floor (Experiment A0) and unrelated-run floor: run the detector on a
  directory of solo runs with nothing injected; every hit is a false positive.

Outputs (in --out):
  pr_curve_<score>.csv     threshold, tp_hits, fp_hits, precision, recall
  cells_<score>.csv        per (type, length, transform): n, recall@t*, mean score
  headline_<score>.md      recall vs length x type, per transform, at t* where
                           precision >= --min-precision (fallback: best F1)
  negatives_<score>.csv    FP count vs threshold on the negative dirs
  raw_hits.jsonl           every hit, every case (for your own plots)

Usage:
    python score.py cases/                                   # default: containment
    python score.py cases/ --score jaccard --min-precision 0.95
    python score.py cases/ --negatives ../runs_a0 ../corpus  # add A0 + unrelated floors
"""

from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import detector as det  # noqa: E402

THRESHOLDS = [round(x, 2) for x in np.arange(0.05, 1.0001, 0.05)]


def run_case(cdir: pathlib.Path, hasher: det.MinHasher, origination: bool,
             common: set[int] | None) -> list[det.Hit]:
    runs = det.load_runs(cdir, hasher, origination, common_ref=common)
    return det.scan_all(runs, hasher)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cases", type=pathlib.Path)
    ap.add_argument("--score", choices=["containment", "coverage", "jaccard"], default="containment")
    ap.add_argument("--min-precision", type=float, default=0.95)
    ap.add_argument("--fixed", type=float, default=0.7, help="also report every table at this fixed threshold")
    ap.add_argument("--negatives", type=pathlib.Path, nargs="*", default=[],
                    help="dirs of solo runs with nothing injected (A0 convergence, unrelated)")
    ap.add_argument("--no-origination", action="store_true", help="ablation")
    ap.add_argument("--common-runs", type=int, default=det.COMMON_RUNS,
                    help="convergence filter K, estimated on the full corpus in meta.json; 0 disables")
    ap.add_argument("--min-evidence", type=int, default=det.MIN_EVIDENCE,
                    help="containment denominator floor; 0 disables (ablation)")
    ap.add_argument("--out", type=pathlib.Path)
    args = ap.parse_args()
    out = args.out or args.cases / "results"
    out.mkdir(parents=True, exist_ok=True)
    det.MIN_EVIDENCE = args.min_evidence
    sc = args.score
    hasher = det.MinHasher()

    labels = [json.loads(l) for l in (args.cases / "labels.jsonl").read_text().splitlines() if l.strip()]
    by_case = {l["case_id"]: l for l in labels}

    # convergence filter reference: estimated once on the whole solo corpus
    meta = json.loads((args.cases / "meta.json").read_text())
    corpus = pathlib.Path(meta["corpus"])
    if not corpus.exists():  # cases built before the repo was reorganised recorded runs/...
        for alt in (pathlib.Path("data") / corpus, pathlib.Path("data/runs") / corpus.name):
            if alt.exists():
                corpus = alt
                break
    common: set[int] | None = None
    if args.common_runs > 0 and corpus.exists():
        corpus_runs = {n: det.build_run(n, p, hasher, not args.no_origination)
                       for n, p in det.discover_runs(corpus).items()}
        common = det.common_shingles(corpus_runs, args.common_runs)
        print(f"convergence filter: {len(common)} shingles originated by >= {args.common_runs} "
              f"of {len(corpus_runs)} corpus runs", file=sys.stderr)
    elif args.common_runs > 0:
        print(f"corpus {corpus} not found; estimating convergence per case", file=sys.stderr)

    # ---- run every case
    pos_scores: dict[str, float] = {}       # case_id -> best score on injected entry from source
    neg_scores: list[float] = []            # every other hit
    raw = open(out / "raw_hits.jsonl", "w")
    for i, cid in enumerate(sorted(by_case)):
        lab = by_case[cid]
        hits = run_case(args.cases / cid, hasher, not args.no_origination, common)
        best = 0.0
        for h in hits:
            d = h.__dict__ | {"case_id": cid}
            is_pos = (h.source_run == lab["source_run"] and h.target_run == lab["target_run"]
                      and h.target_entry == lab["target_entry"])
            d["is_positive"] = is_pos
            raw.write(json.dumps(d, default=str) + "\n")
            if is_pos:
                best = max(best, getattr(h, sc))
            else:
                neg_scores.append(getattr(h, sc))
        pos_scores[cid] = best
        print(f"[{i + 1}/{len(by_case)}] {cid}: best={best:.2f} other_hits={len(hits)}", file=sys.stderr)
    raw.close()
    neg = np.array(neg_scores) if neg_scores else np.zeros(0)
    pos = np.array([pos_scores[c] for c in sorted(by_case)])

    # ---- PR curve
    rows = []
    for t in THRESHOLDS:
        tp = int((pos >= t).sum())
        fp = int((neg >= t).sum())
        prec = tp / (tp + fp) if tp + fp else 1.0
        rec = tp / len(pos) if len(pos) else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        rows.append({"threshold": t, "tp_cases": tp, "fp_hits": fp, "precision": round(prec, 4),
                     "recall": round(rec, 4), "f1": round(f1, 4)})
    with open(out / f"pr_curve_{sc}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

    ok = [r for r in rows if r["precision"] >= args.min_precision and r["tp_cases"] > 0]
    if ok:
        tstar = max(ok, key=lambda r: r["recall"])["threshold"]
        how = f"lowest threshold with precision >= {args.min_precision}"
    else:
        tstar = max(rows, key=lambda r: r["f1"])["threshold"]
        how = "no threshold reaches min precision; using best F1"
    ok_rows = [r for r in rows if r["threshold"] == tstar][0]

    # ---- per-cell recall at t*
    cells = defaultdict(list)
    for cid, lab in by_case.items():
        cells[(lab["artifact_type"], lab["length_tokens"], lab["transform"])].append(pos_scores[cid])
    cell_rows = []
    for (typ, L, tr), scores in sorted(cells.items()):
        cell_rows.append({"artifact_type": typ, "length_tokens": L, "transform": tr, "n": len(scores),
                          "recall_at_tstar": round(float(np.mean([s >= tstar for s in scores])), 3),
                          "mean_score": round(float(np.mean(scores)), 3),
                          "min_score": round(float(np.min(scores)), 3)})
    with open(out / f"cells_{sc}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cell_rows[0].keys()); w.writeheader(); w.writerows(cell_rows)

    # ---- negative dirs (A0 convergence, unrelated)
    neg_rows = []
    for nd in args.negatives:
        runs = det.load_runs(nd, hasher, not args.no_origination, args.common_runs)
        hits = det.scan_all(runs, hasher)
        s = np.array([getattr(h, sc) for h in hits]) if hits else np.zeros(0)
        n_pairs = sum(len(r.spans) for r in runs.values()) * sum(len(r.ingress) for r in runs.values())
        for t in THRESHOLDS:
            neg_rows.append({"dir": str(nd), "n_runs": len(runs), "threshold": t,
                             "fp_hits": int((s >= t).sum()), "candidate_pairs": n_pairs})
        # dump the top offenders for hand inspection
        top = sorted(hits, key=lambda h: -getattr(h, sc))[:40]
        (out / f"negatives_top_{nd.name}.jsonl").write_text(
            "\n".join(json.dumps(h.__dict__, default=str) for h in top))
    if neg_rows:
        with open(out / f"negatives_{sc}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=neg_rows[0].keys()); w.writeheader(); w.writerows(neg_rows)

    # ---- headline markdown
    lengths = sorted({l["length_tokens"] for l in labels})
    types = [t for t in ["prose", "code", "structured", "terse"] if any(l["artifact_type"] == t for l in labels)]
    transforms = [t for t in ["verbatim", "reformatted", "truncated", "paraphrased"] if any(l["transform"] == t for l in labels)]
    md = [f"# Experiment A headline ({sc})", "",
          f"Threshold t* = {tstar} ({how}). At t*: precision {ok_rows['precision']}, "
          f"recall {ok_rows['recall']}, {ok_rows['fp_hits']} false-positive hits across "
          f"{len(labels)} cases, {len(neg)} negative pairs scored > 0.", "",
          f"Detector: char {det.K}-grams, MinHash {det.NUM_PERM} perms, source window {det.SRC_WINDOW} chars, "
          f"origination filter {'OFF (ablation)' if args.no_origination else 'ON'}, "
          f"convergence filter K={args.common_runs}, evidence floor {args.min_evidence}.", ""]
    for tname, tval in [("t*", tstar), (f"fixed t={args.fixed}", args.fixed)]:
        for tr in transforms:
            md += [f"## {tr}: recall at {tname} by span length (tokens) x artifact type", "",
                   "| type | " + " | ".join(str(L) for L in lengths) + " |",
                   "|---|" + "---|" * len(lengths)]
            for typ in types:
                vals = []
                for L in lengths:
                    s = cells.get((typ, L, tr))
                    vals.append("n/a" if not s else f"{np.mean([x >= tval for x in s]):.2f} (n={len(s)})")
                md.append(f"| {typ} | " + " | ".join(vals) + " |")
            md.append("")
    # recall by originated fraction of the injected region (boilerplate-heavy leaks are undetectable by design)
    fr = [(l.get("originated_fraction", 1.0), pos_scores[l["case_id"]] >= tstar) for l in labels]
    md += ["## Recall at t* by originated fraction of the leaked region", "",
           "| originated fraction | n | recall |", "|---|---|---|"]
    for lo, hi in [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.01)]:
        b = [r for f, r in fr if lo <= f < hi]
        md.append(f"| {lo:.2f}-{min(hi,1.0):.2f} | {len(b)} | {np.mean(b):.2f} |" if b else f"| {lo:.2f}-{min(hi,1.0):.2f} | 0 | n/a |")
    md += ["", "## PR sweep", "", "| t | precision | recall | fp hits |", "|---|---|---|---|"]
    md += [f"| {r['threshold']} | {r['precision']} | {r['recall']} | {r['fp_hits']} |" for r in rows]
    if neg_rows:
        md += ["", "## Negative-set false positives (no injection; every hit is an FP)", "",
               "| dir | runs | t=0.5 | t=0.7 | t=0.9 |", "|---|---|---|---|---|"]
        for nd in args.negatives:
            r = {x["threshold"]: x for x in neg_rows if x["dir"] == str(nd)}
            md.append(f"| {nd} | {r[0.5]['n_runs']} | {r[0.5]['fp_hits']} | {r[0.7]['fp_hits']} | {r[0.9]['fp_hits']} |")
    (out / f"headline_{sc}.md").write_text("\n".join(md))
    print("\n".join(md))
    print(f"\nwrote results to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()

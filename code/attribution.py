"""Check that every recalled planted leak is credited to the run that wrote it.

A hit says "this text reappeared"; attribution says "and it came from run A".
The cross-organisational use of the detector depends on the second claim, so it
is measured here rather than asserted: for each case, take the highest-scoring
hit on the injected entry and compare its source run with the planted one.

    python attribution.py data/cases data/cases/results_t035/raw_hits.jsonl
    python attribution.py data/cases_sametask data/cases_sametask/results/raw_hits.jsonl
"""
import argparse, collections, json, pathlib


def load_labels(cases: pathlib.Path) -> dict[str, dict]:
    return {d["case_id"]: d for d in
            (json.loads(l) for l in open(cases / "labels.jsonl"))}


def best_hits(hits_path: pathlib.Path, labels: dict[str, dict], t: float) -> dict[str, dict]:
    """Per case, the best-scoring hit landing on the entry the leak was planted in.
    Hits elsewhere in the target run are false alarms, not attribution evidence."""
    best: dict[str, dict] = {}
    for line in open(hits_path):
        h = json.loads(line)
        lab = labels.get(h.get("case_id"))
        if lab is None or h["containment"] < t:
            continue
        if h["target_run"] != lab["target_run"] or h["target_entry"] != lab["target_entry"]:
            continue
        prev = best.get(lab["case_id"])
        if prev is None or h["containment"] > prev["containment"]:
            best[lab["case_id"]] = h
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cases", type=pathlib.Path)
    ap.add_argument("hits", type=pathlib.Path)
    ap.add_argument("--threshold", type=float, default=0.35)
    a = ap.parse_args()

    labels = load_labels(a.cases)
    best = best_hits(a.hits, labels, a.threshold)
    wrong = {cid: h for cid, h in best.items()
             if h["source_run"] != labels[cid]["source_run"]}
    # a candidate is any run that wrote part of the corpus; the target itself is not one
    candidates = len({l["source_run"] for l in labels.values()}
                     | {l["target_run"] for l in labels.values()}) - 1

    print(f"{a.cases}: {len(labels)} cases, {len(best)} recalled at t = {a.threshold}, "
          f"{len(best) - len(wrong)} attributed to the true source, {len(wrong)} wrong "
          f"(chance is 1 in {candidates})")
    for cid, h in sorted(wrong.items()):
        print(f"   {cid}: credited {h['source_run']}, planted from {labels[cid]['source_run']}"
              f" at {h['containment']:.2f}")
    by_t = collections.Counter(labels[c]["transform"] for c in wrong)
    if by_t:
        print("   by transform:", dict(by_t))
    return 1 if wrong else 0


if __name__ == "__main__":
    raise SystemExit(main())

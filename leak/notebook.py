"""
Append an observation entry for a run directory (or a score results dir) to
OBSERVATIONS.md. Call it after every condition so the notebook writes itself.

    python notebook.py runs/corpus                   # harness run dir
    python notebook.py runs/swarm_directed --threshold 0.7
    python notebook.py benchmark/cases/results       # score.py output dir
    python notebook.py runs/corpus --note "first full corpus, model gpt-4.1-mini"

What it records for a run dir:
  condition.json (agents, turns, shared, arm, tasks file, model)
  per agent: turns used, finished cleanly (final reply without tool call) or hit
             the turn cap, tool calls, chars of egress, chars of ingress
  approx token volume (chars/4) as a cost sanity check
  detector summary at --threshold: hit count, matrix, topology label, top 5 hits
What it records for a results dir: the headline markdown, verbatim.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import detector as det  # noqa: E402
import topology as topo  # noqa: E402

NOTEBOOK = pathlib.Path(__file__).resolve().parent / "OBSERVATIONS.md"


def git_rev() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, cwd=NOTEBOOK.parent).stdout.strip() or "n/a"
    except Exception:
        return "n/a"


def summarise_run_dir(root: pathlib.Path, threshold: float) -> list[str]:
    md = []
    cond = root / "condition.json"
    if cond.exists():
        c = json.loads(cond.read_text())
        md.append("Condition: " + ", ".join(f"{k}={v}" for k, v in c.items() if k != "started"))
    paths = det.discover_runs(root)
    if not paths:
        return md + ["No transcripts found."]
    md += ["", "| agent | turns | finished | tool calls | egress chars | ingress chars | timeouts |",
           "|---|---|---|---|---|---|---|"]
    tot_chars = 0
    for name, p in paths.items():
        es = det.load_transcript(p)
        turns = max((e.meta.get("turn", -1) for e in es), default=-1) + 1
        calls = sum(1 for e in es if e.meta.get("channel") == "bash_command")
        eg = sum(len(e.content) for e in es if e.kind == "EGRESS")
        ing = sum(len(e.content) for e in es if e.kind == "INGRESS")
        timeouts = sum(1 for e in es if e.kind == "INGRESS" and e.content.strip() == "[timeout]")
        last = es[-1] if es else None
        finished = bool(last and last.kind == "EGRESS" and last.meta.get("channel") == "text")
        tot_chars += eg + ing
        md.append(f"| {name} | {turns} | {'yes' if finished else 'cap/err'} | {calls} | {eg} | {ing} | {timeouts} |")
    # context is re-sent every turn, so token volume grows ~quadratically; this is the
    # per-transcript sum, i.e. a lower bound on what was billed
    md.append(f"\nTranscript volume ~{tot_chars // 4:,} tokens (lower bound on billed tokens; "
              f"context is resent each turn).")

    hasher = det.MinHasher()
    runs = det.load_runs(root, hasher)
    hits = det.scan_all(runs, hasher)
    above = [h for h in hits if h.containment >= threshold]
    mat = det.matrix(list(runs), above, "containment", 0.0)
    label = topo.classify(mat["runs"], mat["matrix"])
    md += ["", f"Detector (containment >= {threshold}): **{len(above)} hits**, topology **{label['label']}**"
           + (f", broadcasters {label['broadcasters']}" if label["broadcasters"] else "")]
    if above:
        md += ["", "| source | target | cont | cov | type | path | preview |", "|---|---|---|---|---|---|---|"]
        for h in sorted(above, key=lambda h: -h.containment)[:5]:
            prev = h.source_preview[:50].replace("|", "\\|").replace("\n", " ")
            md.append(f"| {h.source_run} | {h.target_run} | {h.containment:.2f} | {h.coverage:.2f} | "
                      f"{h.artifact_type} | {h.path or ''} | `{prev}` |")
    return md


def summarise_results_dir(root: pathlib.Path) -> list[str]:
    md = []
    for f in sorted(root.glob("headline_*.md")):
        md += [f"From `{f}`:", ""]
        md += [line for line in f.read_text().splitlines() if not line.startswith("# ")]
    return md or ["No headline_*.md in results dir."]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=pathlib.Path)
    ap.add_argument("--threshold", type=float, default=0.7)
    ap.add_argument("--note", default="", help="free text to record with the entry")
    ap.add_argument("--notebook", type=pathlib.Path, default=NOTEBOOK)
    args = ap.parse_args()

    stamp = time.strftime("%Y-%m-%d %H:%M")
    head = [f"## {stamp}  `{args.path}`  (code {git_rev()})", ""]
    if args.note:
        head += [f"Note: {args.note}", ""]
    if (args.path / "labels.jsonl").exists() or list(args.path.glob("headline_*.md")):
        body = summarise_results_dir(args.path if list(args.path.glob("headline_*.md")) else args.path / "results")
    else:
        body = summarise_run_dir(args.path, args.threshold)
    entry = "\n".join(head + body) + "\n\n"
    if not args.notebook.exists():
        args.notebook.write_text("# Observations\n\nAuto-appended by notebook.py after each condition. "
                                 "Add your own remarks under any entry.\n\n")
    with open(args.notebook, "a") as fh:
        fh.write(entry)
    print(entry)
    print(f"appended to {args.notebook}", file=sys.stderr)


if __name__ == "__main__":
    main()

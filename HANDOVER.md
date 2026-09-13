# Handover: since the 13 September status report

Reply to Hana's status report · Apart / CeSIA Incident Response Sprint, Track 1

Ten commits, `05ea88a..037d7f1`, on `claude/repo-status-review-t6kudi`. `main` is still
at `cae28a3`. Every number below re-derives offline; logs in `logs/`.

## One new result, and one correction that affects §4

**A planted benchmark cannot measure the filters** (`RESULTS.md` §9). Ran
{K = 2, 3, 5, off} × {a new target-side origination filter on, off} over both benchmarks,
the three negative sets and both live swarms.

On 685 labelled cases the convergence filter looks redundant — drop it and recall goes
0.9275 → 0.9700 at precision 1.000, attribution still perfect. On the live swarms that is
wrong: convergence off gives 10 and 17 **backward** edges, impossible under the 45 s
stagger. Only K = 2 gives none. Every planted case is two solo runs with one injected
entry, so convergent boilerplate has no third party to invent an edge between; the
benchmark cannot see the failure. §5 already said this of the origination filter — it
holds for convergence too.

**Correction:** §7 previously advised that "a harness that prefers recall should run
K = 5". That is wrong — K = 5 costs 9 and 12 backward edges, K = 3 costs 2 and 4.
Corrected in place. Worth knowing before you write §4.

§9a and §9b answer the two obvious objections: convergence does lose 17/400 real leaks,
all short and generic (every unparaphrased leak ≥ 100 tokens survives at every K); and
timestamps cannot substitute, because dropping all 10 backward edges still leaves 7
spurious ones pointing forward, each with a real `cat /shared/*` behind it.

## Attribution, now measured and audited

Not in your results table, so flagging it: **371/371** recalled leaks attributed to the
true source among 39 candidates, **269/269** among 7 agents that wrote the same files.
`code/attribution.py` computes it; `scripts/rederive.sh` now checks both on every audit
and re-plants the same-task benchmark from `data/runs/a0_long` first — note
`data/cases_sametask` ships results only, not its 285 case directories.

## Smaller changes

- `--target-origination` on `detector.py` and `score.py`: subtract from each ingress entry
  the shingles that run emitted earlier. Off by default; at K = 2 it changes nothing
  measurable anywhere, including both swarm maps. Kept as defence in depth.
- `RESULTS.md` was missing its `## 7` heading entirely — the section hung under the
  watermark one and three "§7" references pointed at nothing. Restored; sections now run
  in document order.
- `leak_explainer.html`: took the three path fixes from your `intuition.html`
  (`code/shared_usage.py`, `code/verify_edges.py`, `scripts/rederive.sh`) and normalised
  the rest of the file table the same way.
- `scripts/ablate_target_origination.sh` reproduces §9; `logs/ablate_target.log` is the run.

## Report

`report/REPORT.md` is a section-by-section outline on the official template, with your
requirements folded in: 8 pages not 4, abstract ≤ 150 words, §4 budgeted at two pages,
and Dual-Use restored as its own required section. Your split is recorded under Author
Contributions.

Dual-use carries an angle we had not considered: the §6b hash feed is itself an
exfiltration surface — anyone who can query it learns which candidate strings a lab's
runs produced. Worth settling before the repo goes public.

## Two asks

1. **The handover itself.** Your note says "the handover §8 outline holds", but that
   numbering (§1 problem, §2 approach … §8 limitations) is not the template's. I have not
   guessed which the submission uses.
2. **The prior-art assessment**, for the primary-source-per-incident-claim requirement.
   Related Work is still a TODO without it.

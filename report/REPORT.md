<!--
  Apart Research sprint report. Structure mirrors the Google Doc template so
  sections can be pasted back one at a time.

  Template rules worth keeping in view:
    - Recommended length: 4 pages excluding references and appendix.
      Rough guide: Intro + Related Work 1p, Methods + Results 2.5p,
      Discussion 0.5p.
    - Guidance text (these HTML comments) gets deleted before submission.
    - Judged on the written report; rubric:
      https://apartresearch.notion.site/sprint-evaluation-rubric
    - At least one figure strongly encouraged; number and caption everything.

  STATUS: outline. Bullets are content notes, not prose. Numbers in [brackets]
  are verified against the repo; numbers marked (pending) are still running.
-->

# Who Leaked to Whom: Recovering Cross-Run Contamination from Agent Transcripts Alone

| TODO: your name | Claude Opus 5 |
|---|---|
| Independent | Anthropic |

With **Apart Research**. Research conducted at the
[Incident Response Research Sprint](https://apartresearch.com/sprints),
11–13 September 2026.

<!-- TODO: confirm the sprint's exact title and URL. -->

## Abstract

<!--
  150-250 words. Cover: the problem, the approach, key results, main takeaway.
  Write this LAST -- it should reflect final results, not the initial plan.
-->

- Problem: eval harnesses run many agents in parallel against a shared cache,
  proxy or folder, promise per-task isolation, and offer no way to check it.
- Approach: detect leaks from the transcripts alone — no model access, no
  instrumentation, no watermark. Credit each span to its first author.
- Headline results: [371/400] planted leaks recalled at precision [1.000];
  [40/40] live swarm edges recovered with [0] backward and [0] spurious;
  [0] hits across [48] agent-runs where nothing could have leaked.
- Takeaway: attribution, not just detection — the detector names the source
  run correctly [371/371] among 39 candidates and [269/269] among 7 agents
  that wrote the same files.
- Methodological result worth its own line: the planted benchmark cannot
  measure either filter. Both look redundant on 685 labelled cases and both
  are load-bearing on the live swarms (§4.7).

## 1. Introduction

- The isolation gap: harnesses assert per-task isolation; nothing audits it.
- Why it matters now: parallel agent evaluation is standard, and a shared
  medium (cache, proxy, `/tmp`, a mounted folder) is the normal case.
- Threat model is **non-adversarial**: unintended leaks, not an agent
  deliberately laundering identifiers. State this early and plainly.
- Contribution list: (1) a transcript-only detector with two ordered filters,
  (2) a 400-case planted benchmark, (3) live swarm topology recovery,
  (4) a measured comparison against keyed watermarking.

## 2. Related Work

- Near-duplicate detection / MinHash + shingling lineage; why a document-level
  Jaccard threshold is the wrong instrument for an embedded leak (§6).
- LLM watermarking: Kirchenbauer et al. green-list scheme; what it requires
  (logit access) and why an outside evaluator can never apply it.
- Benchmark contamination literature — related but distinct: contamination is
  train/test overlap, this is run-to-run overlap at inference time.
- Provenance and first-author attribution.
<!-- TODO: real citations; the repo currently cites only KGW. -->

## 3. Methods

### 3.1 Harness and corpora

- One model instance per Docker container, `--network none`, 512 MB, 1 CPU,
  private `/work`, optional shared `/shared`.
- JSONL transcripts, every entry tagged INGRESS (prompt, tool output) or
  EGRESS (assistant text, bash command).
- Models: gpt-4.1-mini; containment arms also gpt-4.1.
- Corpora: [40] solo runs (20 short, 20 long tasks); same-task baselines at
  [8] agents; four shared-folder swarm arms.

### 3.2 The detector

- Character 5-grams after NFKC normalisation; 100-char source windows.
- **Origination filter** (source side): subtract every shingle that entered
  the run's context before the span was emitted. Causal, one accumulating set.
- **Convergence filter** (cross-run, K=2): drop shingles that K or more runs
  originated independently. Removed [17,313] shingles on the solo corpus,
  [8,126] on the same-task corpus.
- **Evidence floor**: containment = |∩| / max(|window|, 40).
- Order is load-bearing — see §4.3 and Figure 3.
- Decision score is containment, not Jaccard, because its threshold has a
  stable meaning across tool-output lengths (§4.5).

### 3.3 Experiment A — planted leaks

- [4] artifact types × [5] lengths (25–500 tokens) × [4] transformations ×
  [5] replicates = [400] cases.
- Transformations: verbatim, reformatted, truncated to 60%, paraphrased by
  the same model.
- Every run is solo, so a hit on the injected entry is correct by
  construction and any other hit is a false alarm.

### 3.4 Experiment B — live swarm

- [8] agents told to coordinate through `/shared`, started 45s apart, run
  twice on different task sets.
- Ground truth: every `cat`/`head`/`tail` of another agent's file, extracted
  by `shared_usage.py`; edges checked by `verify_edges.py`, not by eye.

### 3.5 Experiment C — the watermark alternative

- Keyed green-list watermark (KGW) on Qwen2.5-0.5B-Instruct, gamma 0.25,
  delta 2.0. Could not run on the agents — needs logits.
- Empirical null from [5,120] scores; why the textbook 1% threshold fails.

## 4. Results

<!--
  Findings with evidence. Separate observation from interpretation.
  Figures numbered with self-contained captions.
  Available figures: docs/img/{pipeline,scoreboard,topology_run1,compare}.svg
  TODO: convert to PNG for the Google Doc paste.
-->

### 4.1 Planted leaks are found

- PR table at thresholds 0.20 / 0.35 / 0.70; operating point t = 0.35 gives
  precision [1.000], recall [0.9275], [0] false-alarm pairs.
- Every leak ≥100 tokens that was not paraphrased was recalled, all 4 types.
- Table 1: recall per (type × length) for each transformation.

### 4.2 Unrelated runs are silent

- [0] hits across [48] agent-runs, two models, six shared-folder conditions.
- [0] on 40 solo runs scanned against each other; [0] on both same-task
  baselines (short and long task).
- Observation worth its own sentence: under an unsatisfiable dependency,
  gpt-4.1 probed the closed network path (pip, ping, nslookup, resolv.conf,
  apt-get) and never the open shared folder.

### 4.3 Real transmissions produce the right map

- Two staggered swarms: [40] directed edges, [38] direct, [2] two-hop,
  [0] spurious, [0] backward.
- Figure: recovered topology of run 1.
- Ablation: without origination, [4] edges appear that match no read, the
  two-hop edge is lost, and one edge inflates [5 → 14] pairs.

### 4.4 Source attribution is exact

- [371/371] recalled leaks attributed to the true source among 39 candidates.
- [269/269] among 7 near-identical candidates (same-task benchmark).
- This is what makes cross-organisational use possible: a lab can answer
  "did text from your run reach ours" from originated hash sets alone.

### 4.5 Jaccard was mis-calibrated, not wrong

- The a-priori config (Jaccard ≥ 0.7) recalls [23.5%]; calibrated to 0.15 it
  recalls [95.75%] at precision 1.0.
- Structural reason: a 100-char leak inside a 3,000-char tool output has
  Jaccard ≈ 0.03 by construction.

### 4.6 Watermarking, measured on matched artifacts

- [20–40%] detection at 50 tokens for code/JSON/shell; [70–100%] from 100.
- False alarms rise [1% → 15.6%] when one text is scanned against 32 keys.
- Hashing needs no model access and its false-alarm rate does not grow with
  the number of parallel runs.

### 4.7 A planted benchmark cannot measure the filters

<!-- Added after the main study. Full tables in RESULTS.md section 9. -->

- Setup: a 2×2 (and beyond) over {convergence K = 2, 3, 5, off} × {target-side
  origination filter on, off}, scored on both benchmarks, the three negative
  sets, and both live swarms.
- On the benchmarks the target filter dominates: false alarms to [0] in every
  K, attribution never wrong, recall up to [0.9700] with convergence off
  against [0.9275] shipped. Read alone, this says convergence is redundant.
- It is not. On the live swarms, where a backward edge is impossible by
  construction (agents start 45s apart), convergence-off gives [10] and [17]
  backward edges, K=5 gives [9] and [12], K=3 gives [2] and [4]. Only K=2
  gives [0].
- The benchmark is blind to this because every planted case is a pair of solo
  runs with one injected entry — convergent boilerplate has no third party to
  invent an edge between. §5 already says the benchmark cannot measure the
  origination filter; the same holds for convergence.
- Generalisable claim for the report: **a precision/recall benchmark built
  from planted leaks measures the score, not the filters.** Filter value has
  to be measured on live runs against a structural ground truth.
- The target filter itself: monotone, free, and at K=2 changes nothing
  measurable. Kept off by default as defence in depth.

## 5. Discussion and Limitations

- What the detector buys an evaluator: an audit that needs no cooperation
  from the model or the harness vendor.
- Why attribution matters more than detection for the cross-lab use case.

### Limitations

- Non-adversarial threat model; renamed identifiers defeat it.
- Smallest detectable unit ≈ 40 characters of originated text.
- [5] planted leaks per cell; cell values move in steps of 0.2.
- One model wrote the corpus and the paraphrases; two models used only for
  the silence claim.
- Read-back laundering: a run that reads its own file back keeps only its
  first emission as its own.
- Experiment B demonstrates topology recovery on instructed transmissions; it
  does not estimate how often agents leak unprompted.
- Experiment C ran on a different, smaller model than the agents.
- K=2 and the floor of 40 were first settings that happened to be the
  zero-false-alarm ones; sweeps show the trade but nothing was cross-validated.

### Dual-Use and Ethical Considerations

- The detector is an auditing tool, but the same machinery fingerprints an
  agent's output. Note the asymmetry: it needs transcripts the auditor
  already holds.
- No human-subject data; all text is model-generated inside containers.

### Future Work

- Whether the target-side filter carries the load in deployments too small
  for convergence to have statistical power (2-3 runs), which is untested.
- Document-frequency weighting instead of hard shingle removal.
- Adversarial arm: an agent instructed to launder what it copies.
- Cross-organisational protocol: exchange originated hash sets, not text.

## 6. Conclusion

- Cross-run leaks are detectable and attributable from transcripts alone.
- The filters are not a heuristic pile: each is a measured dial, and their
  order is load-bearing.
- And the benchmark that validates the score cannot validate the filters —
  a caution for anyone evaluating a contamination detector on planted data.
- One sentence on what an eval harness should do with this.

## Code and Data

- **Code repository**:
  <https://github.com/autumnigloo/2026-09-11-apart-sprint-incident-response>
- **Data/Datasets**: same repository — `data/runs/` every transcript reported,
  `data/cases/` the 400 labelled cases with results, `data/cases_sametask/`
  the near-identical-source benchmark, `data/results_c/` Experiment C.
- **Other artifacts**: `OBSERVATIONS.md` is the full lab notebook including
  results that did not make the report; `RESULTS.md` maps every claim to the
  file it comes from; `leak_explainer.html` is a visual walkthrough.
- **Reproduction**: `bash scripts/rederive.sh` recomputes every number offline
  from the raw transcripts; last audit log in `logs/rederive.log`.

## References

<!-- TODO. At minimum: Kirchenbauer et al. on green-list watermarking;
     Broder on shingling/MinHash; a benchmark-contamination reference. -->

## Appendix

### A.1 Full recall tables by type, length and transformation
### A.2 The K sweep and the evidence-floor ablation
### A.3 Swarm pair-count matrices, both runs
### A.4 Negative-set scans: what the surviving false alarms actually were
### A.5 Experiment C: entropy by artifact type, detection by length, key-count FPR
### A.6 Reproduction and the audit
### A.7 Task files and instruction arms

## LLM Usage Statement

<!-- TODO: state how models were used for the research itself (the agents under
     study) and for writing/analysis. -->

<!--
  Apart Research sprint report. Section structure follows the official Google Doc
  template so each section can be pasted back one at a time:
  https://docs.google.com/document/d/1PQBlhI3tM5vb51x7jBWXBQMYg6hkiU_x8RaCws4kjl4/copy

  Template rules, to delete along with all guidance before submitting:
    - Replace the italicized guidance under each heading with your content.
      The structure is strong guidance, not rigid; adapt it if the project needs to.
    - LENGTH: the sprint's own requirements (collaborator status report, 13 Sep)
      override the generic template here. Submission is a PDF, <= 8 pages excluding
      references and appendices, and the abstract is <= 150 words (the template says
      150-250 -- use 150). Section 4 is budgeted at two pages.
    - REQUIRED: a Limitations and Dual-Use appendix. This is a sprint requirement,
      not optional, and is why Dual-Use has its own heading below rather than being
      folded into the discussion.
    - The report must be the team's own writing; generated-sounding reports are not
      scored. This file is a scaffold for that writing, not a draft to submit.
    - Every incident claim needs a primary source; the prior-art assessment lists
      them. TODO: that document is not in this repository -- get it from Hana.
    - Judged on the written report. Rubric:
      https://apartresearch.notion.site/sprint-evaluation-rubric
    - Figures: number everything (Figure 1, Table 1...), captions that stand alone,
      place them near first reference, and make sure text in figures is legible.
    - Apart strongly encourages the final version be primarily written by the team.

  STATUS: outline. Bullets are content notes, not prose. Numbers in [brackets] are
  verified against the repo. Sections marked (+) are additions to the template.
-->

# Who Leaked to Whom: Recovering Cross-Run Contamination from Agent Transcripts Alone

| TODO: your name | Hana Ibrahim |
|---|---|
| TODO: affiliation | TODO: affiliation |

**With Apart Research / CeSIA.** Incident Response Sprint, Track 1,
11–13 September 2026.

<!-- TODO: confirm the public sprint URL. -->

## Abstract

<!--
  <= 150 words (sprint requirement, tighter than the template's 150-250).
  Cover: the problem, the approach, key results, the main takeaway.
  Polish it last. Owner per the agreed split: you.
-->

- Problem: eval harnesses run many agents in parallel against a shared cache,
  proxy or folder, promise per-task isolation, and give no way to audit it.
- Approach: detect leaks from transcripts alone — no model access, no
  instrumentation, no watermark — and credit each span to its first author.
- Key results: [371/400] planted leaks at precision [1.000]; [40/40] live swarm
  edges with [0] backward and [0] spurious; [0] hits across [48] agent-runs
  where nothing could have leaked; correct source named [371/371] among 39
  candidates and [269/269] among 7 agents that wrote the same files.
- Takeaway: attribution, not just detection — and the benchmark that validates
  the score cannot validate the filters that make attribution work.

## 1. Introduction

<!--
  What problem, why it matters, why it is practically valuable. Enough background
  to follow the work. Describe the threat model or failure mode.
-->

- The isolation gap: harnesses assert per-task isolation; nothing audits it.
- Why now: parallel agent evaluation is standard, and a shared medium (cache,
  proxy, `/tmp`, a mounted volume) is the normal deployment, not the exception.
- Threat model, stated plainly and early: **non-adversarial**. Unintended
  leakage between concurrent runs, not an agent deliberately laundering what it
  copies. An agent that renamed identifiers would defeat this.
- Why an outside evaluator cannot use the obvious alternative: watermarking
  needs logit access, which only the lab serving the model has.

***Our main contributions are:***

1. A transcript-only cross-run leak detector that needs no model access and no
   harness cooperation, built on two ordered filters plus an evidence floor.
2. A labelled benchmark of [400] planted leaks across [4] artifact types, [5]
   lengths and [4] transformations, plus [285] cases planted on near-identical
   sources, with first-author attribution measured rather than assumed.
3. Recovery of the true communication topology from two live agent swarms
   ([40] edges, [0] backward), verified against transcript reads by script.
4. A measured comparison against keyed watermarking on matched artifacts, and
   the result that a planted benchmark cannot measure either filter — both look
   redundant on [685] labelled cases and both are load-bearing on live runs.

## 2. Related Work

<!--
  Most similar prior work and how this differs. What gap does this address?
  When and why would someone use this over the state of the art?
  What insight does it provide that we did not have before?
-->

- Shingling and MinHash near-duplicate detection: the machinery is standard;
  the contribution is what gets *subtracted* before comparison.
- Why a document-level Jaccard threshold is the wrong instrument here: a
  100-char leak inside a 3,000-char tool output has Jaccard ≈ 0.03 by
  construction (§4.5).
- LLM watermarking (Kirchenbauer et al.): requires logit access; measured here
  as the alternative an evaluator cannot actually deploy.
- Benchmark contamination: related but distinct — train/test overlap, versus
  run-to-run overlap at inference time.
- When to use this instead: when you hold transcripts but not the model, and
  you need to name the source run, not just flag a collision.
<!-- TODO: real citations. The repo currently cites only KGW. -->

## 3. Methods

<!--
  Replicable detail. Key design choices, justified. Models, datasets, tools and
  why. Key parameters. What you tried that did not work.
-->

### 3.1 Harness and corpora

- One model instance per Docker container, `--network none`, 512 MB, 1 CPU,
  private `/work`, optional shared `/shared`.
- JSONL transcripts, every entry tagged INGRESS (prompt, tool output) or EGRESS
  (assistant text, bash command). That tagging is what makes origination
  decidable.
- Models: gpt-4.1-mini; containment arms also gpt-4.1.
- Corpora: [40] solo runs (20 short, 20 long tasks); same-task baselines at [8]
  agents each; four shared-folder swarm arms.

### 3.2 The detector

- Character 5-grams after NFKC normalisation; 100-char source windows.
- **Origination filter** (source side): subtract every shingle that entered the
  run's context before the span was emitted. Causal — it only looks backwards.
- **Convergence filter** (cross-run, K=2): drop shingles that K or more runs
  originated independently. Removed [17,313] shingles on the solo corpus,
  [8,126] on the same-task corpus.
- **Evidence floor**: containment = |∩| / max(|window|, 40), so a window reduced
  to a dozen generic shingles cannot score 1.0.
- Order is load-bearing: convergence counts originators, so a receiver's
  re-emission must already have been stripped (§4.3).
- Decision score is containment, not Jaccard, because its threshold keeps a
  stable meaning across tool-output lengths.

### 3.3 Experiments

- **A — planted leaks**: [4] types × [5] lengths (25–500 tokens) × [4]
  transformations × [5] replicates = [400]. Every run is solo, so a hit on the
  injected entry is correct by construction and any other hit is a false alarm.
- **B — live swarm**: [8] agents coordinating through `/shared`, started 45s
  apart, run twice. Ground truth is every `cat`/`head`/`tail` of another agent's
  file; edges checked by `verify_edges.py`, not by eye.
- **C — watermark alternative**: KGW green-list on Qwen2.5-0.5B-Instruct,
  gamma 0.25, delta 2.0; empirical null from [5,120] scores.

### 3.4 What did not work

<!-- The template asks for this explicitly, and it is real evidence of rigour. -->

- The a-priori configuration (MinHash Jaccard ≥ 0.7) recalls [23.5%] — wrong
  instrument, not a wrong idea (§4.5).
- A textbook MinHash implementation that was silently incorrect.
- The first corpus contained no span over 200 tokens, so the length sweep had
  no top end.
- The first version of the score had no evidence floor and rated generic text
  at 1.0.
- The first "coordinate via `/shared`" instruction was too weak for any agent
  to act on, producing an empty swarm.
- All visible in `OBSERVATIONS.md`, the dated lab notebook.

## 4. Results

<!--
  Findings with evidence; separate observation from interpretation. Argue
  robustness: enough data? significant? stable under design changes?
  Figures: docs/img/{pipeline,scoreboard,topology_run1,compare}.svg
  TODO: convert to PNG and check legibility at Doc size.
-->

### 4.1 Planted leaks are found

- t = 0.35: precision [1.000], recall [0.9275], [0] false-alarm pairs.
  Wilson 95% CI on recall [89.8–94.9].
- Every leak ≥100 tokens that was not paraphrased was recalled, all 4 types.
- **Table 1**: recall per (type × length) for each transformation.
- Robustness: [5] replicates per cell means cell values move in steps of 0.2 —
  argue from the aggregate, not the cell.

### 4.2 Unrelated runs are silent

- [0] hits across [48] agent-runs, two models, six shared-folder conditions.
- [0] on 40 solo runs scanned against each other; [0] on both same-task
  baselines.
- Observation worth its own sentence: under an unsatisfiable dependency,
  gpt-4.1 probed the closed network path (pip, ping, nslookup, resolv.conf,
  apt-get) and never the open shared folder.

### 4.3 Real transmissions produce the right map

- **Figure 1**: recovered topology, swarm run 1.
- Two staggered swarms: [40] edges, [38] direct, [2] two-hop, [0] spurious,
  [0] backward.
- Ablation: without origination, [4] edges appear that match no read, the
  two-hop edge is lost, and one edge inflates [5 → 14] pairs.

### 4.4 Source attribution is exact

- [371/371] among 39 candidates; [269/269] among 7 near-identical candidates.
- Interpretation: this is what makes cross-organisational use possible — a lab
  can answer "did text from your run reach ours" from originated hash sets
  alone, without exchanging transcripts.

### 4.5 Jaccard was mis-calibrated, not wrong

- Jaccard ≥ 0.7 recalls [23.5%]; calibrated to 0.15, [95.75%] at precision 1.0.
- Interpretation: containment buys a threshold with a stable meaning, not
  better accuracy.

### 4.6 Watermarking, measured on matched artifacts

- **Figure 2**: entropy by type, detection by length, key-count FPR.
- [20–40%] detection at 50 tokens for code/JSON/shell; [70–100%] from 100.
- False alarms [1% → 15.6%] scanning against 32 keys; hashing has no per-run
  key, so its false-alarm rate does not grow with the number of runs.

### 4.7 A planted benchmark cannot measure the filters

- Design: {convergence K = 2, 3, 5, off} × {target-side origination filter on,
  off}, scored on both benchmarks, three negative sets, and both live swarms.
- **Table 2** (benchmarks): the target filter dominates — false alarms to [0]
  at every K, attribution never wrong, recall up to [0.9700] with convergence
  off against [0.9275] shipped. Read alone, this says convergence is redundant.
- **Table 3** (live swarms): it is not. A backward edge is impossible by
  construction (45s stagger), and convergence-off gives [10] and [17] backward
  edges, K=5 gives [9] and [12], K=3 gives [2] and [4]. Only K=2 gives [0].
- Mechanism: every planted case is a pair of solo runs with one injected entry,
  so convergent boilerplate has no third party to invent an edge between.
- Generalisable claim: **a precision/recall benchmark built from planted leaks
  measures the score, not the filters.** Filter value has to be measured on live
  runs against a structural ground truth.
- This also corrects our own earlier advice that a recall-hungry harness should
  run K=5.
- The filter's cost is real and shaped: it loses [17/400] planted leaks, all
  short and generic, because it deletes only text two runs originated with no
  contact — which cannot be evidence of contact. Every non-paraphrased leak
  ≥100 tokens survives at every K (§9a).
- Anticipated objection: could timestamps kill backward edges instead? They
  can, and it hides the problem. Dropping all [10] backward edges leaves [25]
  against a ground truth of [18] — [7] spurious edges all pointing forward,
  each with a real `cat /shared/*` behind it. The backward edges are the
  instrument, not the failure (§9b).

## 5. Discussion and Limitations

<!-- Broader implications for AI safety. What do the results mean? -->

- What an evaluator gains: an isolation audit that needs no cooperation from the
  model provider or the harness vendor — only the transcripts they already hold.
- Attribution matters more than detection for the cross-lab case, and it is the
  part that prior tooling does not provide.
- Safety framing: isolation failures silently corrupt eval results that feed
  deployment decisions. A cheap audit is worth more than a perfect one nobody
  can run.
- Dual use has its own required appendix section below; keep the discussion here
  to the safety implications of the detection result itself.

### Limitations

<!--
  Template asks explicitly: state the assumptions, and how interpretation would
  change if each did not hold.
-->

- **Assumption: non-adversarial agents.** If false, the method degrades sharply —
  renamed identifiers defeat it. Nothing here is a claim about adversarial
  contamination.
- **Assumption: INGRESS/EGRESS tagging is available and correct.** If a harness
  cannot distinguish what a run read from what it wrote, the origination filter
  is unavailable and, per §4.3, the map is wrong without it.
- **Assumption: enough concurrent runs to estimate convergence from.** K=2 is
  estimated from the corpus; with 2–3 runs there is almost no statistical power.
  Untested.
- Smallest detectable unit ≈ 40 characters of originated text.
- [5] planted leaks per cell; K=2 and the floor of 40 were first settings that
  happened to be zero-false-alarm, and nothing was cross-validated.
- One model wrote the corpus and the paraphrases; two models used only for the
  silence claim.
- Read-back laundering: a run that reads its own file back keeps only its first
  emission as its own.
- Experiment B demonstrates topology recovery on *instructed* transmissions; it
  does not estimate how often agents leak unprompted.
- Experiment C ran on a different, smaller model than the agents, on prompted
  artifacts rather than harness transcripts, with one scheme at one setting.

### Dual-Use

<!--
  REQUIRED by the sprint, paired with Limitations. Owner per the agreed split: you.
  Two angles named in the 13 Sep status report:
-->

- The detector as a **finder of other runs' output**: the same machinery that audits
  isolation also locates what a concurrent agent produced.
- A hash feed as an **exfiltration surface**: §6b proposes labs exchange originated
  hash sets instead of transcripts. That feed is itself a channel — an adversary who
  can query it learns which of their candidate strings a lab's runs produced.
  Mitigations to discuss: batching, thresholds on query volume, salting per pair.
- The asymmetry that limits misuse: it needs transcripts the auditor already holds.

### Future Work

- Whether the target-side filter carries the load where convergence has no
  statistical power (2–3 runs).
- Document-frequency weighting instead of hard shingle removal.
- An adversarial arm: an agent instructed to launder what it copies.
- A cross-organisational protocol exchanging originated hash sets, not text.
- Measuring unprompted leak rates, which Experiment B deliberately does not.

## 6. Conclusion

<!-- 1-2 paragraphs. -->

- Cross-run leaks are detectable *and attributable* from transcripts alone, at
  precision [1.000] on [400] planted cases and [40/40] edges on live swarms.
- The filters are not a heuristic pile: each is a measured dial and their order
  is load-bearing — and the benchmark that validates the score cannot validate
  them, which is a caution for anyone evaluating a contamination detector on
  planted data.

## Code and Data

- **Code repository**:
  <https://github.com/autumnigloo/2026-09-11-apart-sprint-incident-response>
- **Data/Datasets**: same repository — `data/runs/` every transcript reported,
  `data/cases/` the 400 labelled cases with results, `data/cases_sametask/` the
  near-identical-source benchmark, `data/results_c/` Experiment C.
- **Other artifacts**: `leak_explainer.html` is a visual walkthrough;
  `OBSERVATIONS.md` the full lab notebook including results that did not make
  the report; `RESULTS.md` maps every claim to the file it comes from.
- **Reproduction**: `bash scripts/rederive.sh` recomputes every number offline
  from the raw transcripts (log: `logs/rederive.log`);
  `bash scripts/ablate_target_origination.sh` reproduces §4.7.

## Author Contributions

<!--
  Agreed split, 13 Sep status report. Reconcile against the final section numbering
  before submitting — the split below uses the handover's outline, not this file's.
    You:  §1 problem, §2 approach, §6 cross-organisational attribution,
          §7 follow-up, abstract, dual-use half of the appendix.
    Hana: §3 method, §4 results, §5 watermarking, limitations half.
-->

## References

<!-- TODO. At minimum: Kirchenbauer et al. (green-list watermarking); Broder
     (shingling/MinHash); a benchmark-contamination reference. -->

## Appendix

### A.1 Full recall tables by type, length and transformation
### A.2 The K sweep and the evidence-floor ablation
### A.3 Swarm pair-count matrices, both runs
### A.4 Negative-set scans: what the surviving false alarms actually were
### A.5 Experiment C: entropy by type, detection by length, key-count FPR
### A.6 The target-filter grid in full (RESULTS.md §9, Tables 7–9)
### A.7 Task files and instruction arms

## LLM Usage Statement

<!--
  Template: note how LLM assistance was used, and confirm claims were verified.
  Apart strongly encourages the final submission be primarily team-written.
-->

- Distinguish two uses: models as the *object of study* (the agents in the
  containers, gpt-4.1-mini and gpt-4.1; Qwen2.5-0.5B for Experiment C), and
  model assistance in building and writing.
- State that every number is re-derived offline by `scripts/rederive.sh` from
  raw transcripts, and that the audit log is in the repository.

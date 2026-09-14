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

  VERIFICATION STATUS: entries marked [fetched] were read directly; the rest come
  from search summaries and must be checked against the primary source before
  submission — the sprint requires a primary source for every incident claim, and
  the prior-art assessment (ask Hana) may already list several of these.
-->

**Shared-environment eval failures — the motivating incidents.** The field has
documented that agents exploit state in the environment the evaluator also uses:
OpenAI retired SWE-bench Verified as a frontier measure; SWE-bench issue #465
("Repo State Loopholes During Agentic Evaluation") and SWE-bench-Pro issue #7
("Repo state leakage") record agents recovering intended fixes through ordinary
`git log --all` / `git show <future-sha>`, because post-`base_commit` objects stay
reachable in the public images. Berkeley RDI make the general form of it: in
SWE-bench, Terminal-Bench and OSWorld the agent's code runs in the environment the
evaluator inspects, so any evaluation reading state from a shared environment can be
defeated by an agent writing to it.
*Gap:* every one of these is **environment → agent** leakage within a single run.
The same shared environments host many concurrent runs, and **run → agent** leakage
is the unmeasured sibling. That is what this work measures.

**Near-duplicate detection, and why containment.** Broder et al. (1997), *Syntactic
Clustering of the Web*, introduces shingling and defines both statistics we use:
resemblance, |S(A) ∩ S(B)| / |S(A) ∪ S(B)| — Jaccard — and containment,
|S(A) ∩ S(B)| / |S(A)|.
*Gap:* none, and we should say so. Our §4.5 argument for containment over Jaccard is
Broder's own distinction, not a new one; the contribution is the calibration showing
what the wrong choice costs on embedded leaks (23.5% recall at the a-priori 0.7).

**Benchmark and data contamination.** A large literature detects train/test overlap:
the static-to-dynamic survey (arXiv 2502.17521), canary strings as used by BIG-bench,
and membership-style detectors such as Min-K% and Min-K%++.
*Gap:* two. That work concerns **training-time** overlap, not run-to-run overlap at
inference. And canaries, like watermarks, must be planted in advance by whoever owns
the data — an outside evaluator holding only transcripts can plant nothing.
*Honest borrowing:* this literature also reports that n-gram-overlap detectors lose
reliability when contamination is rephrased, which matches our paraphrase results
(§4.1) and should be cited as corroboration rather than discovered independently.

**Watermarking.** Kirchenbauer et al. (2023), *A Watermark for Large Language Models*
— the green/red-list scheme with γ and δ that Experiment C implements, offering
detection "without any knowledge of the model parameters" and interpretable p-values.
Fu & Russell (2025), *Multi-use LLM Watermarking and the False Detection Problem*
[fetched], identify exactly the failure our §4.6 measures: as user capacity grows,
unwatermarked text is increasingly likely to be falsely detected, because one
embedding serves both detection and identification. They propose Dual Watermarking.
*Position:* our 1% → 15.6% across 32 keys is an independent empirical confirmation of
their problem on agent-style artifacts, and we should cite them rather than present it
as novel. Our distinct contribution is the **entropy** half — that JSON and code leave
a watermark almost no room (66% of structured tokens near-forced) — and the empirical
null showing the textbook z = 2.33 gives 5.3% false alarms on repetitive text.
*Gap:* watermarking needs logit access, so an outside evaluator can never apply it.

**Provenance in multi-agent memory.** Margalit et al. (2026), *Governed Shared Memory
for Multi-Agent LLM Systems* [fetched], is the nearest neighbour: it names
"unauthorized leakage" and "provenance collapse" as failure modes and reconstructs
100% of depth-four derivation chains with correct writer identity. MemLineage
(arXiv 2605.14421) is adjacent, enforcing lineage over agent memory.
*Gap, and the sharpest contrast in this section:* these are **runtime governance
architectures**. They require scoped retrieval and provenance-tracking primitives
built into the memory service, and Margalit et al. state plainly that uninstrumented
systems cannot retroactively capture this — the mechanisms must exist at the memory
layer. This work is the post-hoc case: provenance recovered from transcripts of a
harness with no such instrumentation, 38 of 40 edges direct and 2 two-hop, verified
against reads.
*Be honest about the asymmetry:* they recover depth-four chains with instrumentation;
we recover depth-two without it, on text artifacts, non-adversarially.

**When to use this over the alternatives.** When you hold transcripts but not the
model, nothing was planted in advance, the harness was never instrumented, and you
need the source run *named* rather than a collision *flagged*.

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
  Measured, not speculative: code/hash_recovery.py reproduces the numbers below.
-->

The research is defensive and the method needs transcripts the auditor already holds.
The risks are in *deploying* it, and the sharpest one is in our own §6b proposal.

**The hash exchange is not a redaction.** §6b suggests labs answer "did text from your
run reach ours" by exchanging originated shingle hashes rather than transcripts. But the
shingles are character 5-grams overlapping by four characters, so the set is a de Bruijn
graph and the text is a walk through it — and they are hashed with unsalted 32-bit
FNV-1a, which is not a one-way function at this scale. A 90-line greedy assembler
(`code/hash_recovery.py`), given only the 2,651 hashes one run would have sent, returns
626 characters of readable content in 7 seconds: class and method names, docstring
topics, string literals, and a data table recovered close to intact. Exact
reconstruction is limited — the longest verbatim stretch is 24 characters, because a
*set* loses repetition counts and the assembly splices at repeated 4-grams — but
**content disclosure is close to total even when verbatim recovery is not.** On the
unfiltered shingles of the same file the longest verbatim stretch is 54 characters,
longer than the 40 the detector itself calls the smallest meaningful leak.

There is an irony to state plainly: the two filters keep precisely the text that
distinguishes one author from another, which is the same text that identifies the
content. Filtering makes the payload *more* sensitive per byte, not less.

**An endpoint is worse than a one-shot exchange.** A queryable "did you produce this?"
service is a membership oracle. Because 5-grams overlap, an adversary extends a known
fragment one character at a time at roughly 96 queries per character — linear in the
length of the text they are trying to extract, not exponential. It also answers, for
any candidate string, whether a lab's runs ever produced it.

**Mitigations to specify before anyone builds this.** Private set intersection is the
correct primitive: it reveals the intersection and nothing else. Short of that: pairwise
HMAC-keyed shingles so sets are neither reusable across partners nor attackable with
precomputed tables; a one-shot, non-adaptive exchange with both sides committing before
either sees a result; return a score above a threshold, never which shingles matched;
rate-limit and log every query. Longer shingles raise the assembly bar but do not close
the oracle.

**Retaining the transcripts is itself the risk.** The method needs full INGRESS/EGRESS
logs — everything every agent read and wrote. An isolation audit therefore centralises
exactly the data that isolation was protecting, creating a breach target and a retention
obligation where neither existed. Hash at source, scope to the sandbox, short TTL.

**Attribution is an accusation, and we have measured how wrong it can be.** The tool
names a source run. Under a plausible misconfiguration it does so confidently and
wrongly: §9 shows K = 5 producing 9 and 12 physically impossible backward edges, and
convergence off producing 10 and 17. Anyone shipping this should ship the backward-edge
check as a self-test and treat a backward edge as a configuration alarm, never publish
an edge without the read-level verification `verify_edges.py` performs.

**Lesser angles.** The same machinery lets an agent inside a shared medium locate other
runs' output rather than audit it. And publishing the filter design tells an adversarial
agent what to perturb — though §7 already concedes that a rename defeats the method, and
the threat model is non-adversarial throughout.

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

<!--
  Template: consistent format, with Author(s), Year, Title, Venue/Publisher, and a
  URL or DOI. Bibliographic details below were checked against PMLR, arXiv, DBLP and
  the ACM/IEEE records — except where marked "verify". The "cite at" notes are for
  drafting; delete them before submitting.
-->

1. Broder, A. Z. (1997). On the Resemblance and Containment of Documents.
   *Compression and Complexity of SEQUENCES 1997*, Positano, Italy, 11–13 June 1997,
   pp. 21–29. IEEE. DOI: [10.1109/SEQUEN.1997.666900](https://doi.org/10.1109/SEQUEN.1997.666900)
   <!-- cite at §4.5. Defines resemblance |S(A)∩S(B)|/|S(A)∪S(B)| and containment
        |S(A)∩S(B)|/|S(A)| as distinct statistics. Our containment-over-Jaccard
        argument is this distinction; we contribute the calibration, not the idea. -->

2. Broder, A. Z., Glassman, S. C., Manasse, M. S., & Zweig, G. (1997). Syntactic
   Clustering of the Web. *Computer Networks and ISDN Systems*, 29(8–13), 1157–1166.
   (Proc. WWW6.)
   <https://www.microsoft.com/en-us/research/wp-content/uploads/1997/01/src-tn-1997-015.pdf>
   <!-- cite at §3.2 for shingling and the canonicalisation step. -->

3. Broder, A. Z., Charikar, M., Frieze, A. M., & Mitzenmacher, M. (2000). Min-Wise
   Independent Permutations. *Journal of Computer and System Sciences*, 60(3), 630–659.
   Extended abstract: *STOC '98*, pp. 327–336.
   DOI: [10.1145/276698.276781](https://doi.org/10.1145/276698.276781)
   <!-- cite at §3.2 for the 128-permutation MinHash sketch, and where detector.py
        explains why a linear (ax+b) family degenerates on 32-bit shingle hashes. -->

4. Broder, A. Z. (2000). Identifying and Filtering Near-Duplicate Documents.
   *Combinatorial Pattern Matching (CPM 2000)*, LNCS 1848, pp. 1–10. Springer.
   <!-- optional, engineering follow-up. Page range: verify before use. Drop if tight. -->

5. Kirchenbauer, J., Geiping, J., Wen, Y., Katz, J., Miers, I., & Goldstein, T. (2023).
   A Watermark for Large Language Models. *Proceedings of the 40th International
   Conference on Machine Learning (ICML)*, PMLR 202, pp. 17061–17084.
   arXiv:[2301.10226](https://arxiv.org/abs/2301.10226) ·
   <https://proceedings.mlr.press/v202/kirchenbauer23a.html>
   <!-- cite at §3.5 and §4.6. The exact scheme Experiment C implements: green list
        partitioned per previous token, γ = 0.25, δ = 2.0, z-score detection. -->

6. Kirchenbauer, J., Geiping, J., Wen, Y., Shu, M., Saifullah, K., Kong, K.,
   Fernando, K., Saha, A., Goldblum, M., & Goldstein, T. (2024). On the Reliability
   of Watermarks for Large Language Models. *ICLR 2024*.
   arXiv:[2306.04634](https://arxiv.org/abs/2306.04634)
   <!-- cite at §4.1 as well as §4.6, and this is the one to not miss. It finds that
        "paraphrases are statistically likely to leak n-grams or even longer fragments
        of the original text, resulting in high-confidence detections when enough
        tokens are observed" — the same mechanism we report from the other direction
        in §4.1, where paraphrased leaks of 200+ tokens are always recalled because
        identifiers, keys, paths and numbers survive a rewrite. Independent
        corroboration by a different method; cite rather than claim it fresh. -->

7. Fu, Z., & Russell, C. (2025). Multi-use LLM Watermarking and the False Detection
   Problem. arXiv:[2506.15975](https://arxiv.org/abs/2506.15975)
   <!-- cite at §4.6: our 1% → 15.6% across 32 keys confirms their problem. -->

8. Margalit, Y., et al. (2026). Governed Shared Memory for Multi-Agent LLM Systems.
   arXiv:[2606.24535](https://arxiv.org/abs/2606.24535)
   <!-- cite at §2 and §5: nearest neighbour, and the claim we are a counterexample
        to. Full author list: verify. -->

<!--
  Still to add, from the §2 buckets: the data-contamination survey (arXiv 2502.17521),
  a BIG-bench canary reference, Min-K%/Min-K%++, MemLineage (arXiv 2605.14421), and
  the incident primary sources (OpenAI on SWE-bench Verified; SWE-bench issue #465;
  SWE-bench-Pro issue #7; Berkeley RDI). Check Hana's prior-art assessment first —
  it may already carry these in a fixed format.
-->

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

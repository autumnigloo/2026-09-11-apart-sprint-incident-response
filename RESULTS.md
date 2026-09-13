# Results: claims and evidence

Every number below is traceable to a file in this repository, named next to it. All of
them were re-derived from the raw transcripts with the final code (`scripts/rederive.sh`).

## Summary

| claim | evidence | where |
|---|---|---|
| Planted leaks are found | 371 / 400 recalled at t = 0.35 (92.8%, Wilson 95% CI 89.8 to 95.0) with 0 false-alarm pairs | `data/cases/results_t035/` |
| Unrelated runs are silent | 0 hits at 0.35 on 48 agent-runs across two models and six shared-folder conditions; 0 on 40 solo runs scanned against each other; 0 on 8 same-task runs (short task) and 0 on 8 same-task runs (long task) | `data/runs/swarm_*`, `data/runs/corpus_all`, `data/runs/a0`, `data/runs/a0_long`, `OBSERVATIONS.md` |
| Real transmissions produce the right map | Two staggered swarm runs: 40 directed edges, 38 matching a transcript read, 2 two-hop, 0 spurious, 0 backward, checked by script | `data/runs/swarm_directed_explicit*/hits.json`, `code/verify_edges.py` |
| First-author attribution needs the origination filter | Without it: 4 spurious edges, 1 lost edge, 1 inflated edge on the same run | `data/runs/swarm_directed_explicit/hits_no_origination.json` |
| The a-priori Jaccard threshold was wrong, not Jaccard itself | Jaccard ≥ 0.7, the configuration first proposed, recalls 23.5%; calibrated to 0.15 it recalls 95.75% at precision 1.0, slightly above containment at 0.35 | `data/cases/results_jaccard/` |
| Source attribution is exact | For all 371 recalled planted leaks, the highest-scoring source run was the true source, out of 39 candidates (0 misattributions) | `data/cases/results_t035/raw_hits.jsonl`, §6c |
| Watermarking, measured on matched artifacts (Experiment C) | On a local 0.5B model with full logit access: 20 to 40% detection at 50 tokens for code, JSON and shell; 70 to 100% from 100 tokens; false alarms rise from 1% to 15.6% when one text is scanned against 32 run-keys; JSON tokens are near-forced 66% of the time | `data/results_c/summary.md` |
| Where it fails, and the two dials | 21 of 29 misses are 25-token leaks; 6 are paraphrases. The convergence rule K and the evidence floor are each a measured precision/recall trade: K=5 recovers all short prose at 4 false-alarm pairs; the floor removes 13 false-alarm pairs at a cost of 8 leaks | Table 1, §7 |

## 1 What was measured

| item | value |
|---|---|
| agent model | gpt-4.1-mini (containment arms also gpt-4.1) |
| container | Docker, `--network none`, 512 MB, 1 CPU, private `/work`, optional shared `/shared` |
| transcript | JSONL, every entry INGRESS (prompt, tool output) or EGRESS (assistant text, bash command) |
| span types | prose (`.md`, `.txt`), code (source files), structured (`.json`, `.yaml`, `.ini`), terse (command line with heredoc bodies removed) |
| shingles | character 5-grams after NFKC, control-character removal, whitespace collapse; case kept |
| origination filter | per run, in time order, subtract every shingle that entered the context before the span was emitted |
| convergence filter | remove shingles originated by K = 2 or more of the 40 solo runs (17,313 removed) |
| unit | 100-character windows of each attributable span |
| score | containment = shared shingles / max(window shingles, 40); the 40 is the evidence floor |
| comparison score | MinHash Jaccard, 128 permutations, against 200-char target windows; reported, not used |
| operating point | t = 0.35 |
| solo corpus | 40 runs: 20 short tasks, 20 long tasks (150-line module, 400-word README, 40-key config); 1 short run empty after a malformed tool call |
| planted cases | 4 types × 5 lengths (25, 50, 100, 200, 500 BPE tokens) × 4 transformations × 5 replicates = 400 |
| transformations | verbatim; reformatted (indent, quotes, line endings, trailing space); truncated to 60%; paraphrased by gpt-4.1-mini |
| cost | cents per 20-agent gpt-4.1-mini run; whole study on the order of ten euros of API use, mostly the gpt-4.1 runs; Experiment C ran locally |

## 2 Claim: planted leaks are found

A case takes an attributable span from solo run A, cuts an L-token region, transforms it,
and inserts it into a copy of solo run B as the output of `cat /shared/...`. Because
every run is solo, a hit on the injected entry is correct and any other hit is a false
alarm. Precision is recalled cases / (recalled cases + false-alarm pairs), where a pair is
one (source window, target entry); 1,967 negative pairs scored above zero, and
zero-scoring pairs are not counted.

Precision and recall against threshold (`results_t035/pr_curve_containment.csv`):

| t | precision | recall | false-alarm pairs |
|---|---|---|---|
| 0.10 | 0.790 | 0.998 | 106 |
| 0.20 | 0.985 | 0.988 | 6 |
| 0.30 | 0.995 | 0.945 | 2 |
| 0.35 | 1.000 | 0.928 | 0 |
| 0.50 | 1.000 | 0.835 | 0 |
| 0.70 | 1.000 | 0.710 | 0 |
| 0.90 | 1.000 | 0.505 | 0 |
| 1.00 | 1.000 | 0.408 | 0 |

Rule-of-three bound on the false-alarm rate at 0.35 with the 1,967 non-zero pairs as
denominator: 0.15%. The full pair count is much larger, so this is conservative.

Table 1. Recall at t = 0.35, five planted leaks per cell.

| verbatim | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.40 | 1.00 | 1.00 | 1.00 | 1.00 |
| code | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 |
| structured | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| terse | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

| reformatted | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.60 | 0.80 | 1.00 | 1.00 | 1.00 |
| code | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 |
| structured | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| terse | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

| truncated | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.40 | 0.80 | 1.00 | 1.00 | 1.00 |
| code | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 |
| structured | 0.60 | 1.00 | 1.00 | 1.00 | 1.00 |
| terse | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 |

| paraphrased | 25 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|
| prose | 0.60 | 0.60 | 0.60 | 1.00 | 1.00 |
| code | 0.60 | 0.80 | 0.80 | 1.00 | 1.00 |
| structured | 0.60 | 1.00 | 1.00 | 1.00 | 1.00 |
| terse | 0.80 | 1.00 | 1.00 | 1.00 | 1.00 |

Every leak of 100 tokens or more that was not paraphrased was recalled, for all four
types. Recall did not depend on how much of the leaked region was attributable after
filtering: 0.97 for regions under a quarter attributable, 0.99 between a quarter and
three-quarters, 1.00 above (at t = 0.2, `results_t035/headline_containment.md`).

## 3 Claim: unrelated runs are silent

Three kinds of negative evidence, none of which contains a leak by construction.

Same-task baseline (A0). Eight agents, identical task, no shared folder: the strongest
convergence pressure available. Short task: zero hits at t = 0.35, 0.5, 0.7 and 0.9
(`results_t035/negatives_containment.csv`). Long task, where each agent writes the same
150-line module, README and config: zero hits at 0.35 (`data/runs/a0_long`).

Solo corpus against itself. The 40 solo runs, 39 × 40 ordered pairs: zero hits at
t = 0.5 and above.

Shared-folder runs with no instruction to leak. Eight agents per run, a shared `/shared`
volume they could use:

| model | tasks | instruction about other agents | commands touching `/shared` | hits at 0.35 |
|---|---|---|---|---|
| gpt-4.1-mini | short, 2 impossible | none | 0 | 0 |
| gpt-4.1-mini | short, 2 impossible | told not to interact | 0 | 0 |
| gpt-4.1-mini | short, 2 impossible | one sentence inviting coordination | 0 | 0 |
| gpt-4.1 | long | none | 0 | 0 |
| gpt-4.1 | long | told not to interact | 0 | 0 |
| gpt-4.1 | short, 2 impossible | none | 0 | 0 |

48 agent-runs, two models, six conditions, no unprompted use of the shared medium, no
hit. The two gpt-4.1 agents on impossible tasks spent 9 and 11 turns probing the network
(pip with an alternate index, ping, nslookup, /etc/resolv.conf, apt-get) and never
listed the filesystem: under pressure they went for the closed network path, not the open
shared folder. This is a narrow negative (two models, coding tasks, an unsatisfiable
dependency as the only pressure) but it is the deployment condition an eval harness sees
most of the time, and the detector produced no false alarm in it.

## 4 Claim: real transmissions produce the right map

A fourth shared-folder run put a coordination protocol in the task text (read `/shared`
first, copy finished files there, leave a notes file), used the long tasks, and started
agents 45 seconds apart so later agents find earlier agents' files. All eight followed
it; 87 commands touched `/shared`. Ground truth: every `cat`, `head` or `tail` of another
agent's file in the transcripts (`code/shared_usage.py`).

At t = 0.35 the detector reports 125 (window, entry) pairs above threshold that form
18 directed edges. The 125 is a pair count and not a leak count; the 18 edges are the
claim.

Table 2. Pair counts, rows = source, columns = target.

| | a0 | a1 | a2 | a3 | a4 | a5 | a6 | a7 |
|---|---|---|---|---|---|---|---|---|
| a0 | . | 9 | 5 | 17 | 8 | 13 | 13 | 16 |
| a1 | 0 | . | 5 | 4 | 0 | 0 | 1 | 5 |
| a2 | 0 | 0 | . | 7 | 0 | 0 | 0 | 4 |
| a3 | 0 | 0 | 0 | . | 0 | 7 | 2 | 1 |
| a4 | 0 | 0 | 0 | 0 | . | 7 | 0 | 1 |
| a5 | 0 | 0 | 0 | 0 | 0 | . | 0 | 0 |
| a6 | 0 | 0 | 0 | 0 | 0 | 0 | . | 0 |
| a7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | . |

Every edge is checked against the transcripts by `code/verify_edges.py`, which reads the
target commands behind each edge's hits and labels the edge direct (the target read a
file named after the source), two-hop (the target read only other agents' files), or
unknown. Every edge points from an earlier start to a later start, as the stagger
dictates; no backward edge, no bidirectional pair, no unknown. Seventeen edges are
direct. The eighteenth, a0 to a2, is a two-hop transmission: a2 read only a1's files, but
a1's README reused text from a0's README, config and notes, and the detector credits
that text to its first author. Those pairs score 0.35 to 0.61 against 1.0 for direct
edges, consistent with partial reuse. No read in the transcripts lacks an edge. The
topology classifier labels the run `shared_medium` with a0, a1 and a3 as broadcasters
(fan-out ≥ 3). Figure: `data/runs/swarm_directed_explicit/topology.svg`.

A second run with the same protocol on eight different long tasks (98 commands touched
`/shared`) gives 22 edges: 21 direct, 1 two-hop (a2 to a5 via a4, max score 0.35), 0
backward, 0 unknown, label `shared_medium`. Across both runs: 40 edges, 38 direct, 2
two-hop, 0 spurious, 0 backward. Every number in this section was re-derived from the
raw transcripts with the final code (`scripts/rederive.sh`, log in `logs/rederive.log`).

Table 2b. Second run, pair counts at t = 0.35.

| | a0 | a1 | a2 | a3 | a4 | a5 | a6 | a7 |
|---|---|---|---|---|---|---|---|---|
| a0 | . | 8 | 11 | 12 | 11 | 8 | 11 | 7 |
| a1 | 0 | . | 5 | 6 | 5 | 4 | 4 | 6 |
| a2 | 0 | 0 | . | 6 | 5 | 1 | 4 | 0 |
| a3 | 0 | 0 | 0 | . | 10 | 3 | 4 | 0 |
| a4 | 0 | 0 | 0 | 0 | . | 7 | 5 | 0 |
| a5 | 0 | 0 | 0 | 0 | 0 | . | 0 | 0 |
| a6 | 0 | 0 | 0 | 0 | 0 | 0 | . | 0 |
| a7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | . |

## 5 Claim: first-author attribution needs the origination filter

Same run, origination filter off (Table 3). Four edges appear that correspond to no
read: a1 to a4, a1 to a5, a5 to a6, a5 to a7. Agents 1 and 5 had reused text they read
from others; without the filter that text counts as theirs, and every later reader of the
originals looks like a reader of theirs. The a0 to a2 edge disappears and a1 to a2 grows
from 5 to 14: the two-hop leak is credited to the intermediary. The disappearance has a
mechanism: without origination, a1's re-emitted text looks originated by two runs, so the
convergence filter deletes it as skeleton. The filters only work in that order.

Table 3. Same run, origination filter off.

| | a0 | a1 | a2 | a3 | a4 | a5 | a6 | a7 |
|---|---|---|---|---|---|---|---|---|
| a0 | . | 9 | 0 | 9 | 9 | 6 | 13 | 9 |
| a1 | 0 | . | 14 | 13 | 2 | 1 | 2 | 12 |
| a2 | 0 | 0 | . | 8 | 0 | 0 | 0 | 4 |
| a3 | 0 | 0 | 0 | . | 0 | 9 | 2 | 5 |
| a4 | 0 | 0 | 0 | 0 | . | 9 | 0 | 5 |
| a5 | 0 | 0 | 0 | 0 | 0 | . | 1 | 1 |
| a6 | 0 | 0 | 0 | 0 | 0 | 0 | . | 0 |
| a7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | . |

On the second swarm run the same ablation loses the two-hop edge (a2 to a5) and adds no
spurious one: 21 edges, all direct. The size of the effect depends on how much the
receiving agents reused what they read; the first run had more reuse. In both runs the
map without the filter is wrong, in the first by four edges and one misattribution, in
the second by one lost edge.

On the planted benchmark the same ablation is neutral (t* = 0.2, precision 0.995, recall
0.99 without the filter against 0.985 and 0.9875 with it): planted leaks are already
attributable and there is nothing to launder. The filter's value is attribution in live
runs, which the benchmark cannot test.

The convergence filter, ablated on the benchmark: t* moves from 0.35 to 0.30 (precision
0.956, recall 0.985, 18 false-alarm pairs). The operating point barely changes; what
changes is volume below it, 12,081 non-zero negative pairs without the filter against
1,967 with it. The K sweep in §7 shows the same trade at intermediate settings.

## 6 Claim: the a-priori Jaccard threshold was wrong, not Jaccard itself

The configuration first proposed was MinHash Jaccard between the leaked text and the
receiving entry at a threshold of 0.7. On the merged corpus that recalls 23.5%
(`results_jaccard/headline_jaccard.md`). The reason is structural: a 100-character leak
inside a 3,000-character tool output has Jaccard around 0.03 by construction, so a
threshold chosen for near-duplicate documents cannot fire on an embedded leak.

Calibrated on the benchmark, Jaccard does carry the information. Its best threshold is
0.15, where precision is 1.0 and recall 95.75%, slightly above containment's 92.75% at
0.35. At 0.1 it is 0.949 / 0.9825; at 0.05, 0.752 / 0.9925.

What containment buys is not accuracy but a threshold with a stable meaning. Containment
asks what fraction of the leaked window came back, so 0.35 means the same thing whether
the receiving entry is 200 or 4,000 characters. A Jaccard threshold is a ratio to the
receiving entry's size, so its best value shifts with the distribution of tool-output
lengths and would have to be re-fitted on each harness. Both scores are reported; the
detector decides on containment for that reason. The earlier draft's "13% at 0.7" was
the first, short-task corpus; 23.5% is the merged corpus and supersedes it.

## 6c Claim: source attribution is exact

The cross-organisational use of the detector (a lab answering "did text from your run
reach ours" from originated hash sets, without exchanging transcripts) depends on the
detector naming the right source, not only reporting a hit. Experiment A measures this
directly: every planted leak has a known source run among 39 candidates. For each of the
371 recalled cases, the source run with the highest containment score on the injected
entry was compared with the true source. All 371 were attributed correctly; none was
attributed to another run (`raw_hits.jsonl`, threshold 0.35). Chance is 1 in 39. On the
live swarms the same holds at the edge level (38 direct edges all pointing at the agent
whose file was read, and the two two-hop edges credited to the original author rather
than the intermediary). Attribution is therefore as reliable as detection on this
benchmark, with the same caveats: verbatim and lightly transformed text, a single model.

## 6b Claim: watermarking measured on matched artifacts (Experiment C)

Watermarking cannot be applied to the agents themselves (API access only), so it was
measured separately on a local open-weight model, Qwen2.5-0.5B-Instruct, with the
green-list scheme of Kirchenbauer et al. (hash-partitioned green list per previous
token and run-key, gamma 0.25, delta 2.0, sampling at T = 0.8, top-p 0.95). The model was
prompted for the four artifact types at four target lengths, ten samples per cell with
the watermark and ten without, over a key space of 32 run-keys. Detection is the
green-token z-score under the true key. The 1% false-alarm threshold was set from the
empirical null: every unwatermarked sample scored against every key, 5,120 scores.

Empirical threshold. The 1% quantile of the null is z = 3.77, against 2.33 for the
textbook normal approximation. On repetitive low-entropy text the same bigram recurs
and is green or red every time, so green counts are not independent and the null is
wider than assumed. Using the textbook threshold on agent-style artifacts gives 5.3% false alarms, five
times the nominal rate (`data/results_c/scores.jsonl`, 5,120 null scores).

Table 4. Detection rate at 1% FPR by artifact type and generated length; n = 10 per cell.
Mean generated length in brackets where the model stopped short of the target.

| type | 50 | 100 | 200 | 500 |
|---|---|---|---|---|
| prose | 0.80 | 0.80 | 1.00 | 1.00 (464) |
| code | 0.20 | 0.80 | 0.70 | 1.00 |
| structured | 0.20 | 0.90 | 0.70 (178) | 0.80 (201) |
| terse | 0.40 | 1.00 | 1.00 (192) | 1.00 (332) |

Truncated to the first 50 tokens of every sample: prose 0.62, code 0.38, structured
0.30, terse 0.66. First 100: 0.87, 0.60, 0.76, 0.97.

Table 5. Next-token entropy of the unwatermarked samples, the room a watermark has.

| type | mean entropy (nats) | share of tokens under 0.5 nat |
|---|---|---|
| prose | 1.38 | 0.29 |
| terse | 1.27 | 0.34 |
| code | 0.75 | 0.53 |
| structured | 0.73 | 0.66 |

Table 6. False-alarm rate when one text is scanned against N run-keys and the maximum
score is taken, at the single-key 1% threshold.

| N | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| FPR | 0.010 | 0.021 | 0.041 | 0.073 | 0.109 | 0.156 |

Reading against Experiment A. With full model access and no transformation of the text,
the watermark detects 20 to 40% of 50-token code, JSON and shell artifacts and 70 to
100% from 100 tokens, and its false-alarm rate grows with the number of parallel runs
scanned. Hashing, with no model access, found 100% of verbatim leaks of 100 tokens or
more of every type at zero observed false alarms, and its false-alarm rate does not
depend on the number of runs because there is no per-run key to scan against. The
comparison is on matched artifact types, not identical text, and on a 0.5B model rather
than the agents' model; both caveats favour the watermark (a stronger model has higher
entropy prose but not higher entropy JSON).



The 29 misses at t = 0.35 decompose exactly:

| misses | what they are |
|---|---|
| 21 | 25-token leaks (one window; after filtering often under the 40-shingle floor) |
| 6 | paraphrased leaks of 50 or 100 tokens |
| 2 | 50-token prose, one reformatted, one truncated |

Minimum detectable unit and the evidence floor. A 25-token leak is about one
100-character window. After the two filters its attributable content is often below 40
shingles, and the score is capped at (attributable / 40). About 40 characters of
attributable text is the smallest leak that can score highly. The floor is a measured
trade, isolated on the merged corpus (`results_nofloor`): without it, 13 false-alarm
pairs at 0.35 and recall 94.75%; with it, 0 and 92.75%. Thirteen false alarms bought
for eight leaks, all of them 25-token (verbatim prose at 25 tokens goes from 0.60 to
0.40).

Prose at short lengths and the convergence rule. Verbatim prose recall at 25 tokens is
0.40 against 1.00 for structured and terse. The cause is the convergence filter: at
K = 2 it removes every shingle that any two of the 40 solo runs originated, and ordinary
English shares far more 5-grams across unrelated documents than code or JSON does. The
sweep (`results_k3`, `results_k5`, `results_k10`) makes K a measured dial:

| K | recall at 0.35 | false-alarm pairs at 0.35 | precision | verbatim prose at 25 tokens | non-zero negative pairs |
|---|---|---|---|---|---|
| 2 | 0.928 | 0 | 1.000 | 0.40 | 1,967 |
| 3 | 0.950 | 3 | 0.992 | 0.80 | 4,853 |
| 5 | 0.968 | 4 | 0.990 | 1.00 | 8,192 |
| 10 | 0.968 | 50 | 0.886 | 1.00 | 11,954 |
| off | 0.970 | 10 | 0.975 | | 12,081 |

K = 5 recovers every short prose leak for four false-alarm pairs in about 400 hits;
K = 10 gains nothing further and costs fifty. K = 2 is reported as the operating point
because it is the only zero-false-alarm setting; a harness that prefers recall should
run K = 5. The earlier draft's suggestion that K should scale with corpus size is wrong:
larger K loses precision quickly. Weighting shingles by document frequency instead of
removing them remains the untested alternative.

Paraphrase. At t = 0.7 paraphrased prose of 100 tokens or less is mostly missed. At 0.35
paraphrased leaks of 200 tokens or more are always found and shorter ones mostly,
because identifiers, keys, paths and numbers survive a rewrite. The paraphraser was the
same model as the agents. Someone who also renamed identifiers would win; this detector
is for unintended leaks.

## 8 Threats to validity

- Five planted leaks per cell. Cell values move in steps of 0.2. Trust the aggregate.
- Precision counts only non-zero-scoring negative pairs; the false-alarm bound is
  conservative for that reason.
- The convergence rule K = 2 and the evidence floor of 40 were both first settings that
  happened to be the zero-false-alarm ones; the sweeps in §7 show the trade around them
  but nothing was cross-validated, and 400 cases with 5 per cell cannot resolve
  differences of one or two false alarms.
- One model wrote the corpus and the paraphrases. Two models were used only for the
  silent-runs claim. Nothing is claimed about frontier models under adversarial
  pressure.
- Read-back laundering: a run that reads its own file and rewrites it keeps only its
  first emission attributable.
- The explicit swarm runs are demonstrations on eight agents with an instructed
  protocol. They show topology recovery on real transmissions (two runs, 40 edges); they
  do not estimate how often agents leak.
- Watermarking was measured on a different, smaller model than the agents, on prompted
  artifacts rather than harness transcripts, with one scheme (KGW) at one setting. It
  needs logit access, which is why it could not be run on the agents, and why an outside
  evaluator could never watermark a lab's model.

## Appendix: reproduce

```
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
export OPENAI_API_KEY=...                     # set a spend cap first
docker pull python:3.11-slim
python code/harness.py --agents 1 --turns 3 --run-root data/runs/smoke && python code/detector.py data/runs/smoke
bash scripts/run_all.sh core     # corpora, baseline, benchmark, ablations
bash scripts/run_all.sh swarm    # containment arms and the explicit arm
bash scripts/run_all.sh check    # containment arms with gpt-4.1
bash scripts/run_extra.sh        # K sweep, floor ablation, long-task baseline, second explicit swarm
bash scripts/rederive.sh         # recompute every number above from runs/ and data/cases/, offline
pip install torch transformers accelerate && python code/experiment_c.py --n 10   # Experiment C, ~7 min on an M4
python code/verify_edges.py data/runs/swarm_directed_explicit/hits.json   # edge-by-edge check against reads
```
Every table above is re-derived offline by `code/score.py`, `detector.py` and
`topology.py` from `runs/` and `data/cases/`.

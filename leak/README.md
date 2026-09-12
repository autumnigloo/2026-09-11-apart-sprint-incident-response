# Cross-run leak detection for agent evaluation sandboxes

Content-hashing detector that finds text one agent produced inside another agent's
inputs, with a measured comparison against per-run keyed watermarking, with an origination filter (only text a run authored counts), a convergence
filter (shared skeleton is not evidence), and a cross-run matrix that is classified into
a leak topology. Includes the labelled benchmark (Experiment A), the convergence baseline
(A0), the live-swarm demonstration (Experiment B), and an auto-written lab notebook.

Results, figures and the write-up are in `RESULTS.md`. The per-run notebook is
`OBSERVATIONS.md`.

## Layout

```
harness.py              agent harness: one gpt-4.1-mini agent per Docker container (--network none),
                        private /work, optional shared /shared, JSONL transcripts with INGRESS/EGRESS tags
detector.py             normalise -> char 5-grams -> origination filter -> convergence filter
                        -> containment of 100-char source windows in other runs' INGRESS -> hits + matrix
topology.py             classifies the matrix: none / directed / bidirectional / shared_medium; draws SVG
benchmark/inject.py     Experiment A: plants typed, sized, transformed spans from solo run A into run B
benchmark/score.py      Experiment A: precision/recall per cell, PR sweep, negative-set floors, ablations
notebook.py             appends a dated summary of any run dir or results dir to OBSERVATIONS.md
shared_usage.py         lists every bash command that touched /shared (ground truth for Experiment B)
verify_edges.py         labels every detected edge direct / two-hop / unknown against those reads
run_all.sh              reproduces everything in order; resumes after a crash
run_extra.sh            K sweep, evidence-floor ablation, long-task baseline, second explicit swarm
rederive.sh             recomputes every reported number from the raw data, offline; use to audit
experiment_c.py         Experiment C: keyed watermark (KGW) on a local 0.5B model, by artifact type,
                        length and number of run-keys; writes results_c/summary.md
tasks_solo.txt          20 distinct short tasks (corpus part 1)
tasks_solo_long.txt     20 distinct long tasks: 150-line module, 400-word README, 40-key config (part 2)
tasks_swarm.txt         8 tasks for the containment arms, 2 impossible
runs/                   transcripts of every run reported (container scratch removed)
benchmark/cases/        the 400 labelled cases, paraphrase cache, and results*/ directories
```

## Reproduce

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=...           # set a hard spend cap first; the whole study cost under EUR 5
docker pull python:3.11-slim
python harness.py --agents 1 --turns 3 --run-root runs/smoke && python detector.py runs/smoke
bash run_all.sh core                # corpora, baseline, benchmark, ablations (~40 min, mostly API latency)
bash run_all.sh swarm               # Experiment B (~25 min)
bash run_all.sh check               # containment arms repeated with gpt-4.1 (~15 min, a few EUR)
bash run_extra.sh                   # sweeps, floor ablation, long-task baseline, second swarm (~30 min)
pip install torch transformers accelerate && python experiment_c.py --n 10   # watermark measurement (~7 min)
```

Everything after the harness runs is offline and deterministic; `score.py` alone re-derives
every table from `benchmark/cases/` and `runs/`.

## Detector in one paragraph

Text is NFKC-normalised with control characters removed and whitespace collapsed, then
hashed into character 5-grams. Per run, in transcript order, every shingle that entered
the context (prompt, tool output, file read-back) is recorded; an EGRESS span's evidence
is its shingles minus everything ingested before it was emitted (origination). Shingles
originated by two or more solo runs are removed as convergent skeleton. Spans are cut
into 100-character windows. Score of a source span against a target INGRESS entry is
`|window ∩ entry| / max(|window|, 40)`: containment with a 40-shingle evidence floor, so
that a window left with a handful of generic shingles cannot score high. MinHash Jaccard
(128 permutations) against 200-character target windows is reported alongside because it
was the configuration proposed originally; it is not used for decisions. Operating point
in the report: 0.35.

## Known limits (see RESULTS.md §6)

Non-adversarial threat model. Minimum detectable unit about 40 characters of attributable
text. Read-back laundering keeps only a run's first emission attributable. Single model.
n = 5 per benchmark cell. Experiment B is a demonstration, not a rate estimate.

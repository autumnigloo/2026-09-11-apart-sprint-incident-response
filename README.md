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
README.md, RESULTS.md, OBSERVATIONS.md, leak_explainer.html, requirements.txt
code/
  harness.py          agent harness: one model instance per Docker container (--network none),
                      private /work, optional shared /shared, JSONL transcripts tagged INGRESS/EGRESS
  detector.py         normalise -> char 5-grams -> origination filter -> convergence filter
                      -> containment of 100-char windows in other runs' INGRESS -> hits + matrix
  topology.py         classifies the matrix: none / directed / bidirectional / shared_medium; draws SVG
  inject.py           Experiment A: plants typed, sized, transformed spans from solo run A into run B
  score.py            Experiment A: precision/recall per cell, PR sweep, negative-set floors, ablations
  shared_usage.py     every bash command that touched /shared (ground truth for Experiment B)
  verify_edges.py     labels every detected edge direct / two-hop / unknown against those reads
  notebook.py         appends a dated summary of a run or results dir to OBSERVATIONS.md
  experiment_c.py     Experiment C: keyed watermark on a local 0.5B model, by type, length, key count
scripts/
  run_all.sh          corpora, baseline, benchmark, ablations, swarm arms, gpt-4.1 check; resumes
  run_extra.sh        K sweep, floor ablation, long-task baseline, second swarm
  rederive.sh         recomputes every reported number from data/, offline; the audit
tasks/                task lists: 20 short, 20 long, 8 for the swarm (2 impossible)
data/
  runs/               transcripts of every run reported (container scratch removed)
  cases/              the 400 labelled cases, paraphrase cache, results*/ directories
  rederived/          output of the audit run
  results_c/          Experiment C summary and per-sample scores
logs/                 run_extra.log, rederive.log, experiment_c.log
```

All commands are run from the repository root.

## Reproduce

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=...           # set a hard spend cap first; the whole study cost under EUR 5
docker pull python:3.11-slim
python code/harness.py --agents 1 --turns 3 --run-root data/runs/smoke && python code/detector.py data/runs/smoke
bash scripts/run_all.sh core                # corpora, baseline, benchmark, ablations (~40 min, mostly API latency)
bash scripts/run_all.sh swarm               # Experiment B (~25 min)
bash scripts/run_all.sh check               # containment arms repeated with gpt-4.1 (~15 min, a few EUR)
bash scripts/run_extra.sh                   # sweeps, floor ablation, long-task baseline, second swarm (~30 min)
pip install torch transformers accelerate && python code/experiment_c.py --n 10   # watermark measurement (~7 min)
```

Everything after the harness runs is offline and deterministic; `score.py` alone re-derives
every table from `data/cases/` and `runs/`.

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

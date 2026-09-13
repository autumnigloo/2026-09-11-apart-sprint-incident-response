<p align="center"><img src="docs/img/banner.svg" alt="Cross-run leak detection: who leaked to whom, from the transcripts alone" width="100%"></p>

<p align="center">
<a href="RESULTS.md">Results</a> &nbsp;•&nbsp;
<a href="leak_explainer.html">Visual walkthrough</a> &nbsp;•&nbsp;
<a href="OBSERVATIONS.md">Lab notebook</a> &nbsp;•&nbsp;
<a href="#reproduce">Reproduce</a>
</p>

When many AI agents run in parallel with a shared cache, proxy or folder, text one agent wrote can end up in front of another. Evaluation harnesses promise per-task isolation and say nothing about that. This repository detects such leaks from the transcripts alone, credits each piece of text to its first author, and draws the map of who leaked to whom.

<p align="center"><img src="docs/img/scoreboard.svg" alt="371 of 400 planted leaks found; 0 false alarms; 40 of 40 swarm edges explained; a watermark catches 1 in 5 short code samples" width="100%"></p>

## The detector

<p align="center"><img src="docs/img/pipeline.svg" alt="transcripts, shingles, origination filter, convergence filter, containment, hit matrix, topology" width="100%"></p>

Two filters make attribution honest. **Origination**: a run is credited only with text it produced before that text ever entered its context, so an echoed prompt or a rewritten file never counts as the run's own. **Convergence**: shared skeleton (`import json`, `__main__` guards, pip output) is not evidence, because any two agents writing Python will both write it. The score asks how much of a leaked window came back, with a 40-shingle evidence floor so a window left with a dozen generic pieces cannot score 1.0. All of it is in [`code/detector.py`](code/detector.py).

## What was measured

<details open>
<summary><b>Experiment A &nbsp;·&nbsp; 400 planted leaks</b></summary>
<br>

Forty solo agents ran with no shared folder, so their transcripts contain no leak. Then 400 leaks were planted: a span of one agent's own text (prose, code, JSON, shell), 25 to 500 tokens, verbatim or reformatted or truncated or paraphrased by the same model, pasted into another agent's transcript as a `cat /shared/...` output.

| threshold | precision | recall | false-alarm pairs |
|:---:|:---:|:---:|:---:|
| 0.20 | 0.985 | 0.988 | 6 |
| **0.35** | **1.000** | **0.928** | **0** |
| 0.70 | 1.000 | 0.710 | 0 |

Every leak of 100 tokens or more that was not paraphrased was found, for every type, and every one of the 371 recalled leaks was attributed to the correct source run out of 39 candidates. The 29 misses at 0.35: 21 are 25-token leaks, 6 paraphrases, 2 short prose. The convergence rule and the evidence floor are each a measured dial; see the K sweep and floor ablation in [`RESULTS.md`](RESULTS.md).
</details>

<details open>
<summary><b>Silence tests &nbsp;·&nbsp; where nothing can have leaked</b></summary>
<br>

| test | result |
|---|:---:|
| 8 agents, identical short task, no shared folder | 0 hits |
| 8 agents, identical long task (150-line module, README, config) | 0 hits |
| 40 solo runs scanned against each other | 0 hits |
| 48 agents with a shared folder and no instruction to use it: gpt-4.1-mini and gpt-4.1, six conditions, two impossible tasks | 0 commands touched it, 0 hits |

Under pressure from an unsatisfiable dependency, gpt-4.1 probed the closed network path (pip, ping, nslookup, resolv.conf, apt-get) and never the open shared folder.
</details>

<details open>
<summary><b>Experiment B &nbsp;·&nbsp; a live swarm with a shared folder</b></summary>
<br>

Eight agents told to coordinate through `/shared`, started 45 seconds apart, run twice on different tasks. Every edge the detector drew points from an earlier start to a later one, and every edge has a read behind it in the transcript.

<p align="center"><img src="docs/img/topology_run1.svg" alt="Recovered topology of the first swarm run: 17 direct edges and one two-hop edge, none backwards" width="100%"></p>

Second run: 22 edges, 21 direct, 1 two-hop. Switching the origination filter off adds four edges that correspond to no read and loses the two-hop one; the map is wrong without it. Checked by [`code/verify_edges.py`](code/verify_edges.py), not by eye.
</details>

<details open>
<summary><b>Experiment C &nbsp;·&nbsp; the watermark alternative, measured</b></summary>
<br>

Per-run keyed watermarking was the original plan. It needs the model's logits, so it could not run on the agents; it was measured on a local 0.5B model generating the same four artifact types.

<p align="center"><img src="docs/img/compare.svg" alt="Entropy per artifact type, watermark detection at 50 tokens, and hashing recall" width="100%"></p>

At 100 tokens the watermark reaches 80 to 100%. The textbook 1% threshold gave 5.3% false alarms on this kind of text, because repetitive artifacts break the independence the threshold assumes.
</details>

## Layout

```
README.md  RESULTS.md  OBSERVATIONS.md  leak_explainer.html  requirements.txt
code/       harness.py detector.py topology.py inject.py score.py shared_usage.py verify_edges.py notebook.py experiment_c.py
scripts/    run_all.sh run_extra.sh rederive.sh
tasks/      20 short tasks, 20 long tasks, 8 swarm tasks (2 impossible)
data/       runs/ (every transcript reported)  cases/ (400 labelled cases + results)  rederived/  results_c/
logs/       run_extra.log rederive.log experiment_c.log
docs/img/   the figures on this page
```

<details>
<summary>What each file does</summary>
<br>

| file | role |
|---|---|
| `code/harness.py` | one model instance per Docker container (`--network none`), private `/work`, optional shared `/shared`, JSONL transcripts tagged INGRESS/EGRESS; task files, instruction arms, same-task mode, staggered starts |
| `code/detector.py` | the pipeline above; hits and the N × N matrix |
| `code/topology.py` | classifies the matrix and draws it |
| `code/inject.py`, `code/score.py` | Experiment A: plant the leaks; precision/recall per cell, threshold sweep, negative sets, ablations |
| `code/shared_usage.py`, `code/verify_edges.py` | ground truth for Experiment B and the edge-by-edge check against it |
| `code/notebook.py` | appends a dated summary of any run to `OBSERVATIONS.md` |
| `code/experiment_c.py` | keyed green-list watermark on a local model: detection by type and length, entropy by type, false alarms against N keys |
| `scripts/run_all.sh` | everything in order; resumes after a crash |
| `scripts/run_extra.sh` | K sweep, floor ablation, long-task baseline, second swarm |
| `scripts/rederive.sh` | recomputes every reported number from `data/`, offline; the audit |
</details>

## Reproduce

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=...            # set a hard spend cap first; the whole study was about ten euros of API use
docker pull python:3.11-slim
python code/harness.py --agents 1 --turns 3 --run-root data/runs/smoke && python code/detector.py data/runs/smoke

bash scripts/run_all.sh core         # corpora, baseline, benchmark, ablations                 ~40 min, mostly API latency
bash scripts/run_all.sh swarm        # Experiment B                                            ~25 min
bash scripts/run_all.sh check        # containment arms with gpt-4.1                           ~15 min
bash scripts/run_extra.sh            # K sweep, floor ablation, long baseline, second swarm    ~30 min
pip install torch transformers accelerate && python code/experiment_c.py --n 10                # Experiment C, ~7 min on an M4
```

Everything after the agent runs is offline and deterministic. `bash scripts/rederive.sh` recomputes every number in `RESULTS.md` from the transcripts in `data/`; the log of the last audit is [`logs/rederive.log`](logs/rederive.log).

## What this does not claim

Non-adversarial threat model: an agent that rewrote identifiers on purpose would defeat it. The smallest detectable leak is about 40 characters of text the agent actually originated. An agent that reads its own file back keeps only its first version as its own. Five planted leaks per benchmark cell. The corpus and paraphrases come from one model; the silence tests used two. Experiment B shows the map can be recovered from real transmissions, not how often agents leak. Experiment C ran on a different, smaller model than the agents. Details in [`RESULTS.md`](RESULTS.md).

<p align="center"><sub>Apart Research incident-response sprint, 11 to 13 September 2026</sub></p>

#!/usr/bin/env bash
# Reproduces every experiment in the report, in order, writing OBSERVATIONS.md as it goes.
#   bash run_all.sh            everything
#   bash run_all.sh core       corpora, A0, inject, score (Experiment A + baseline)
#   bash run_all.sh swarm      Experiment B: three containment arms + the explicit arm
#   bash run_all.sh check      Experiment B containment arms repeated with gpt-4.1
# Steps whose output exists are skipped, so a re-run after a crash resumes.
# Needs: .venv active, OPENAI_API_KEY exported, docker running, smoke test passed:
#   python code/harness.py --agents 1 --turns 3 --run-root data/runs/smoke && python code/detector.py data/runs/smoke
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:-all}"
TURNS="${TURNS:-25}"
REPS="${REPS:-5}"
TH="${TH:-0.35}"      # operating point reported in the paper

log() { echo; echo "=== $(date +%H:%M) $*"; }
awake() { if command -v caffeinate >/dev/null; then caffeinate -i "$@"; else "$@"; fi; }

if [[ "$MODE" == "all" || "$MODE" == "core" ]]; then
  if [[ ! -f data/runs/corpus/agent-19/transcript.jsonl ]]; then
    log "corpus: 20 solo agents, short tasks"
    awake python code/harness.py --agents 20 --turns "$TURNS" --tasks tasks/tasks_solo.txt --run-root data/runs/corpus
  fi
  python code/notebook.py data/runs/corpus --threshold "$TH" --note "solo corpus, short tasks"

  if [[ ! -f data/runs/corpus_long/agent-19/transcript.jsonl ]]; then
    log "corpus_long: 20 solo agents, long tasks (150-line module, 400-word README, 40-key config)"
    awake python code/harness.py --agents 20 --turns "$TURNS" --tasks tasks/tasks_solo_long.txt --run-root data/runs/corpus_long
  fi
  python code/notebook.py data/runs/corpus_long --threshold "$TH" --note "solo corpus, long tasks"

  if [[ ! -d data/runs/corpus_all/agent-39 ]]; then
    log "merge into data/runs/corpus_all (agent-0..19 short, agent-20..39 long)"
    mkdir -p data/runs/corpus_all
    cp -r data/runs/corpus/agent-* data/runs/corpus_all/
    for i in $(seq 0 19); do cp -r "data/runs/corpus_long/agent-$i" "data/runs/corpus_all/agent-$((i+20))"; done
  fi

  if [[ ! -f data/runs/a0/agent-7/transcript.jsonl ]]; then
    log "a0: 8 agents, same task, no shared volume (convergence baseline)"
    awake python code/harness.py --agents 8 --turns "$TURNS" --same-task 0 --tasks tasks/tasks_solo.txt --run-root data/runs/a0
  fi
  python code/notebook.py data/runs/a0 --threshold "$TH" --note "convergence baseline; every hit is a false positive"

  if [[ ! -f data/cases/labels.jsonl ]]; then
    log "inject: labelled cases from the merged corpus (paraphrase uses the API, cached)"
    python code/inject.py data/runs/corpus_all --out data/cases --reps "$REPS"
  fi

  log "score: main (tables at t*=auto and t=$TH), jaccard, two ablations"
  python code/score.py data/cases --fixed "$TH" --negatives data/runs/corpus_all data/runs/a0
  python code/score.py data/cases --fixed "$TH" --score jaccard --negatives data/runs/corpus_all data/runs/a0 --out data/cases/results_jaccard
  python code/score.py data/cases --fixed "$TH" --no-origination --out data/cases/results_no_origination
  python code/score.py data/cases --fixed "$TH" --common-runs 0 --out data/cases/results_no_convergence
  for d in results results_jaccard results_no_origination results_no_convergence; do
    python code/notebook.py "data/cases/$d" --note "Experiment A: $d"
  done
  log "core done: data/cases/results/headline_containment.md"
fi

if [[ "$MODE" == "all" || "$MODE" == "swarm" ]]; then
  for arm in unspecified prohibited directed; do
    if [[ ! -f "data/runs/swarm_$arm/agent-7/transcript.jsonl" ]]; then
      log "swarm arm=$arm: 8 agents, shared volume, short tasks (2 impossible)"
      awake python code/harness.py --agents 8 --turns "$TURNS" --shared --arm "$arm" --tasks tasks/tasks_swarm.txt --run-root "data/runs/swarm_$arm"
    fi
    python code/shared_usage.py "data/runs/swarm_$arm"
    python code/detector.py "data/runs/swarm_$arm" --threshold "$TH" --out "data/runs/swarm_$arm/hits.json" >/dev/null
    python code/topology.py "data/runs/swarm_$arm/hits.json" --svg "data/runs/swarm_$arm/topology.svg" >/dev/null
    python code/notebook.py "data/runs/swarm_$arm" --threshold "$TH" --note "Experiment B arm=$arm"
  done
  arm=directed_explicit
  if [[ ! -f "data/runs/swarm_$arm/agent-7/transcript.jsonl" ]]; then
    log "swarm arm=$arm: protocol in the task text, long tasks, 45 s stagger"
    awake python code/harness.py --agents 8 --turns "$TURNS" --shared --arm "$arm" --tasks tasks/tasks_solo_long.txt --stagger 45 --run-root "data/runs/swarm_$arm"
  fi
  python code/shared_usage.py "data/runs/swarm_$arm"
  python code/detector.py "data/runs/swarm_$arm" --threshold "$TH" --out "data/runs/swarm_$arm/hits.json" >/dev/null
  python code/detector.py "data/runs/swarm_$arm" --threshold "$TH" --no-origination --out "data/runs/swarm_$arm/hits_no_origination.json" >/dev/null
  python code/topology.py "data/runs/swarm_$arm/hits.json" --svg "data/runs/swarm_$arm/topology.svg" >/dev/null
  python code/notebook.py "data/runs/swarm_$arm" --threshold "$TH" --note "Experiment B arm=$arm (ablation matrix in hits_no_origination.json)"
  log "swarm done"
fi

if [[ "$MODE" == "all" || "$MODE" == "check" ]]; then
  for cond in "unspecified tasks/tasks_solo_long.txt swarm_unspecified_gpt41" \
              "prohibited tasks/tasks_solo_long.txt swarm_prohibited_gpt41" \
              "unspecified tasks/tasks_swarm.txt swarm_unspecified_gpt41_impossible"; do
    set -- $cond; arm=$1; tasks=$2; dir=$3
    if [[ ! -f "data/runs/$dir/agent-7/transcript.jsonl" ]]; then
      log "gpt-4.1 check: arm=$arm tasks=$tasks"
      MODEL=gpt-4.1 awake python code/harness.py --agents 8 --turns "$TURNS" --shared --arm "$arm" --tasks "$tasks" --run-root "data/runs/$dir"
    fi
    python code/shared_usage.py "data/runs/$dir"
    python code/detector.py "data/runs/$dir" --threshold "$TH" --out "data/runs/$dir/hits.json" >/dev/null
    python code/notebook.py "data/runs/$dir" --threshold "$TH" --note "Experiment B containment arm, gpt-4.1, arm=$arm tasks=$tasks"
  done
  log "check done"
fi

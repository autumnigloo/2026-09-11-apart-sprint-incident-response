#!/usr/bin/env bash
# Reproduces every experiment in the report, in order, writing OBSERVATIONS.md as it goes.
#   bash run_all.sh            everything
#   bash run_all.sh core       corpora, A0, inject, score (Experiment A + baseline)
#   bash run_all.sh swarm      Experiment B: three containment arms + the explicit arm
#   bash run_all.sh check      Experiment B containment arms repeated with gpt-4.1
# Steps whose output exists are skipped, so a re-run after a crash resumes.
# Needs: .venv active, OPENAI_API_KEY exported, docker running, smoke test passed:
#   python harness.py --agents 1 --turns 3 --run-root runs/smoke && python detector.py runs/smoke
set -euo pipefail
cd "$(dirname "$0")"
MODE="${1:-all}"
TURNS="${TURNS:-25}"
REPS="${REPS:-5}"
TH="${TH:-0.35}"      # operating point reported in the paper

log() { echo; echo "=== $(date +%H:%M) $*"; }
awake() { if command -v caffeinate >/dev/null; then caffeinate -i "$@"; else "$@"; fi; }

if [[ "$MODE" == "all" || "$MODE" == "core" ]]; then
  if [[ ! -f runs/corpus/agent-19/transcript.jsonl ]]; then
    log "corpus: 20 solo agents, short tasks"
    awake python harness.py --agents 20 --turns "$TURNS" --tasks tasks_solo.txt --run-root runs/corpus
  fi
  python notebook.py runs/corpus --threshold "$TH" --note "solo corpus, short tasks"

  if [[ ! -f runs/corpus_long/agent-19/transcript.jsonl ]]; then
    log "corpus_long: 20 solo agents, long tasks (150-line module, 400-word README, 40-key config)"
    awake python harness.py --agents 20 --turns "$TURNS" --tasks tasks_solo_long.txt --run-root runs/corpus_long
  fi
  python notebook.py runs/corpus_long --threshold "$TH" --note "solo corpus, long tasks"

  if [[ ! -d runs/corpus_all/agent-39 ]]; then
    log "merge into runs/corpus_all (agent-0..19 short, agent-20..39 long)"
    mkdir -p runs/corpus_all
    cp -r runs/corpus/agent-* runs/corpus_all/
    for i in $(seq 0 19); do cp -r "runs/corpus_long/agent-$i" "runs/corpus_all/agent-$((i+20))"; done
  fi

  if [[ ! -f runs/a0/agent-7/transcript.jsonl ]]; then
    log "a0: 8 agents, same task, no shared volume (convergence baseline)"
    awake python harness.py --agents 8 --turns "$TURNS" --same-task 0 --tasks tasks_solo.txt --run-root runs/a0
  fi
  python notebook.py runs/a0 --threshold "$TH" --note "convergence baseline; every hit is a false positive"

  if [[ ! -f benchmark/cases/labels.jsonl ]]; then
    log "inject: labelled cases from the merged corpus (paraphrase uses the API, cached)"
    python benchmark/inject.py runs/corpus_all --out benchmark/cases --reps "$REPS"
  fi

  log "score: main (tables at t*=auto and t=$TH), jaccard, two ablations"
  python benchmark/score.py benchmark/cases --fixed "$TH" --negatives runs/corpus_all runs/a0
  python benchmark/score.py benchmark/cases --fixed "$TH" --score jaccard --negatives runs/corpus_all runs/a0 --out benchmark/cases/results_jaccard
  python benchmark/score.py benchmark/cases --fixed "$TH" --no-origination --out benchmark/cases/results_no_origination
  python benchmark/score.py benchmark/cases --fixed "$TH" --common-runs 0 --out benchmark/cases/results_no_convergence
  for d in results results_jaccard results_no_origination results_no_convergence; do
    python notebook.py "benchmark/cases/$d" --note "Experiment A: $d"
  done
  log "core done: benchmark/cases/results/headline_containment.md"
fi

if [[ "$MODE" == "all" || "$MODE" == "swarm" ]]; then
  for arm in unspecified prohibited directed; do
    if [[ ! -f "runs/swarm_$arm/agent-7/transcript.jsonl" ]]; then
      log "swarm arm=$arm: 8 agents, shared volume, short tasks (2 impossible)"
      awake python harness.py --agents 8 --turns "$TURNS" --shared --arm "$arm" --tasks tasks_swarm.txt --run-root "runs/swarm_$arm"
    fi
    python shared_usage.py "runs/swarm_$arm"
    python detector.py "runs/swarm_$arm" --threshold "$TH" --out "runs/swarm_$arm/hits.json" >/dev/null
    python topology.py "runs/swarm_$arm/hits.json" --svg "runs/swarm_$arm/topology.svg" >/dev/null
    python notebook.py "runs/swarm_$arm" --threshold "$TH" --note "Experiment B arm=$arm"
  done
  arm=directed_explicit
  if [[ ! -f "runs/swarm_$arm/agent-7/transcript.jsonl" ]]; then
    log "swarm arm=$arm: protocol in the task text, long tasks, 45 s stagger"
    awake python harness.py --agents 8 --turns "$TURNS" --shared --arm "$arm" --tasks tasks_solo_long.txt --stagger 45 --run-root "runs/swarm_$arm"
  fi
  python shared_usage.py "runs/swarm_$arm"
  python detector.py "runs/swarm_$arm" --threshold "$TH" --out "runs/swarm_$arm/hits.json" >/dev/null
  python detector.py "runs/swarm_$arm" --threshold "$TH" --no-origination --out "runs/swarm_$arm/hits_no_origination.json" >/dev/null
  python topology.py "runs/swarm_$arm/hits.json" --svg "runs/swarm_$arm/topology.svg" >/dev/null
  python notebook.py "runs/swarm_$arm" --threshold "$TH" --note "Experiment B arm=$arm (ablation matrix in hits_no_origination.json)"
  log "swarm done"
fi

if [[ "$MODE" == "all" || "$MODE" == "check" ]]; then
  for cond in "unspecified tasks_solo_long.txt swarm_unspecified_gpt41" \
              "prohibited tasks_solo_long.txt swarm_prohibited_gpt41" \
              "unspecified tasks_swarm.txt swarm_unspecified_gpt41_impossible"; do
    set -- $cond; arm=$1; tasks=$2; dir=$3
    if [[ ! -f "runs/$dir/agent-7/transcript.jsonl" ]]; then
      log "gpt-4.1 check: arm=$arm tasks=$tasks"
      MODEL=gpt-4.1 awake python harness.py --agents 8 --turns "$TURNS" --shared --arm "$arm" --tasks "$tasks" --run-root "runs/$dir"
    fi
    python shared_usage.py "runs/$dir"
    python detector.py "runs/$dir" --threshold "$TH" --out "runs/$dir/hits.json" >/dev/null
    python notebook.py "runs/$dir" --threshold "$TH" --note "Experiment B containment arm, gpt-4.1, arm=$arm tasks=$tasks"
  done
  log "check done"
fi

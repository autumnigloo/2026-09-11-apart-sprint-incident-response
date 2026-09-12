#!/usr/bin/env bash
# The four follow-up checks, in order of value. Offline ones first (free), then two cheap agent runs.
#   bash run_extra.sh
set -euo pipefail
cd "$(dirname "$0")/.."
awake() { if command -v caffeinate >/dev/null; then caffeinate -i "$@"; else "$@"; fi; }
log() { echo; echo "=== $(date +%H:%M) $*"; }

log "1. convergence rule sweep (offline)"
for k in 3 5 10; do
  python code/score.py data/cases --fixed 0.35 --common-runs $k --negatives data/runs/corpus_all data/runs/a0 --out data/cases/results_k$k >/dev/null 2>&1
  echo "== K=$k"; grep -E "^Threshold" data/cases/results_k$k/headline_containment.md
  grep -A3 "verbatim: recall at fixed" data/cases/results_k$k/headline_containment.md | tail -1
  grep -E "^\| 0.35 " data/cases/results_k$k/headline_containment.md
done

log "2. evidence floor ablation (offline)"
python code/score.py data/cases --fixed 0.35 --min-evidence 0 --negatives data/runs/corpus_all data/runs/a0 --out data/cases/results_nofloor >/dev/null 2>&1
grep -E "^Threshold|^\| 0.35 " data/cases/results_nofloor/headline_containment.md
grep -A3 "verbatim: recall at fixed" data/cases/results_nofloor/headline_containment.md | tail -1

log "3. harder silence test: 8 agents, same long task, no shared folder"
if [[ ! -f data/runs/a0_long/agent-7/transcript.jsonl ]]; then
  awake python code/harness.py --agents 8 --turns 25 --same-task 0 --tasks tasks/tasks_solo_long.txt --run-root data/runs/a0_long
fi
python code/detector.py data/runs/a0_long --threshold 0.35 2>/dev/null | grep "hits at"
python code/notebook.py data/runs/a0_long --threshold 0.35 --note "convergence baseline, long task" >/dev/null

log "4. second explicit swarm, different tasks"
grep -v '^#' tasks/tasks_solo_long.txt | tail -n 8 > tasks/tasks_solo_long_b.txt
if [[ ! -f data/runs/swarm_directed_explicit_2/agent-7/transcript.jsonl ]]; then
  awake python code/harness.py --agents 8 --turns 25 --shared --arm directed_explicit --tasks tasks/tasks_solo_long_b.txt --stagger 45 --run-root data/runs/swarm_directed_explicit_2
fi
python code/shared_usage.py data/runs/swarm_directed_explicit_2
python code/detector.py data/runs/swarm_directed_explicit_2 --threshold 0.35 --out data/runs/swarm_directed_explicit_2/hits.json 2>/dev/null | tail -10
python code/topology.py data/runs/swarm_directed_explicit_2/hits.json --svg data/runs/swarm_directed_explicit_2/topology.svg | head -4
python code/notebook.py data/runs/swarm_directed_explicit_2 --threshold 0.35 --note "Experiment B explicit arm, replicate" >/dev/null

log "done. paste this whole output back."

#!/usr/bin/env bash
# One-time move from the old flat layout into data/ and logs/. Run from the repo root
# AFTER the new code tree has been copied in. Idempotent: skips what is already moved.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data logs tasks
[[ -d runs ]] && mv runs data/runs
[[ -d benchmark/cases ]] && mv benchmark/cases data/cases
[[ -d benchmark/rederived ]] && mv benchmark/rederived data/rederived
[[ -d results_c ]] && mv results_c data/results_c
for f in run_extra.log rederive.log experiment_c.log; do [[ -f $f ]] && mv "$f" logs/; done
[[ -f tasks_solo_long_b.txt ]] && mv tasks_solo_long_b.txt tasks/
rm -f harness.py detector.py topology.py notebook.py shared_usage.py verify_edges.py experiment_c.py
rm -f run_all.sh run_extra.sh rederive.sh tasks_solo.txt tasks_solo_long.txt tasks_swarm.txt
rm -rf benchmark __pycache__
[[ -f tasks/tasks_solo_long_b.txt ]] || { grep -v '^#' tasks/tasks_solo_long.txt | tail -n 8 > tasks/tasks_solo_long_b.txt; }
echo "layout now:"; ls

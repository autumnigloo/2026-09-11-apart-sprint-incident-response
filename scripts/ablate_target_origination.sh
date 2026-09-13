#!/usr/bin/env bash
# {convergence K} x {target-origination on/off} on both benchmarks, the negative
# sets, and the live swarms. Offline, no API. ~15 minutes.
#   bash scripts/ablate_target_origination.sh 2>&1 | tee logs/ablate_target.log
#
# The headline is the swarm block at the end: the planted benchmark cannot see
# what the convergence filter is for, in the same way it cannot see what the
# origination filter is for (RESULTS.md section 5).
set -uo pipefail
cd "$(dirname "$0")/.."
OUT=${OUT:-data/rederived/ablate_target}
rm -rf "$OUT"; mkdir -p "$OUT"
# the same-task cases ship as results only; re-plant them if that has not been done
ST=data/rederived/cases_sametask
if [[ ! -d $ST ]]; then
  mkdir -p "$ST"
  python code/inject.py data/runs/a0_long --out "$ST" --reps 5 --seed 0 \
    --transforms verbatim,reformatted,truncated >/dev/null 2>"$OUT/inject_sametask.err"
fi

for K in 2 5 0; do
  for TGT in off on; do
    cell="k${K}_tgt${TGT}"
    flag=""; [[ $TGT == on ]] && flag="--target-origination"
    echo "=== $(date +%H:%M:%S) cell $cell"
    python code/score.py data/cases --fixed 0.35 --common-runs "$K" $flag \
      --negatives data/runs/corpus_all data/runs/a0 data/runs/a0_long \
      --out "$OUT/$cell" >"$OUT/$cell.log" 2>&1
    python code/score.py "$ST" --fixed 0.35 --common-runs "$K" $flag \
      --out "$OUT/${cell}_st" >"$OUT/${cell}_st.log" 2>&1
    echo "--- benchmark @0.35:   $(grep -E '^\| 0.35 ' "$OUT/$cell/headline_containment.md" | head -1)"
    echo "--- sametask  @0.35:   $(grep -E '^\| 0.35 ' "$OUT/${cell}_st/headline_containment.md" | head -1)"
    echo "--- negative-set scan (t=0.5/0.7/0.9):"
    grep -E '^\| (data/)?runs/' "$OUT/$cell/headline_containment.md"
    echo "--- attribution:"
    python code/attribution.py data/cases "$OUT/$cell/raw_hits.jsonl" --threshold 0.35
    python code/attribution.py "$ST" "$OUT/${cell}_st/raw_hits.jsonl" --threshold 0.35
    echo
  done
done
echo "=== $(date +%H:%M:%S) live swarms: the test the benchmark cannot run"
echo "    (agents start 45s apart, so a backward edge is physically impossible)"
for d in swarm_directed_explicit swarm_directed_explicit_2; do
  echo "--- $d"
  for K in 2 3 5 0; do
    for TGT in off on; do
      flag=""; [[ $TGT == on ]] && flag="--target-origination"
      python code/detector.py data/runs/$d --threshold 0.35 --common-runs "$K" $flag \
        --out "$OUT/sw_${d}_k${K}_$TGT.json" >/dev/null 2>&1
      printf '    K=%-2s tgt=%-3s  %s\n' "$K" "$TGT" \
        "$(python code/verify_edges.py "$OUT/sw_${d}_k${K}_$TGT.json" | tail -1)"
    done
  done
done
echo "=== $(date +%H:%M:%S) grid done"

#!/usr/bin/env bash
# Re-derives every number in RESULTS.md from the raw transcripts with the code as it is now.
# Offline, deterministic, no API calls (paraphrases come from the cache). ~10 minutes.
#   bash rederive.sh 2>&1 | tee rederive.log
# Nothing under runs/ or benchmark/cases/ is modified. Fresh results go to benchmark/rederived/.
set -uo pipefail
cd "$(dirname "$0")"
OUT=benchmark/rederived; rm -rf "$OUT"; mkdir -p "$OUT"
log() { echo; echo "=== $(date +%H:%M) $*"; }
hdr() { grep -E "^Threshold" "$1" | sed 's/(lowest.*)\. //'; }
row() { grep -E "^\| $2 " "$1" | head -1; }

log "code fingerprint (final versions)"
md5 -q detector.py benchmark/score.py benchmark/inject.py harness.py 2>/dev/null || md5sum detector.py benchmark/score.py benchmark/inject.py harness.py

log "1. re-plant the 400 cases from the raw corpus and compare with the scored cases"
python benchmark/inject.py runs/corpus_all --out "$OUT/cases" --reps 5 --seed 0 >/dev/null 2>"$OUT/inject.err"
cp benchmark/cases/paraphrase_cache.json "$OUT/cases/" 2>/dev/null || true
python3 - <<'PY'
import json
a=[json.loads(l) for l in open("benchmark/cases/labels.jsonl")]
b=[json.loads(l) for l in open("benchmark/rederived/cases/labels.jsonl")]
key=lambda d:(d["case_id"],d["source_run"],d["target_run"],d["source_entry"],d["target_entry"],d["injected_text"])
same=sum(1 for x,y in zip(a,b) if key(x)==key(y))
print(f"cases scored: {len(a)}  re-planted: {len(b)}  identical: {same}")
if same!=len(a): print("MISMATCH: the scored cases differ from a fresh plant; scoring below uses the ORIGINAL cases")
PY

log "2. re-score the original cases with the final detector"
S="benchmark/cases"
python benchmark/score.py $S --fixed 0.35 --negatives runs/corpus_all runs/a0 runs/a0_long --out $OUT/main >/dev/null 2>&1
python benchmark/score.py $S --fixed 0.35 --score jaccard --out $OUT/jaccard >/dev/null 2>&1
python benchmark/score.py $S --fixed 0.35 --no-origination --out $OUT/no_origination >/dev/null 2>&1
python benchmark/score.py $S --fixed 0.35 --common-runs 0 --out $OUT/no_convergence >/dev/null 2>&1
python benchmark/score.py $S --fixed 0.35 --min-evidence 0 --out $OUT/no_floor >/dev/null 2>&1
for k in 3 5 10; do python benchmark/score.py $S --fixed 0.35 --common-runs $k --out $OUT/k$k >/dev/null 2>&1; done

log "3. detector on every run directory"
for d in corpus_all a0 a0_long swarm_unspecified swarm_prohibited swarm_directed swarm_unspecified_gpt41 swarm_prohibited_gpt41 swarm_unspecified_gpt41_impossible; do
  [[ -d runs/$d ]] || { echo "$d: missing"; continue; }
  n=$(python detector.py runs/$d --threshold 0.35 2>/dev/null | grep -o "^[0-9]* hits" | head -1)
  echo "$d: $n at 0.35 ($(python shared_usage.py runs/$d 2>/dev/null | tail -1 | grep -o '[0-9]* commands' || echo 'n/a'))"
done
for d in swarm_directed_explicit swarm_directed_explicit_2; do
  [[ -d runs/$d ]] || continue
  python detector.py runs/$d --threshold 0.35 --out $OUT/$d.json >/dev/null 2>&1
  python detector.py runs/$d --threshold 0.35 --no-origination --out $OUT/${d}_noorig.json >/dev/null 2>&1
  echo "$d: $(python verify_edges.py $OUT/$d.json | tail -1)"
  echo "$d without origination: $(python verify_edges.py $OUT/${d}_noorig.json | tail -1)"
  python topology.py $OUT/$d.json | python3 -c "import json,sys;d=json.load(sys.stdin);print('   label',d['label'],'broadcasters',d['broadcasters'])"
done

log "4. NUMBERS to compare with RESULTS.md"
echo "-- main (containment, K=2, floor 40):"; hdr $OUT/main/headline_containment.md; row $OUT/main/headline_containment.md 0.35; row $OUT/main/headline_containment.md 0.2; row $OUT/main/headline_containment.md 0.7
echo "   verbatim prose at 0.35:"; grep -A4 "verbatim: recall at fixed t=0.35" $OUT/main/headline_containment.md | tail -1
grep -A4 "Negative-set" $OUT/main/headline_containment.md | tail -3
echo "-- jaccard:"; hdr $OUT/jaccard/headline_jaccard.md; row $OUT/jaccard/headline_jaccard.md 0.1; row $OUT/jaccard/headline_jaccard.md 0.7
echo "-- no origination:"; hdr $OUT/no_origination/headline_containment.md
echo "-- no convergence:"; hdr $OUT/no_convergence/headline_containment.md; row $OUT/no_convergence/headline_containment.md 0.35
echo "-- no floor:"; row $OUT/no_floor/headline_containment.md 0.35; grep -A4 "verbatim: recall at fixed t=0.35" $OUT/no_floor/headline_containment.md | tail -1
for k in 3 5 10; do echo "-- K=$k:"; row $OUT/k$k/headline_containment.md 0.35; grep -A4 "verbatim: recall at fixed t=0.35" $OUT/k$k/headline_containment.md | tail -1; done
echo "-- originated-fraction bands (main):"; grep -A6 "originated fraction" $OUT/main/headline_containment.md | tail -4
log "done. compare against RESULTS.md; paste this log back if anything differs."

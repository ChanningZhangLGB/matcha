#!/usr/bin/env bash
# Backfill GLAD and MACE into the four text sweeps that were launched without them.
#
#   bash results/utils/run_glad_mace_backfill.sh
#
# WHY THE FULL 8 AND NOT JUST THE TWO MISSING ONES. build_routing.py opens its output
# with mode "w" -- a run restricted to --methods GLAD,MACE would REPLACE routing.csv
# with a two-method file and destroy the six already computed. Re-running all eight is
# the safe form, and nearly free: the six fast methods total ~157 s per file against
# hours for GLAD+MACE.
#
# Back up results/*/allocation/**/routing.csv before running. The existing files are
# overwritten in place and there is no git here.
#
# CONCURRENCY. Each worker is given OMP_NUM_THREADS=3 and MAX_PAR workers run at once,
# so the job occupies about 3*MAX_PAR cores and leaves the rest of the box free. The
# aggregators are numpy-bound, so without the thread cap each process grabs all cores
# and the workers fight each other.
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1

DATASETS=(sentiment movie_reviews conll_ner_5k pico_5k)
MODELS=(gpt-4o-mini llama3.1-8b-instruct-q8_0 qwen2.5-7b-instruct-q8_0)
ROUTES=(human_only human_plus_llm)
ALL_METHODS="MajorityVote,Wawa,DawidSkene,OneCoinDawidSkene,ZeroBasedSkill,MMSR,GLAD,MACE"
MAX_PAR="${MAX_PAR:-6}"
export OMP_NUM_THREADS=3 OPENBLAS_NUM_THREADS=3 MKL_NUM_THREADS=3

LOG="${TMPDIR:-/tmp}/glad_mace_backfill"
mkdir -p "$LOG"

have8() {                       # $1 = routing.csv ; already contains GLAD and MACE?
  [ -f "$1" ] || return 1
  grep -q ",GLAD," "$1" && grep -q ",MACE," "$1"
}

jobs_run=0
for DS in "${DATASETS[@]}"; do
  for M in "${MODELS[@]}"; do
    for R in "${ROUTES[@]}"; do
      D="results/${DS}"; [ "$DS" = movie_reviews ] && D="${D}/categorical"
      # skip only if every measure file for this cell already has all 8
      done_all=1
      for ME in confidence entropy inter_rater random; do
        have8 "${D}/allocation/${M}/${ME}/${R}/routing.csv" || { done_all=0; break; }
      done
      if [ "$done_all" = 1 ]; then
        echo "[skip] ${DS}/${M}/${R} already has GLAD+MACE"
        continue
      fi

      while [ "$(jobs -rp | wc -l)" -ge "$MAX_PAR" ]; do sleep 20; done
      echo "[run ] ${DS}/${M}/${R}"
      (
        "${PYTHON:-python}" results/build_routing.py "$M" \
            --datasets "$DS" --route "$R" \
            --measures confidence,entropy,inter_rater --random \
            --methods "$ALL_METHODS" \
            > "${LOG}/${DS}_${M}_${R}.log" 2>&1
        echo "[done] ${DS}/${M}/${R} rc=$?"
      ) &
      jobs_run=$((jobs_run + 1))
    done
  done
done
wait
echo "BACKFILL_COMPLETE  ${jobs_run} jobs"

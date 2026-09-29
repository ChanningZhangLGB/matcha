#!/usr/bin/env bash
# Full routing sweep for one dataset: 4 uncertainty bases x 2 routes, per model.
#
#   bash results/utils/run_routing_sweep.sh <dataset> [model ...]
#
# build_routing.py does NOT loop over routes -- `--route` takes a single value and
# DEFAULTS to human_only -- and `--random` is an opt-in flag. Invoking it once per
# model therefore silently produces 3 of the 8 required cells. This script supplies
# both routes explicitly and always passes --random, so a complete sweep is:
#
#     {confidence, entropy, inter_rater, random} x {human_only, human_plus_llm} = 8
#
# Cells already COMPLETE are skipped, so this is safe to re-run after an interruption.
# Completeness is judged by the sweep REACHING ITS LAST BUDGET (X=95), not by row
# count: an aggregator that fails to converge at some budget is omitted from that row,
# so a finished cell legitimately holds fewer than 19x8=152 data rows. (Observed:
# MMSR drops out at X=45 on crowdtruth_pooled/gpt-4o-mini/entropy, and at X=40 on
# labelme.) Counting rows would mark those complete files as partial and recompute
# them for ~15 minutes each, every run, forever.
#
# Models run in PARALLEL (each ~4.6 cores, 24 available); measures within a model run
# sequentially inside build_routing.py.
set -uo pipefail
cd "$(dirname "$0")/../.." || exit 1

DS="${1:?usage: run_routing_sweep.sh <dataset> [model ...]}"; shift
MODELS=("$@")
if [ ${#MODELS[@]} -eq 0 ]; then
  MODELS=(gpt-4o-mini llama3.1-8b-instruct-q8_0 qwen2.5-7b-instruct-q8_0)
fi
LAST_X=95           # the final budget in the sweep
LOGDIR="${TMPDIR:-/tmp}/routing_${DS}"
mkdir -p "$LOGDIR"

complete() {                       # $1 = routing.csv path
  [ -f "$1" ] || return 1
  [ "$(tail -1 "$1" | cut -d, -f1)" = "$LAST_X" ]
}

for M in "${MODELS[@]}"; do
(
  for ROUTE in human_only human_plus_llm; do
    NEED=()
    for ME in confidence entropy inter_rater; do
      complete "results/${DS}/allocation/${M}/${ME}/${ROUTE}/routing.csv" || NEED+=("$ME")
    done
    RAND=""
    complete "results/${DS}/allocation/${M}/random/${ROUTE}/routing.csv" || RAND="--random"
    if [ ${#NEED[@]} -eq 0 ] && [ -z "$RAND" ]; then
      echo "[$M/$ROUTE] already complete, skipped"; continue
    fi
    # An EMPTY --measures is deliberate when only `random` is outstanding: build_routing
    # splits it to [""], finds no splits.csv for that name and skips, then still runs
    # the --random block. Substituting a real measure here would recompute a finished
    # cell for ~15 minutes.
    ME_ARG=$(IFS=,; echo "${NEED[*]:-}")
    echo "[$M/$ROUTE] measures=${ME_ARG} ${RAND}"
    "${PYTHON:-python}" results/build_routing.py "$M" \
        --datasets "$DS" --route "$ROUTE" --measures "$ME_ARG" $RAND \
        >> "$LOGDIR/${M}_${ROUTE}.log" 2>&1
  done
  echo "[$M] DONE"
) &
done
wait
echo "SWEEP_COMPLETE $DS"

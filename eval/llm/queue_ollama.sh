#!/usr/bin/env bash
# Queue control + customized runs for one local model.
#
#   eval/llm/queue_ollama.sh <ollama_tag> <short_name>
#
# Waits for any in-flight run of THIS model to finish, then runs the two remaining
# prompt groups. Within a group the five datasets run in parallel; groups run
# sequentially so the GPU is not oversubscribed by 10 jobs at once.
#
# Datasets and sampling are identical to the basic run (temperature 0, top_p 1.0,
# seed 42). Only max_tokens differs, using the budgets learned from the basic run:
#   conll_ner 1400/1800/4000, movie_reviews cot 700, pico topk 2500,
#   and customized/conll_ner 100/400/250 (per-token MCQ emits one letter).
set -u
cd "$(dirname "$0")/../.."

TAG="$1"          # e.g. llama3.1:8b-instruct-q8_0
SHORT="$2"        # e.g. llama31
PY="${PYTHON:-python}"
DATASETS="sentiment movie_reviews crowdtruth conll_ner pico"

echo "[queue:$SHORT] waiting for in-flight basic run to finish..."
while pgrep -f "run_ollama.py $TAG " >/dev/null; do sleep 60; done
echo "[queue:$SHORT] basic finished at $(date '+%F %T')"

for GROUP in control customized; do
  echo "[queue:$SHORT] === starting $GROUP at $(date '+%F %T') ==="
  for DS in $DATASETS; do
    $PY -u eval/llm/run_ollama.py "$TAG" "$DS" --group "$GROUP" --workers 2 \
      > "llm_output/logs/${SHORT}_${GROUP}_${DS}.log" 2>&1 &
  done
  wait
  echo "[queue:$SHORT] === $GROUP complete at $(date '+%F %T') ==="
done
echo "[queue:$SHORT] ALL_GROUPS_COMPLETE $(date '+%F %T')"

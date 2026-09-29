#!/usr/bin/env bash
# Full scoring pipeline for one model, once its generation runs are complete.
#
#   scripts/finalize.sh gpt-4o-mini
#   scripts/finalize.sh qwen2.5-7b-instruct-q8_0
#   scripts/finalize.sh llama3.1-8b-instruct-q8_0
#   scripts/finalize.sh gpt-4o-mini --no-patch     # score released outputs, no model calls
#
# CATEGORICAL track (all 6 datasets)          REGRESSION track (movie_reviews only)
#   1 patch failures                            7 LLM as regressor
#   2 score each prompt group                   8 human + LLM combined
#   3 protocol x strategy table
#   4 majority vote over conditions           BOTH
#   5 per-instance uncertainty                  9 summary tables (categorical
#   6 uncertainty CDF figures                     + regression, rebuilt for all models)
#   6b human + LLM combined aggregation
#
# movie_reviews writes into movie_reviews/categorical/ and movie_reviews/regression/;
# every other dataset has a single framing and writes to its folder directly.
#
# Step 9 rebuilds from whatever exists, so each new model adds its column and earlier
# models are preserved. Steps 6b and 8 are the slow ones (GLAD/MACE re-run per dataset).
set -u
cd "$(dirname "$0")/.."
MODEL="${1:?usage: scripts/finalize.sh <model-dir-name>}"
PY="${PYTHON:-python}"

# Step 1 re-queries the model for unparseable records, so it needs API or Ollama access.
# Skip it with --no-patch when scoring the released outputs: failures are dropped at
# scoring time and the `coverage` column records how many.
if [ "${2:-}" != "--no-patch" ]; then
  echo "### 1. patch failures ($MODEL)"
  $PY eval/llm/patch_failures.py --model "$MODEL" --strip --rerun 2>&1 | tail -3
  $PY eval/llm/patch_failures.py --model "$MODEL" 2>&1 | tail -2
fi

echo "### 2. score each prompt group"
for g in basic_instruction control customized; do
  $PY eval/llm/score_llm.py "$MODEL" --group "$g" 2>/dev/null | sed 's/^/   /'
done

echo "### 3. protocol x prompt-strategy tables"
$PY results/utils/build_model_summary.py "$MODEL"

echo "### 4. majority vote across conditions"
$PY results/utils/build_majority_vote.py "$MODEL"

echo "### 5. per-instance uncertainty"
$PY eval/llm/uncertainty.py "$MODEL"

echo "### 6. uncertainty CDF figures"
$PY results/utils/plot_uncertainty_cdf.py "$MODEL"

echo "### 6b. human + LLM combined aggregation (categorical, slow)"
$PY results/utils/build_combined_aggregation.py "$MODEL" 2>&1 | grep -E "^===|FAILED|^done"

echo "### 7. REGRESSION: LLM as regressor (movie_reviews)"
$PY eval/llm/regression_llm.py "$MODEL"

echo "### 8. REGRESSION: human + LLM combined (movie_reviews)"
$PY eval/llm/combined_regression.py "$MODEL"

echo "### 9. rebuild summary tables (categorical + regression)"
$PY results/utils/build_summary_table.py

echo "### done: $MODEL"

# movie_reviews - regression (continuous framing)

MAE / RMSE lower is better; R2 higher is better. n = 1,498.

## LLM-only

Mean over all 9 conditions (3 prompt groups x 3 protocols) -- the continuous analogue of the categorical 9-condition majority vote.

| model | conditions | MAE | RMSE | R2 |
|---|---|--:|--:|--:|
| gpt-4o-mini | 9 conditions | 0.1098 | 0.1351 | 0.4544 |
| llama3.1-8b | 9 conditions | 0.1033 | 0.1320 | 0.4792 |
| qwen2.5-7b | 9 conditions | 0.1171 | 0.1464 | 0.3598 |

## Human-only (crowd aggregation)

No model column: human-only involves no LLM, so this is a single measurement of the crowd. It applies unchanged wherever the submission table places a human-only column.

| method | MAE | RMSE | R2 |
|---|--:|--:|--:|
| Mean | 0.0607 | 0.0755 | 0.8299 |
| EMBias | 0.0492 | 0.0587 | 0.8969 |

## Crowd-LLM (crowd + LLM as one extra annotator)

| model | method | MAE | RMSE | R2 |
|---|---|--:|--:|--:|
| gpt-4o-mini | Mean | 0.0540 | 0.0672 | 0.8650 |
| gpt-4o-mini | EMBias | 0.0476 | 0.0571 | 0.9027 |
| llama3.1-8b | Mean | 0.0536 | 0.0668 | 0.8668 |
| llama3.1-8b | EMBias | 0.0476 | 0.0571 | 0.9025 |
| qwen2.5-7b | Mean | 0.0573 | 0.0712 | 0.8483 |
| qwen2.5-7b | EMBias | 0.0484 | 0.0578 | 0.9001 |

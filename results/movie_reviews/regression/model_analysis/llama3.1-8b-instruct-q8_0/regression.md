# movie_reviews - llama3.1-8b-instruct-q8_0 as a regressor

The model was asked for a star rating (0-10); the raw number is kept and rescaled to [0,1],
so these sit on the same scale as the human aggregation below.

## LLM

| condition | MAE | RMSE | R2 | r | coverage |
|---|--:|--:|--:|--:|--:|
| **MEAN_of_6_continuous_conditions** | 0.1071 | 0.1347 | 0.4580 | 0.8707 | 100.0% |
| **MEAN_of_all_9_conditions** | 0.1033 | 0.1320 | 0.4792 | 0.8533 | 100.0% |
| basic/cot | 0.0993 | 0.1297 | 0.4972 | 0.8613 | 99.6% |
| basic/topk | 0.1364 | 0.1677 | 0.1601 | 0.8533 | 100.0% |
| basic/vanilla | 0.0975 | 0.1277 | 0.5126 | 0.8655 | 100.0% |
| control/cot | 0.1083 | 0.1441 | 0.3769 | 0.8401 | 99.7% |
| control/topk | 0.1377 | 0.1755 | 0.0791 | 0.8305 | 100.0% |
| control/vanilla | 0.1133 | 0.1515 | 0.3137 | 0.8292 | 100.0% |
| customized/cot | 0.1398 | 0.1959 | -0.1482 | 0.6709 | 99.4% |
| customized/topk | 0.1539 | 0.1945 | -0.1310 | 0.6726 | 100.0% |
| customized/vanilla | 0.1612 | 0.2226 | -0.4807 | 0.6018 | 100.0% |

## Human crowd (same scale)

| method | MAE | RMSE | R2 | r |
|---|--:|--:|--:|--:|
| Mean | 0.0607 | 0.0755 | 0.8299 | 0.9283 |
| EMBias | 0.0492 | 0.0587 | 0.8969 | 0.9672 |
| shipped_DS | 0.0436 | 0.0535 | 0.9143 | 0.9736 |

`customized` answers by picking one of 11 lettered options rather than giving a free number,
so it is listed but kept out of the headline aggregate; the row including it is shown for contrast.

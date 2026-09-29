# movie_reviews - gpt-4o-mini as a regressor

The model was asked for a star rating (0-10); the raw number is kept and rescaled to [0,1],
so these sit on the same scale as the human aggregation below.

## LLM

| condition | MAE | RMSE | R2 | r | coverage |
|---|--:|--:|--:|--:|--:|
| **MEAN_of_6_continuous_conditions** | 0.0949 | 0.1206 | 0.5653 | 0.8788 | 100.0% |
| **MEAN_of_all_9_conditions** | 0.1098 | 0.1351 | 0.4544 | 0.8638 | 100.0% |
| basic/cot | 0.1065 | 0.1382 | 0.4290 | 0.8601 | 99.9% |
| basic/topk | 0.0944 | 0.1258 | 0.5273 | 0.8632 | 100.0% |
| basic/vanilla | 0.0918 | 0.1218 | 0.5564 | 0.8638 | 100.0% |
| control/cot | 0.1075 | 0.1361 | 0.4464 | 0.8720 | 100.0% |
| control/topk | 0.0924 | 0.1216 | 0.5580 | 0.8769 | 100.0% |
| control/vanilla | 0.0912 | 0.1194 | 0.5736 | 0.8746 | 100.0% |
| customized/cot | 0.1485 | 0.1864 | -0.0369 | 0.8157 | 99.6% |
| customized/topk | 0.1828 | 0.2235 | -0.2714 | 0.7681 | 70.0% |
| customized/vanilla | 0.1617 | 0.2027 | -0.2286 | 0.7586 | 99.9% |

## Human crowd (same scale)

| method | MAE | RMSE | R2 | r |
|---|--:|--:|--:|--:|
| Mean | 0.0607 | 0.0755 | 0.8299 | 0.9283 |
| EMBias | 0.0492 | 0.0587 | 0.8969 | 0.9672 |
| shipped_DS | 0.0436 | 0.0535 | 0.9143 | 0.9736 |

`customized` answers by picking one of 11 lettered options rather than giving a free number,
so it is listed but kept out of the headline aggregate; the row including it is shown for contrast.

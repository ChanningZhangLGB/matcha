# movie_reviews - qwen2.5-7b-instruct-q8_0 as a regressor

The model was asked for a star rating (0-10); the raw number is kept and rescaled to [0,1],
so these sit on the same scale as the human aggregation below.

## LLM

| condition | MAE | RMSE | R2 | r | coverage |
|---|--:|--:|--:|--:|--:|
| **MEAN_of_6_continuous_conditions** | 0.1150 | 0.1490 | 0.3363 | 0.8026 | 100.0% |
| **MEAN_of_all_9_conditions** | 0.1171 | 0.1464 | 0.3598 | 0.8290 | 100.0% |
| basic/cot | 0.1124 | 0.1503 | 0.3243 | 0.8028 | 99.9% |
| basic/topk | 0.1261 | 0.1655 | 0.1812 | 0.7425 | 100.0% |
| basic/vanilla | 0.1035 | 0.1440 | 0.3800 | 0.7888 | 100.0% |
| control/cot | 0.1348 | 0.1749 | 0.0856 | 0.7925 | 99.9% |
| control/topk | 0.1341 | 0.1800 | 0.0321 | 0.7556 | 100.0% |
| control/vanilla | 0.1209 | 0.1653 | 0.1839 | 0.7713 | 100.0% |
| customized/cot | 0.1435 | 0.1811 | 0.0190 | 0.7995 | 99.9% |
| customized/topk | 0.1449 | 0.1812 | 0.0188 | 0.7922 | 100.0% |
| customized/vanilla | 0.1584 | 0.1965 | -0.1544 | 0.7863 | 100.0% |

## Human crowd (same scale)

| method | MAE | RMSE | R2 | r |
|---|--:|--:|--:|--:|
| Mean | 0.0607 | 0.0755 | 0.8299 | 0.9283 |
| EMBias | 0.0492 | 0.0587 | 0.8969 | 0.9672 |
| shipped_DS | 0.0436 | 0.0535 | 0.9143 | 0.9736 |

`customized` answers by picking one of 11 lettered options rather than giving a free number,
so it is listed but kept out of the headline aggregate; the row including it is shown for contrast.

# imagenet16h - qwen2.5vl-7b-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6456 | 0.6485 | 0.6438 |
| CoT | 0.6175 | 0.6240 | 0.6275 |
| Top-K | 0.6375 | 0.6377 | 0.6308 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6228 | 0.6267 | 0.6457 |
| CoT | 0.6019 | 0.6122 | 0.6313 |
| Top-K | 0.6130 | 0.6119 | 0.6358 |

**Crowd baseline** (best of 8 aggregators): Wawa accuracy 0.8767, macro-F1 0.8760

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.6523** | **0.6247** | 100.0% |

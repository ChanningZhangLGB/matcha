# labelme - qwen2.5vl-7b-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7750 | 0.7480 | 0.7530 |
| CoT | 0.7480 | 0.7190 | 0.7410 |
| Top-K | 0.7770 | 0.7610 | 0.7500 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7290 | 0.7140 | 0.7212 |
| CoT | 0.7309 | 0.6290 | 0.7356 |
| Top-K | 0.7262 | 0.7135 | 0.7215 |

**Crowd baseline** (best of 8 aggregators): DawidSkene accuracy 0.7920, macro-F1 0.7861

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7600** | **0.7282** | 100.0% |

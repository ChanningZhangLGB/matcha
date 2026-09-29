# labelme - minicpm-v-8b-2.6-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7500 | 0.7470 | 0.7460 |
| CoT | 0.7430 | 0.7510 | 0.7240 |
| Top-K | 0.7490 | 0.7390 | 0.7490 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6273 | 0.6269 | 0.7267 |
| CoT | 0.6465 | 0.6604 | 0.7229 |
| Top-K | 0.6945 | 0.6091 | 0.6549 |

**Crowd baseline** (best of 8 aggregators): DawidSkene accuracy 0.7920, macro-F1 0.7861

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7460** | **0.7132** | 100.0% |

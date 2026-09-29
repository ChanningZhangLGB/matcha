# imagenet16h - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7875 | 0.7419 | 0.7923 |
| CoT | 0.7896 | 0.7892 | 0.7690 |
| Top-K | 0.7917 | 0.7833 | 0.7950 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7544 | 0.7580 | 0.7976 |
| CoT | 0.7454 | 0.7544 | 0.7728 |
| Top-K | 0.7521 | 0.7526 | 0.8004 |

**Crowd baseline** (best of 8 aggregators): Wawa accuracy 0.8767, macro-F1 0.8760

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7973** | **0.7600** | 100.0% |

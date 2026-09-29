# imagenet16h - minicpm-v-8b-2.6-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6042 | 0.5727 | 0.6479 |
| CoT | 0.6212 | 0.6119 | 0.6644 |
| Top-K | 0.6277 | 0.5854 | 0.6498 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6664 | 0.6530 | 0.6743 |
| CoT | 0.6391 | 0.6273 | 0.6681 |
| Top-K | 0.6619 | 0.6586 | 0.6682 |

**Crowd baseline** (best of 8 aggregators): Wawa accuracy 0.8767, macro-F1 0.8760

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.6229** | **0.6733** | 100.0% |

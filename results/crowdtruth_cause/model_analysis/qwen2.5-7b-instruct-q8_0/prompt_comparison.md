# crowdtruth_cause - qwen2.5-7b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7538 | 0.7415 | 0.7549 |
| CoT | 0.7579 | 0.7528 | 0.7549 |
| Top-K | 0.7477 | 0.7426 | 0.7579 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6596 | 0.6326 | 0.5475 |
| CoT | 0.6261 | 0.6100 | 0.5652 |
| Top-K | 0.6562 | 0.6224 | 0.5498 |

**Crowd baseline** (best of 8 aggregators): DawidSkene accuracy 0.7600, macro-F1 0.6065

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7692** | **0.6316** | 100.0% |

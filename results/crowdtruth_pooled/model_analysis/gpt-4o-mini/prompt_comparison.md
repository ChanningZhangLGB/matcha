# crowdtruth_pooled - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7769 | 0.7757 | 0.7632 |
| CoT | 0.7794 | 0.7782 | 0.7845 |
| Top-K | 0.7744 | 0.7801 | 0.7644 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7257 | 0.7376 | 0.6873 |
| CoT | 0.7316 | 0.7403 | 0.7282 |
| Top-K | 0.7184 | 0.7390 | 0.6816 |


## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7845** | **0.7349** | 100.0% |

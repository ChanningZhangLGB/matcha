# crowdtruth_pooled - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7845** | **0.7349** | 100.0% |
| best single condition (`customized/cot`) | 0.7845 | 0.7282 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7794 | 0.7316 | 100.0% |
| basic/topk | 0.7744 | 0.7184 | 100.0% |
| basic/vanilla | 0.7769 | 0.7257 | 100.0% |
| control/cot | 0.7782 | 0.7403 | 100.0% |
| control/topk | 0.7801 | 0.7390 | 100.0% |
| control/vanilla | 0.7757 | 0.7376 | 100.0% |
| customized/cot | 0.7845 | 0.7282 | 100.0% |
| customized/topk | 0.7644 | 0.6816 | 100.0% |
| customized/vanilla | 0.7632 | 0.6873 | 100.0% |

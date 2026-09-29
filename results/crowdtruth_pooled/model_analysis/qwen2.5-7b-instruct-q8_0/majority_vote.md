# crowdtruth_pooled - qwen2.5-7b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7813** | **0.7309** | 100.0% |
| best single condition (`customized/cot`) | 0.7744 | 0.7114 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7719 | 0.7224 | 100.0% |
| basic/topk | 0.7625 | 0.7214 | 100.0% |
| basic/vanilla | 0.7625 | 0.7182 | 100.0% |
| control/cot | 0.7713 | 0.7236 | 100.0% |
| control/topk | 0.7688 | 0.7250 | 100.0% |
| control/vanilla | 0.7600 | 0.7166 | 100.0% |
| customized/cot | 0.7744 | 0.7114 | 100.0% |
| customized/topk | 0.7732 | 0.7098 | 100.0% |
| customized/vanilla | 0.7575 | 0.6786 | 100.0% |

# crowdtruth_cause - qwen2.5-7b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7692** | **0.6316** | 100.0% |
| best single condition (`basic/cot`) | 0.7579 | 0.6261 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7579 | 0.6261 | 100.0% |
| basic/topk | 0.7477 | 0.6562 | 100.0% |
| basic/vanilla | 0.7538 | 0.6596 | 100.0% |
| control/cot | 0.7528 | 0.6100 | 100.0% |
| control/topk | 0.7426 | 0.6224 | 100.0% |
| control/vanilla | 0.7415 | 0.6326 | 100.0% |
| customized/cot | 0.7549 | 0.5652 | 100.0% |
| customized/topk | 0.7579 | 0.5498 | 100.0% |
| customized/vanilla | 0.7549 | 0.5475 | 100.0% |

**Crowd baseline**: DawidSkene accuracy 0.7600, macro-F1 0.6065

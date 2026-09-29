# quiz - qwen2.5-7b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (4 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7355** | **0.6836** | 100.0% |
| best single condition (`control/cot`) | 0.7597 | 0.7092 | 99.4% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7290 | 0.6766 | 100.0% |
| basic/topk | 0.7355 | 0.6838 | 100.0% |
| basic/vanilla | 0.7161 | 0.6686 | 100.0% |
| control/cot | 0.7597 | 0.7092 | 99.4% |
| control/topk | 0.7355 | 0.6624 | 100.0% |
| control/vanilla | 0.7097 | 0.6486 | 100.0% |
| customized/cot | 0.5613 | 0.4572 | 100.0% |
| customized/topk | 0.5871 | 0.4823 | 100.0% |
| customized/vanilla | 0.5935 | 0.4828 | 100.0% |

**Crowd baseline**: MACE accuracy 0.7226, macro-F1 0.7547

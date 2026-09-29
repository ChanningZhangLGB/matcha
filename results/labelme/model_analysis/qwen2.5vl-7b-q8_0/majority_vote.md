# labelme - qwen2.5vl-7b-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (7 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7600** | **0.7282** | 100.0% |
| best single condition (`basic/topk`) | 0.7770 | 0.7262 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7480 | 0.7309 | 100.0% |
| basic/topk | 0.7770 | 0.7262 | 100.0% |
| basic/vanilla | 0.7750 | 0.7290 | 100.0% |
| control/cot | 0.7190 | 0.6290 | 100.0% |
| control/topk | 0.7610 | 0.7135 | 100.0% |
| control/vanilla | 0.7480 | 0.7140 | 100.0% |
| customized/cot | 0.7410 | 0.7356 | 100.0% |
| customized/topk | 0.7500 | 0.7215 | 100.0% |
| customized/vanilla | 0.7530 | 0.7212 | 100.0% |

**Crowd baseline**: DawidSkene accuracy 0.7920, macro-F1 0.7861

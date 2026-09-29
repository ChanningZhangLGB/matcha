# labelme - minicpm-v-8b-2.6-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (7 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7460** | **0.7132** | 100.0% |
| best single condition (`control/cot`) | 0.7510 | 0.6604 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7430 | 0.6465 | 100.0% |
| basic/topk | 0.7490 | 0.6945 | 100.0% |
| basic/vanilla | 0.7500 | 0.6273 | 100.0% |
| control/cot | 0.7510 | 0.6604 | 100.0% |
| control/topk | 0.7390 | 0.6091 | 100.0% |
| control/vanilla | 0.7470 | 0.6269 | 100.0% |
| customized/cot | 0.7240 | 0.7229 | 100.0% |
| customized/topk | 0.7490 | 0.6549 | 100.0% |
| customized/vanilla | 0.7460 | 0.7267 | 100.0% |

**Crowd baseline**: DawidSkene accuracy 0.7920, macro-F1 0.7861

# imagenet16h - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (145 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7973** | **0.7600** | 100.0% |
| best single condition (`customized/topk`) | 0.7950 | 0.8004 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7896 | 0.7454 | 100.0% |
| basic/topk | 0.7917 | 0.7521 | 100.0% |
| basic/vanilla | 0.7875 | 0.7544 | 100.0% |
| control/cot | 0.7892 | 0.7544 | 100.0% |
| control/topk | 0.7833 | 0.7526 | 100.0% |
| control/vanilla | 0.7419 | 0.7580 | 100.0% |
| customized/cot | 0.7690 | 0.7728 | 100.0% |
| customized/topk | 0.7950 | 0.8004 | 100.0% |
| customized/vanilla | 0.7923 | 0.7976 | 100.0% |

**Crowd baseline**: Wawa accuracy 0.8767, macro-F1 0.8760

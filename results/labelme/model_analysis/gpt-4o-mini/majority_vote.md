# labelme - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (4 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.8140** | **0.8117** | 100.0% |
| best single condition (`customized/cot`) | 0.8190 | 0.8214 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.8030 | 0.8005 | 100.0% |
| basic/topk | 0.7940 | 0.7866 | 100.0% |
| basic/vanilla | 0.7960 | 0.7886 | 100.0% |
| control/cot | 0.8120 | 0.8068 | 100.0% |
| control/topk | 0.8130 | 0.8045 | 100.0% |
| control/vanilla | 0.8140 | 0.8081 | 100.0% |
| customized/cot | 0.8190 | 0.8214 | 100.0% |
| customized/topk | 0.8060 | 0.8045 | 100.0% |
| customized/vanilla | 0.8070 | 0.8083 | 100.0% |

**Crowd baseline**: DawidSkene accuracy 0.7920, macro-F1 0.7861

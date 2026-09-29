# quiz - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (2 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.8387** | **0.8651** | 100.0% |
| best single condition (`basic/cot`) | 0.8710 | 0.8883 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.8710 | 0.8883 | 100.0% |
| basic/topk | 0.8258 | 0.8566 | 100.0% |
| basic/vanilla | 0.8452 | 0.8730 | 100.0% |
| control/cot | 0.8581 | 0.8782 | 100.0% |
| control/topk | 0.8323 | 0.8551 | 100.0% |
| control/vanilla | 0.8323 | 0.8581 | 100.0% |
| customized/cot | 0.8129 | 0.7972 | 100.0% |
| customized/topk | 0.8065 | 0.8302 | 100.0% |
| customized/vanilla | 0.8000 | 0.8238 | 100.0% |

**Crowd baseline**: MACE accuracy 0.7226, macro-F1 0.7547

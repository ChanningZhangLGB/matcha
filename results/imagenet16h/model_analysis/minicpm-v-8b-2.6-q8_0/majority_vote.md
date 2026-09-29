# imagenet16h - minicpm-v-8b-2.6-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (115 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.6229** | **0.6733** | 100.0% |
| best single condition (`customized/cot`) | 0.6644 | 0.6681 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.6212 | 0.6391 | 100.0% |
| basic/topk | 0.6277 | 0.6619 | 100.0% |
| basic/vanilla | 0.6042 | 0.6664 | 100.0% |
| control/cot | 0.6119 | 0.6273 | 100.0% |
| control/topk | 0.5854 | 0.6586 | 100.0% |
| control/vanilla | 0.5727 | 0.6530 | 100.0% |
| customized/cot | 0.6644 | 0.6681 | 100.0% |
| customized/topk | 0.6498 | 0.6682 | 100.0% |
| customized/vanilla | 0.6479 | 0.6743 | 100.0% |

**Crowd baseline**: Wawa accuracy 0.8767, macro-F1 0.8760

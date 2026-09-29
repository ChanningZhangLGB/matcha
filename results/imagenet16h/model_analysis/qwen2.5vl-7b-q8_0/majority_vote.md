# imagenet16h - qwen2.5vl-7b-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (135 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.6523** | **0.6247** | 100.0% |
| best single condition (`control/vanilla`) | 0.6485 | 0.6267 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.6175 | 0.6019 | 100.0% |
| basic/topk | 0.6375 | 0.6130 | 100.0% |
| basic/vanilla | 0.6456 | 0.6228 | 100.0% |
| control/cot | 0.6240 | 0.6122 | 100.0% |
| control/topk | 0.6377 | 0.6119 | 100.0% |
| control/vanilla | 0.6485 | 0.6267 | 100.0% |
| customized/cot | 0.6275 | 0.6313 | 100.0% |
| customized/topk | 0.6308 | 0.6358 | 100.0% |
| customized/vanilla | 0.6438 | 0.6457 | 100.0% |

**Crowd baseline**: Wawa accuracy 0.8767, macro-F1 0.8760

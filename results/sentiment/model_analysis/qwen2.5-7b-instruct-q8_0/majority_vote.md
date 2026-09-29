# sentiment - qwen2.5-7b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **12 conditions** vote per instance.
Ties break on the alphabetically-first label (55 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (12 conditions)** | **0.9060** | **0.9059** | 100.0% |
| best single condition (`basic/vanilla`) | 0.9124 | 0.9124 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.9058 | 0.9057 | 100.0% |
| basic/topk | 0.8980 | 0.8977 | 100.0% |
| basic/vanilla | 0.9124 | 0.9124 | 100.0% |
| control/cot | 0.9050 | 0.9049 | 100.0% |
| control/topk | 0.9061 | 0.9061 | 100.0% |
| control/vanilla | 0.9102 | 0.9102 | 100.0% |
| customized/cot[negative] | 0.8487 | 0.8462 | 100.0% |
| customized/cot[positive] | 0.8956 | 0.8956 | 100.0% |
| customized/topk[negative] | 0.8954 | 0.8953 | 100.0% |
| customized/topk[positive] | 0.8794 | 0.8785 | 100.0% |
| customized/vanilla[negative] | 0.8836 | 0.8832 | 100.0% |
| customized/vanilla[positive] | 0.8976 | 0.8975 | 100.0% |

**Crowd baseline**: OneCoinDawidSkene accuracy 0.9166, macro-F1 0.9166

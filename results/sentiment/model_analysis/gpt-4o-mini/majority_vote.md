# sentiment - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **12 conditions** vote per instance.
Ties break on the alphabetically-first label (59 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (12 conditions)** | **0.9012** | **0.9007** | 100.0% |
| best single condition (`control/cot`) | 0.9154 | 0.9152 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.9094 | 0.9093 | 100.0% |
| basic/topk | 0.8950 | 0.8944 | 100.0% |
| basic/vanilla | 0.9056 | 0.9053 | 100.0% |
| control/cot | 0.9154 | 0.9152 | 100.0% |
| control/topk | 0.9012 | 0.9007 | 100.0% |
| control/vanilla | 0.9104 | 0.9101 | 100.0% |
| customized/cot[negative] | 0.8882 | 0.8876 | 100.0% |
| customized/cot[positive] | 0.8924 | 0.8919 | 100.0% |
| customized/topk[negative] | 0.8786 | 0.8777 | 100.0% |
| customized/topk[positive] | 0.8668 | 0.8651 | 100.0% |
| customized/vanilla[negative] | 0.8792 | 0.8784 | 100.0% |
| customized/vanilla[positive] | 0.9024 | 0.9020 | 100.0% |

**Crowd baseline**: OneCoinDawidSkene accuracy 0.9166, macro-F1 0.9166

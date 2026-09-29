# sentiment - llama3.1-8b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **12 conditions** vote per instance.
Ties break on the alphabetically-first label (112 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (12 conditions)** | **0.9068** | **0.9067** | 100.0% |
| best single condition (`control/vanilla`) | 0.9190 | 0.9190 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.8774 | 0.8766 | 100.0% |
| basic/topk | 0.8968 | 0.8965 | 100.0% |
| basic/vanilla | 0.9010 | 0.9009 | 100.0% |
| control/cot | 0.8928 | 0.8924 | 100.0% |
| control/topk | 0.9096 | 0.9094 | 100.0% |
| control/vanilla | 0.9190 | 0.9190 | 100.0% |
| customized/cot[negative] | 0.8392 | 0.8362 | 100.0% |
| customized/cot[positive] | 0.8744 | 0.8742 | 100.0% |
| customized/topk[negative] | 0.8782 | 0.8779 | 100.0% |
| customized/topk[positive] | 0.8620 | 0.8605 | 100.0% |
| customized/vanilla[negative] | 0.8802 | 0.8795 | 100.0% |
| customized/vanilla[positive] | 0.8934 | 0.8932 | 100.0% |

**Crowd baseline**: OneCoinDawidSkene accuracy 0.9166, macro-F1 0.9166

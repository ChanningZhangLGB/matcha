# crowdtruth_treat - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.8052** | **0.8012** | 100.0% |
| best single condition (`control/vanilla`) | 0.8261 | 0.8239 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.8003 | 0.7963 | 100.0% |
| basic/topk | 0.7987 | 0.7938 | 100.0% |
| basic/vanilla | 0.7955 | 0.7900 | 100.0% |
| control/cot | 0.8116 | 0.8093 | 100.0% |
| control/topk | 0.8196 | 0.8174 | 100.0% |
| control/vanilla | 0.8261 | 0.8239 | 100.0% |
| customized/cot | 0.8132 | 0.8089 | 100.0% |
| customized/topk | 0.7810 | 0.7698 | 100.0% |
| customized/vanilla | 0.7842 | 0.7757 | 100.0% |

**Crowd baseline**: GLAD accuracy 0.8293, macro-F1 0.8256

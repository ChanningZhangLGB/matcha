# crowdtruth_treat - qwen2.5-7b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.8003** | **0.7955** | 100.0% |
| best single condition (`control/topk`) | 0.8100 | 0.8062 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7939 | 0.7889 | 100.0% |
| basic/topk | 0.7858 | 0.7789 | 100.0% |
| basic/vanilla | 0.7762 | 0.7675 | 100.0% |
| control/cot | 0.8003 | 0.7975 | 100.0% |
| control/topk | 0.8100 | 0.8062 | 100.0% |
| control/vanilla | 0.7890 | 0.7841 | 100.0% |
| customized/cot | 0.8052 | 0.7998 | 100.0% |
| customized/topk | 0.7971 | 0.7934 | 100.0% |
| customized/vanilla | 0.7617 | 0.7506 | 100.0% |

**Crowd baseline**: GLAD accuracy 0.8293, macro-F1 0.8256

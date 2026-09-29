# crowdtruth_treat - llama3.1-8b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (1 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7810** | **0.7726** | 100.0% |
| best single condition (`customized/topk`) | 0.8454 | 0.8447 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7826 | 0.7763 | 100.0% |
| basic/topk | 0.6940 | 0.6574 | 100.0% |
| basic/vanilla | 0.6940 | 0.6558 | 100.0% |
| control/cot | 0.7681 | 0.7628 | 100.0% |
| control/topk | 0.7520 | 0.7351 | 100.0% |
| control/vanilla | 0.7585 | 0.7428 | 100.0% |
| customized/cot | 0.8145 | 0.8127 | 99.8% |
| customized/topk | 0.8454 | 0.8447 | 100.0% |
| customized/vanilla | 0.8309 | 0.8289 | 100.0% |

**Crowd baseline**: GLAD accuracy 0.8293, macro-F1 0.8256

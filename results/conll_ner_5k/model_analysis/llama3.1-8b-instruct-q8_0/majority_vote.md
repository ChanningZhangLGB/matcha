# conll_ner_5k - llama3.1-8b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (542 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7096** | **0.2386** | 99.1% |
| best single condition (`control/vanilla`) | 0.7999 | 0.3304 | 43.8% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7647 | 0.3789 | 39.8% |
| basic/topk | 0.7088 | 0.3463 | 22.6% |
| basic/vanilla | 0.7911 | 0.3073 | 39.5% |
| control/cot | 0.7895 | 0.3832 | 31.9% |
| control/topk | 0.7292 | 0.2861 | 20.5% |
| control/vanilla | 0.7999 | 0.3304 | 43.8% |
| customized/cot | 0.6366 | 0.2345 | 83.9% |
| customized/topk | 0.2508 | 0.1433 | 31.6% |
| customized/vanilla | 0.7854 | 0.2344 | 92.3% |

**Crowd baseline**: DawidSkene accuracy 0.9418, macro-F1 0.7529

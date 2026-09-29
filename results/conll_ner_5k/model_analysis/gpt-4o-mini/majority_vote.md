# conll_ner_5k - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (91 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.9069** | **0.5418** | 99.9% |
| best single condition (`customized/cot`) | 0.9315 | 0.5896 | 99.6% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.8739 | 0.5872 | 37.3% |
| basic/topk | 0.8145 | 0.4891 | 19.6% |
| basic/vanilla | 0.8550 | 0.5080 | 39.0% |
| control/cot | 0.8907 | 0.6133 | 33.3% |
| control/topk | 0.7985 | 0.4475 | 18.9% |
| control/vanilla | 0.8660 | 0.5628 | 43.1% |
| customized/cot | 0.9315 | 0.5896 | 99.6% |
| customized/topk | 0.8971 | 0.4497 | 94.1% |
| customized/vanilla | 0.9062 | 0.4557 | 96.1% |

**Crowd baseline**: DawidSkene accuracy 0.9418, macro-F1 0.7529

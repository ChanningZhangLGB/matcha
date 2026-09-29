# conll_ner_5k - qwen2.5-7b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (234 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.8377** | **0.3785** | 98.8% |
| best single condition (`basic/cot`) | 0.8662 | 0.5124 | 24.5% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.8662 | 0.5124 | 24.5% |
| basic/topk | 0.7908 | 0.3681 | 30.0% |
| basic/vanilla | 0.8477 | 0.4970 | 33.2% |
| control/cot | 0.8262 | 0.4494 | 27.2% |
| control/topk | 0.7803 | 0.3664 | 32.0% |
| control/vanilla | 0.8011 | 0.3883 | 29.9% |
| customized/cot | 0.6285 | 0.3248 | 38.8% |
| customized/topk | 0.8204 | 0.3145 | 88.9% |
| customized/vanilla | 0.8556 | 0.3228 | 97.9% |

**Crowd baseline**: DawidSkene accuracy 0.9418, macro-F1 0.7529

# crowdtruth_cause - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7713** | **0.6304** | 100.0% |
| best single condition (`basic/cot`) | 0.7662 | 0.6332 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7662 | 0.6332 | 100.0% |
| basic/topk | 0.7590 | 0.5988 | 100.0% |
| basic/vanilla | 0.7651 | 0.6294 | 100.0% |
| control/cot | 0.7569 | 0.6482 | 100.0% |
| control/topk | 0.7549 | 0.6316 | 100.0% |
| control/vanilla | 0.7436 | 0.6307 | 100.0% |
| customized/cot | 0.7662 | 0.5958 | 100.0% |
| customized/topk | 0.7538 | 0.5247 | 100.0% |
| customized/vanilla | 0.7497 | 0.5321 | 100.0% |

**Crowd baseline**: DawidSkene accuracy 0.7600, macro-F1 0.6065

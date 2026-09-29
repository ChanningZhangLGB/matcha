# movie_reviews - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (26 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7483** | **0.7242** | 100.0% |
| best single condition (`basic/vanilla`) | 0.7690 | 0.7449 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7154 | 0.6934 | 99.9% |
| basic/topk | 0.7630 | 0.7394 | 100.0% |
| basic/vanilla | 0.7690 | 0.7449 | 100.0% |
| control/cot | 0.6969 | 0.6793 | 100.0% |
| control/topk | 0.7530 | 0.7314 | 100.0% |
| control/vanilla | 0.7583 | 0.7361 | 100.0% |
| customized/cot | 0.6119 | 0.5948 | 99.6% |
| customized/topk | 0.5939 | 0.5688 | 70.0% |
| customized/vanilla | 0.5929 | 0.5718 | 99.9% |

**Crowd baseline**: ZeroBasedSkill accuracy 0.7924, macro-F1 0.7826

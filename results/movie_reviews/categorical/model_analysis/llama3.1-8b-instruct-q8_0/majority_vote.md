# movie_reviews - llama3.1-8b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (13 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7437** | **0.7172** | 100.0% |
| best single condition (`basic/cot`) | 0.7714 | 0.7474 | 99.6% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7714 | 0.7474 | 99.6% |
| basic/topk | 0.6842 | 0.6581 | 100.0% |
| basic/vanilla | 0.7657 | 0.7410 | 100.0% |
| control/cot | 0.7396 | 0.7120 | 99.7% |
| control/topk | 0.6615 | 0.6411 | 100.0% |
| control/vanilla | 0.7136 | 0.6905 | 100.0% |
| customized/cot | 0.6494 | 0.6297 | 99.4% |
| customized/topk | 0.4927 | 0.4806 | 100.0% |
| customized/vanilla | 0.5694 | 0.5540 | 100.0% |

**Crowd baseline**: ZeroBasedSkill accuracy 0.7924, macro-F1 0.7826

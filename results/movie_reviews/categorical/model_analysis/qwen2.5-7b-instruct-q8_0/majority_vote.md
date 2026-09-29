# movie_reviews - qwen2.5-7b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (7 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.6816** | **0.6589** | 100.0% |
| best single condition (`basic/vanilla`) | 0.7316 | 0.6993 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7206 | 0.6921 | 99.9% |
| basic/topk | 0.6589 | 0.6367 | 100.0% |
| basic/vanilla | 0.7316 | 0.6993 | 100.0% |
| control/cot | 0.6497 | 0.6337 | 99.9% |
| control/topk | 0.6335 | 0.6199 | 100.0% |
| control/vanilla | 0.6756 | 0.6534 | 100.0% |
| customized/cot | 0.6584 | 0.6363 | 99.9% |
| customized/topk | 0.6876 | 0.6678 | 100.0% |
| customized/vanilla | 0.5941 | 0.5842 | 100.0% |

**Crowd baseline**: ZeroBasedSkill accuracy 0.7924, macro-F1 0.7826

# movie_reviews - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7690 | 0.7583 | 0.5929 |
| CoT | 0.7154 | 0.6969 | 0.6119 |
| Top-K | 0.7630 | 0.7530 | 0.5939 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7449 | 0.7361 | 0.5718 |
| CoT | 0.6934 | 0.6793 | 0.5948 |
| Top-K | 0.7394 | 0.7314 | 0.5688 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| customized | cot | 99.6% | 1,492/1,498 |
| customized | topk | 70.0% | 1,049/1,498 |
| customized | vanilla | 99.9% | 1,496/1,498 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill accuracy 0.7924, macro-F1 0.7826

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7483** | **0.7242** | 100.0% |

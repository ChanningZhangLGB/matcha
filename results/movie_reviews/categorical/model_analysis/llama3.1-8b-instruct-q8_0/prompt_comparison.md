# movie_reviews - llama3.1-8b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7657 | 0.7136 | 0.5694 |
| CoT | 0.7714 | 0.7396 | 0.6494 |
| Top-K | 0.6842 | 0.6615 | 0.4927 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7410 | 0.6905 | 0.5540 |
| CoT | 0.7474 | 0.7120 | 0.6297 |
| Top-K | 0.6581 | 0.6411 | 0.4806 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| basic | cot | 99.6% | 1,492/1,498 |
| control | cot | 99.7% | 1,494/1,498 |
| customized | cot | 99.4% | 1,489/1,498 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill accuracy 0.7924, macro-F1 0.7826

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7437** | **0.7172** | 100.0% |

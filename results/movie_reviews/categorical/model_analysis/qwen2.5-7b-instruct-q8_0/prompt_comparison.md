# movie_reviews - qwen2.5-7b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7316 | 0.6756 | 0.5941 |
| CoT | 0.7206 | 0.6497 | 0.6584 |
| Top-K | 0.6589 | 0.6335 | 0.6876 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6993 | 0.6534 | 0.5842 |
| CoT | 0.6921 | 0.6337 | 0.6363 |
| Top-K | 0.6367 | 0.6199 | 0.6678 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| basic | cot | 99.9% | 1,496/1,498 |
| control | cot | 99.9% | 1,496/1,498 |
| customized | cot | 99.9% | 1,496/1,498 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill accuracy 0.7924, macro-F1 0.7826

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.6816** | **0.6589** | 100.0% |

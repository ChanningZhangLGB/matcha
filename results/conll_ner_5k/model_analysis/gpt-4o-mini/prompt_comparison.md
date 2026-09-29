# conll_ner_5k - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.8550 | 0.8660 | 0.9062 |
| CoT | 0.8739 | 0.8907 | 0.9315 |
| Top-K | 0.8145 | 0.7985 | 0.8971 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.5080 | 0.5628 | 0.4557 |
| CoT | 0.5872 | 0.6133 | 0.5896 |
| Top-K | 0.4891 | 0.4475 | 0.4497 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| basic | cot | 37.3% | 1,864/5,001 |
| basic | topk | 19.6% | 981/5,001 |
| basic | vanilla | 39.0% | 1,952/5,001 |
| control | cot | 33.3% | 1,665/5,001 |
| control | topk | 18.9% | 943/5,001 |
| control | vanilla | 43.1% | 2,157/5,001 |
| customized | cot | 99.6% | 4,980/5,001 |
| customized | topk | 94.1% | 4,705/5,001 |
| customized | vanilla | 96.1% | 4,806/5,001 |

**Crowd baseline** (best of 8 aggregators): DawidSkene accuracy 0.9418, macro-F1 0.7529

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.9069** | **0.5418** | 99.9% |

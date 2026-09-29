# conll_ner_5k - qwen2.5-7b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.8477 | 0.8011 | 0.8556 |
| CoT | 0.8662 | 0.8262 | 0.6285 |
| Top-K | 0.7908 | 0.7803 | 0.8204 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.4970 | 0.3883 | 0.3228 |
| CoT | 0.5124 | 0.4494 | 0.3248 |
| Top-K | 0.3681 | 0.3664 | 0.3145 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| basic | cot | 24.5% | 1,226/5,001 |
| basic | topk | 30.0% | 1,501/5,001 |
| basic | vanilla | 33.2% | 1,661/5,001 |
| control | cot | 27.2% | 1,358/5,001 |
| control | topk | 32.0% | 1,602/5,001 |
| control | vanilla | 29.8% | 1,493/5,001 |
| customized | cot | 38.8% | 1,938/5,001 |
| customized | topk | 88.9% | 4,448/5,001 |
| customized | vanilla | 97.9% | 4,895/5,001 |

**Crowd baseline** (best of 8 aggregators): DawidSkene accuracy 0.9418, macro-F1 0.7529

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.8377** | **0.3785** | 98.8% |

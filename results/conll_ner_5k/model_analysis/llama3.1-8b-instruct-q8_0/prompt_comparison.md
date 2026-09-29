# conll_ner_5k - llama3.1-8b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7911 | 0.7999 | 0.7854 |
| CoT | 0.7647 | 0.7895 | 0.6366 |
| Top-K | 0.7088 | 0.7292 | 0.2508 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.3073 | 0.3304 | 0.2344 |
| CoT | 0.3789 | 0.3832 | 0.2345 |
| Top-K | 0.3463 | 0.2861 | 0.1433 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| basic | cot | 39.8% | 1,989/5,001 |
| basic | topk | 22.6% | 1,130/5,001 |
| basic | vanilla | 39.5% | 1,977/5,001 |
| control | cot | 31.9% | 1,596/5,001 |
| control | topk | 20.5% | 1,023/5,001 |
| control | vanilla | 43.8% | 2,189/5,001 |
| customized | cot | 83.9% | 4,194/5,001 |
| customized | topk | 31.6% | 1,579/5,001 |
| customized | vanilla | 92.3% | 4,617/5,001 |

**Crowd baseline** (best of 8 aggregators): DawidSkene accuracy 0.9418, macro-F1 0.7529

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7096** | **0.2386** | 99.1% |

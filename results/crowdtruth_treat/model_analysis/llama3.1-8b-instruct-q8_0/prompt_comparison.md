# crowdtruth_treat - llama3.1-8b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6940 | 0.7585 | 0.8309 |
| CoT | 0.7826 | 0.7681 | 0.8145 |
| Top-K | 0.6940 | 0.7520 | 0.8454 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6558 | 0.7428 | 0.8289 |
| CoT | 0.7763 | 0.7628 | 0.8127 |
| Top-K | 0.6574 | 0.7351 | 0.8447 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| customized | cot | 99.8% | 620/621 |

**Crowd baseline** (best of 8 aggregators): GLAD accuracy 0.8293, macro-F1 0.8256

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7810** | **0.7726** | 100.0% |

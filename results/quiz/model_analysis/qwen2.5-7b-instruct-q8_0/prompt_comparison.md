# quiz - qwen2.5-7b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7161 | 0.7097 | 0.5935 |
| CoT | 0.7290 | 0.7597 | 0.5613 |
| Top-K | 0.7355 | 0.7355 | 0.5871 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6686 | 0.6486 | 0.4828 |
| CoT | 0.6766 | 0.7092 | 0.4572 |
| Top-K | 0.6838 | 0.6624 | 0.4823 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| control | cot | 99.4% | 154/155 |

**Crowd baseline** (best of 8 aggregators): MACE accuracy 0.7226, macro-F1 0.7547

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7355** | **0.6836** | 100.0% |

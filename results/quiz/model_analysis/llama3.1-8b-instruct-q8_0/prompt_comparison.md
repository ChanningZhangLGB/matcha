# quiz - llama3.1-8b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6387 | 0.6387 | 0.4387 |
| CoT | 0.6688 | 0.6000 | 0.4903 |
| Top-K | 0.6323 | 0.6323 | 0.5161 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.5281 | 0.5384 | 0.3548 |
| CoT | 0.5555 | 0.4933 | 0.4355 |
| Top-K | 0.5254 | 0.5265 | 0.4638 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| basic | cot | 99.4% | 154/155 |

**Crowd baseline** (best of 8 aggregators): MACE accuracy 0.7226, macro-F1 0.7547

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.6387** | **0.5323** | 100.0% |

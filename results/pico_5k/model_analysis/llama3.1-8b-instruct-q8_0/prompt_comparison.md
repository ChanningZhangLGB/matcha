# pico_5k - llama3.1-8b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.9019 | 0.8196 | 0.8925 |
| CoT | 0.9050 | 0.8200 | 0.9446 |
| Top-K | 0.8641 | 0.8357 | 0.8984 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6721 | 0.6082 | 0.6722 |
| CoT | 0.6848 | 0.5940 | 0.7452 |
| Top-K | 0.6453 | 0.6194 | 0.6777 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| customized | topk | 96.3% | 4,850/5,034 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill accuracy 0.9615, macro-F1 0.8414

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.9118** | **0.6992** | 100.0% |

# pico_5k - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.9293 | 0.9102 | 0.9331 |
| CoT | 0.9233 | 0.9263 | 0.9271 |
| Top-K | 0.9398 | 0.9413 | 0.9350 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7344 | 0.7139 | 0.7533 |
| CoT | 0.7005 | 0.7507 | 0.7244 |
| Top-K | 0.7071 | 0.7331 | 0.7004 |

## Coverage below 100%

Records the model failed to produce are dropped, so these cells are scored
on a subset - read them alongside the metric, not as equivalent.

| strategy | protocol | coverage | scored |
|---|---|--:|--:|
| control | topk | 97.8% | 4,924/5,034 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill accuracy 0.9615, macro-F1 0.8414

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.9406** | **0.7579** | 100.0% |

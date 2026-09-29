# quiz - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.8452 | 0.8323 | 0.8000 |
| CoT | 0.8710 | 0.8581 | 0.8129 |
| Top-K | 0.8258 | 0.8323 | 0.8065 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.8730 | 0.8581 | 0.8238 |
| CoT | 0.8883 | 0.8782 | 0.7972 |
| Top-K | 0.8566 | 0.8551 | 0.8302 |

**Crowd baseline** (best of 8 aggregators): MACE accuracy 0.7226, macro-F1 0.7547

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.8387** | **0.8651** | 100.0% |

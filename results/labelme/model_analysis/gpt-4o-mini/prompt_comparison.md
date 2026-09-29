# labelme - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7960 | 0.8140 | 0.8070 |
| CoT | 0.8030 | 0.8120 | 0.8190 |
| Top-K | 0.7940 | 0.8130 | 0.8060 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7886 | 0.8081 | 0.8083 |
| CoT | 0.8005 | 0.8068 | 0.8214 |
| Top-K | 0.7866 | 0.8045 | 0.8045 |

**Crowd baseline** (best of 8 aggregators): DawidSkene accuracy 0.7920, macro-F1 0.7861

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.8140** | **0.8117** | 100.0% |

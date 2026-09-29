# crowdtruth_treat - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7955 | 0.8261 | 0.7842 |
| CoT | 0.8003 | 0.8116 | 0.8132 |
| Top-K | 0.7987 | 0.8196 | 0.7810 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7900 | 0.8239 | 0.7757 |
| CoT | 0.7963 | 0.8093 | 0.8089 |
| Top-K | 0.7938 | 0.8174 | 0.7698 |

**Crowd baseline** (best of 8 aggregators): GLAD accuracy 0.8293, macro-F1 0.8256

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.8052** | **0.8012** | 100.0% |

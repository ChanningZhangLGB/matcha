# crowdtruth_treat - qwen2.5-7b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7762 | 0.7890 | 0.7617 |
| CoT | 0.7939 | 0.8003 | 0.8052 |
| Top-K | 0.7858 | 0.8100 | 0.7971 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7675 | 0.7841 | 0.7506 |
| CoT | 0.7889 | 0.7975 | 0.7998 |
| Top-K | 0.7789 | 0.8062 | 0.7934 |

**Crowd baseline** (best of 8 aggregators): GLAD accuracy 0.8293, macro-F1 0.8256

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.8003** | **0.7955** | 100.0% |

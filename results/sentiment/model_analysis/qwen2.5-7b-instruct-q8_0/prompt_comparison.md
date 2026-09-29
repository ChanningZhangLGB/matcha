# sentiment - qwen2.5-7b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.9124 | 0.9102 | 0.8836 / 0.8976 |
| CoT | 0.9058 | 0.9050 | 0.8487 / 0.8956 |
| Top-K | 0.8980 | 0.9061 | 0.8954 / 0.8794 |

*sentiment `customized` is True/False asked twice, counterbalanced;*
*the two values are `assert=negative / assert=positive`.*

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.9124 | 0.9102 | 0.8832 / 0.8975 |
| CoT | 0.9057 | 0.9049 | 0.8462 / 0.8956 |
| Top-K | 0.8977 | 0.9061 | 0.8953 / 0.8785 |

*sentiment `customized` is True/False asked twice, counterbalanced;*
*the two values are `assert=negative / assert=positive`.*

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene accuracy 0.9166, macro-F1 0.9166

## Majority vote across all 12 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.9060** | **0.9059** | 100.0% |

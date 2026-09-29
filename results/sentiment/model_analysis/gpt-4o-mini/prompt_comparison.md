# sentiment - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.9056 | 0.9104 | 0.8792 / 0.9024 |
| CoT | 0.9094 | 0.9154 | 0.8882 / 0.8924 |
| Top-K | 0.8950 | 0.9012 | 0.8786 / 0.8668 |

*sentiment `customized` is True/False asked twice, counterbalanced;*
*the two values are `assert=negative / assert=positive`.*

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.9053 | 0.9101 | 0.8784 / 0.9020 |
| CoT | 0.9093 | 0.9152 | 0.8876 / 0.8919 |
| Top-K | 0.8944 | 0.9007 | 0.8777 / 0.8651 |

*sentiment `customized` is True/False asked twice, counterbalanced;*
*the two values are `assert=negative / assert=positive`.*

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene accuracy 0.9166, macro-F1 0.9166

## Majority vote across all 12 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.9012** | **0.9007** | 100.0% |

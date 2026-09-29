# sentiment - llama3.1-8b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.9010 | 0.9190 | 0.8802 / 0.8934 |
| CoT | 0.8774 | 0.8928 | 0.8392 / 0.8744 |
| Top-K | 0.8968 | 0.9096 | 0.8782 / 0.8620 |

*sentiment `customized` is True/False asked twice, counterbalanced;*
*the two values are `assert=negative / assert=positive`.*

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.9009 | 0.9190 | 0.8795 / 0.8932 |
| CoT | 0.8766 | 0.8924 | 0.8362 / 0.8742 |
| Top-K | 0.8965 | 0.9094 | 0.8779 / 0.8605 |

*sentiment `customized` is True/False asked twice, counterbalanced;*
*the two values are `assert=negative / assert=positive`.*

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene accuracy 0.9166, macro-F1 0.9166

## Majority vote across all 12 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.9068** | **0.9067** | 100.0% |

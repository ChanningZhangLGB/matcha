# crowdtruth_cause - gpt-4o-mini: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7651 | 0.7436 | 0.7497 |
| CoT | 0.7662 | 0.7569 | 0.7662 |
| Top-K | 0.7590 | 0.7549 | 0.7538 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6294 | 0.6307 | 0.5321 |
| CoT | 0.6332 | 0.6482 | 0.5958 |
| Top-K | 0.5988 | 0.6316 | 0.5247 |

**Crowd baseline** (best of 8 aggregators): DawidSkene accuracy 0.7600, macro-F1 0.6065

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7713** | **0.6304** | 100.0% |

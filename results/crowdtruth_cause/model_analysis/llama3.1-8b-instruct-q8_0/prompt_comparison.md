# crowdtruth_cause - llama3.1-8b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.7744 | 0.7497 | 0.6318 |
| CoT | 0.7744 | 0.7641 | 0.7423 |
| Top-K | 0.7692 | 0.7487 | 0.6174 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6187 | 0.6298 | 0.5573 |
| CoT | 0.6331 | 0.6474 | 0.6333 |
| Top-K | 0.5983 | 0.6250 | 0.5489 |

**Crowd baseline** (best of 8 aggregators): DawidSkene accuracy 0.7600, macro-F1 0.6065

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.7579** | **0.6302** | 100.0% |

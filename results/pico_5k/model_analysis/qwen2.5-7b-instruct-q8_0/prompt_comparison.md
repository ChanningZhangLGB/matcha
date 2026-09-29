# pico_5k - qwen2.5-7b-instruct-q8_0: protocol x prompt strategy

Accuracy of the model as a single annotator, scored against ground truth.
`control` = paraphrase; `customized` = the task-fitted manipulation.

## Accuracy

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.9013 | 0.8403 | 0.8683 |
| CoT | 0.8925 | 0.8423 | 0.9058 |
| Top-K | 0.9279 | 0.8802 | 0.9174 |

## Macro-F1

| Protocol | basic | control | customized |
|---|--:|--:|--:|
| Vanilla | 0.6622 | 0.5480 | 0.6201 |
| CoT | 0.6656 | 0.6012 | 0.6586 |
| Top-K | 0.7126 | 0.6234 | 0.6764 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill accuracy 0.9615, macro-F1 0.8414

## Majority vote across all 9 conditions

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| Majority vote | **0.8955** | **0.6437** | 100.0% |

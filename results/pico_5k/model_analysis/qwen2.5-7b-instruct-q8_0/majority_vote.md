# pico_5k - qwen2.5-7b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.8955** | **0.6437** | 100.0% |
| best single condition (`basic/topk`) | 0.9279 | 0.7126 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.8925 | 0.6656 | 100.0% |
| basic/topk | 0.9279 | 0.7126 | 100.0% |
| basic/vanilla | 0.9013 | 0.6622 | 100.0% |
| control/cot | 0.8423 | 0.6012 | 100.0% |
| control/topk | 0.8802 | 0.6234 | 100.0% |
| control/vanilla | 0.8403 | 0.5480 | 100.0% |
| customized/cot | 0.9058 | 0.6586 | 100.0% |
| customized/topk | 0.9174 | 0.6764 | 100.0% |
| customized/vanilla | 0.8683 | 0.6201 | 100.0% |

**Crowd baseline**: ZeroBasedSkill accuracy 0.9615, macro-F1 0.8414

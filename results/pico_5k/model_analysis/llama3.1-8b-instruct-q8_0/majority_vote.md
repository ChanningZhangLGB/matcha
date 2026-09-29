# pico_5k - llama3.1-8b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.9118** | **0.6992** | 100.0% |
| best single condition (`customized/cot`) | 0.9446 | 0.7452 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.9050 | 0.6848 | 100.0% |
| basic/topk | 0.8641 | 0.6453 | 100.0% |
| basic/vanilla | 0.9019 | 0.6721 | 100.0% |
| control/cot | 0.8200 | 0.5940 | 100.0% |
| control/topk | 0.8357 | 0.6194 | 100.0% |
| control/vanilla | 0.8196 | 0.6082 | 100.0% |
| customized/cot | 0.9446 | 0.7452 | 100.0% |
| customized/topk | 0.8984 | 0.6777 | 96.3% |
| customized/vanilla | 0.8925 | 0.6722 | 100.0% |

**Crowd baseline**: ZeroBasedSkill accuracy 0.9615, macro-F1 0.8414

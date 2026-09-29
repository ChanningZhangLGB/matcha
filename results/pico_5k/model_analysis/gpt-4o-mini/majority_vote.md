# pico_5k - gpt-4o-mini: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.9406** | **0.7579** | 100.0% |
| best single condition (`control/topk`) | 0.9413 | 0.7331 | 97.8% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.9233 | 0.7005 | 100.0% |
| basic/topk | 0.9398 | 0.7071 | 100.0% |
| basic/vanilla | 0.9293 | 0.7344 | 100.0% |
| control/cot | 0.9263 | 0.7507 | 100.0% |
| control/topk | 0.9413 | 0.7331 | 97.8% |
| control/vanilla | 0.9102 | 0.7139 | 100.0% |
| customized/cot | 0.9271 | 0.7244 | 100.0% |
| customized/topk | 0.9350 | 0.7004 | 100.0% |
| customized/vanilla | 0.9331 | 0.7533 | 100.0% |

**Crowd baseline**: ZeroBasedSkill accuracy 0.9615, macro-F1 0.8414

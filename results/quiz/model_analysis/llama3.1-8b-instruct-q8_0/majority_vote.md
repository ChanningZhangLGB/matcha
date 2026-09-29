# quiz - llama3.1-8b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (6 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.6387** | **0.5323** | 100.0% |
| best single condition (`basic/cot`) | 0.6688 | 0.5555 | 99.4% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.6688 | 0.5555 | 99.4% |
| basic/topk | 0.6323 | 0.5254 | 100.0% |
| basic/vanilla | 0.6387 | 0.5281 | 100.0% |
| control/cot | 0.6000 | 0.4933 | 100.0% |
| control/topk | 0.6323 | 0.5265 | 100.0% |
| control/vanilla | 0.6387 | 0.5384 | 100.0% |
| customized/cot | 0.4903 | 0.4355 | 100.0% |
| customized/topk | 0.5161 | 0.4638 | 100.0% |
| customized/vanilla | 0.4387 | 0.3548 | 100.0% |

**Crowd baseline**: MACE accuracy 0.7226, macro-F1 0.7547

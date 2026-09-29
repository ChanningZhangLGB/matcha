# crowdtruth_cause - llama3.1-8b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (0 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7579** | **0.6302** | 100.0% |
| best single condition (`basic/cot`) | 0.7744 | 0.6331 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7744 | 0.6331 | 100.0% |
| basic/topk | 0.7692 | 0.5983 | 100.0% |
| basic/vanilla | 0.7744 | 0.6187 | 100.0% |
| control/cot | 0.7641 | 0.6474 | 100.0% |
| control/topk | 0.7487 | 0.6250 | 100.0% |
| control/vanilla | 0.7497 | 0.6298 | 100.0% |
| customized/cot | 0.7423 | 0.6333 | 99.9% |
| customized/topk | 0.6174 | 0.5489 | 100.0% |
| customized/vanilla | 0.6318 | 0.5573 | 100.0% |

**Crowd baseline**: DawidSkene accuracy 0.7600, macro-F1 0.6065

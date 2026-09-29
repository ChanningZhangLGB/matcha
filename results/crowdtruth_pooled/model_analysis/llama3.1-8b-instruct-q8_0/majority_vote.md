# crowdtruth_pooled - llama3.1-8b-instruct-q8_0: majority vote across conditions

Each (protocol x prompt-strategy) pair is one condition; **9 conditions** vote per instance.
Ties break on the alphabetically-first label (1 ties).

| | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| **Majority vote (9 conditions)** | **0.7669** | **0.7130** | 100.0% |
| best single condition (`basic/cot`) | 0.7776 | 0.7229 | 100.0% |

## Conditions that voted

| condition | accuracy | macro-F1 | coverage |
|---|--:|--:|--:|
| basic/cot | 0.7776 | 0.7229 | 100.0% |
| basic/topk | 0.7400 | 0.6407 | 100.0% |
| basic/vanilla | 0.7431 | 0.6479 | 100.0% |
| control/cot | 0.7657 | 0.7184 | 100.0% |
| control/topk | 0.7500 | 0.6868 | 100.0% |
| control/vanilla | 0.7531 | 0.6926 | 100.0% |
| customized/cot | 0.7704 | 0.7337 | 99.9% |
| customized/topk | 0.7061 | 0.6839 | 100.0% |
| customized/vanilla | 0.7093 | 0.6819 | 100.0% |

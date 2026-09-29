# sentiment - llama3.1-8b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-pos | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8928 | 0.8924 | 0.8924 | 0.8987 | 100.0% | 4,999/4,999 | 83 |
| topk | 0.9096 | 0.9094 | 0.9094 | 0.9058 | 100.0% | 4,999/4,999 | 82 |
| vanilla | 0.9190 | 0.9190 | 0.9190 | 0.9195 | 100.0% | 4,999/4,999 | 83 |

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene macro-F1 0.9166
**Best LLM protocol**: vanilla macro-F1 0.9190 (+0.0024 vs crowd)

# quiz - llama3.1-8b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6000 | 0.4933 | 0.5966 | 100.0% | 155/155 | 86 |
| topk | 0.6323 | 0.5265 | 0.6263 | 100.0% | 155/155 | 77 |
| vanilla | 0.6387 | 0.5384 | 0.6378 | 100.0% | 155/155 | 92 |

**Crowd baseline** (best of 8 aggregators): MACE macro-F1 0.7547
**Best LLM protocol**: vanilla macro-F1 0.5384 (-0.2163 vs crowd)

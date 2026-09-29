# quiz - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8581 | 0.8782 | 0.8577 | 100.0% | 155/155 | 92 |
| topk | 0.8323 | 0.8551 | 0.8318 | 100.0% | 155/155 | 80 |
| vanilla | 0.8323 | 0.8581 | 0.8319 | 100.0% | 155/155 | 93 |

**Crowd baseline** (best of 8 aggregators): MACE macro-F1 0.7547
**Best LLM protocol**: cot macro-F1 0.8782 (+0.1236 vs crowd)

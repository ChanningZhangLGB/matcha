# imagenet16h - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7690 | 0.7728 | 0.7728 | 100.0% | 4,800/4,800 | 78 |
| topk | 0.7950 | 0.8004 | 0.8004 | 100.0% | 4,800/4,800 | 74 |
| vanilla | 0.7923 | 0.7976 | 0.7976 | 100.0% | 4,800/4,800 | 74 |

**Crowd baseline** (best of 8 aggregators): Wawa macro-F1 0.8760
**Best LLM protocol**: topk macro-F1 0.8004 (-0.0756 vs crowd)

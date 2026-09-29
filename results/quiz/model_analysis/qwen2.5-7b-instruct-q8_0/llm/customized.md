# quiz - qwen2.5-7b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.5613 | 0.4572 | 0.5690 | 100.0% | 155/155 | 96 |
| topk | 0.5871 | 0.4823 | 0.5853 | 100.0% | 155/155 | 90 |
| vanilla | 0.5935 | 0.4828 | 0.5900 | 100.0% | 155/155 | 95 |

**Crowd baseline** (best of 8 aggregators): MACE macro-F1 0.7547
**Best LLM protocol**: vanilla macro-F1 0.4828 (-0.2718 vs crowd)

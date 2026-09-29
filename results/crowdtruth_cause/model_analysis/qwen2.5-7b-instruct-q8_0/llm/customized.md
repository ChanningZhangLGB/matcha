# crowdtruth_cause - qwen2.5-7b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7549 | 0.5652 | 0.7069 | 0.2779 | 100.0% | 975/975 | 96 |
| topk | 0.7579 | 0.5498 | 0.7008 | 0.2436 | 100.0% | 975/975 | 84 |
| vanilla | 0.7549 | 0.5475 | 0.6986 | 0.2413 | 100.0% | 975/975 | 88 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.6065
**Best LLM protocol**: cot macro-F1 0.5652 (-0.0413 vs crowd)

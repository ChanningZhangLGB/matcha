# crowdtruth_treat - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8003 | 0.7963 | 0.7978 | 0.7678 | 100.0% | 621/621 | 88 |
| topk | 0.7987 | 0.7938 | 0.7955 | 0.7619 | 100.0% | 621/621 | 82 |
| vanilla | 0.7955 | 0.7900 | 0.7918 | 0.7562 | 100.0% | 621/621 | 86 |

**Crowd baseline** (best of 8 aggregators): GLAD macro-F1 0.8256
**Best LLM protocol**: cot macro-F1 0.7963 (-0.0292 vs crowd)

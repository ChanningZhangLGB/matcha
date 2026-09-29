# crowdtruth_cause - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7662 | 0.6332 | 0.7421 | 0.4124 | 100.0% | 975/975 | 88 |
| topk | 0.7590 | 0.5988 | 0.7239 | 0.3454 | 100.0% | 975/975 | 82 |
| vanilla | 0.7651 | 0.6294 | 0.7401 | 0.4052 | 100.0% | 975/975 | 86 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.6065
**Best LLM protocol**: cot macro-F1 0.6332 (+0.0267 vs crowd)

# crowdtruth_cause - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7662 | 0.5958 | 0.7252 | 0.3333 | 100.0% | 975/975 | 88 |
| topk | 0.7538 | 0.5247 | 0.6875 | 0.1946 | 100.0% | 975/975 | 82 |
| vanilla | 0.7497 | 0.5321 | 0.6895 | 0.2129 | 100.0% | 975/975 | 86 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.6065
**Best LLM protocol**: cot macro-F1 0.5958 (-0.0107 vs crowd)

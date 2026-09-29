# crowdtruth_cause - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7569 | 0.6482 | 0.7447 | 0.4527 | 100.0% | 975/975 | 89 |
| topk | 0.7549 | 0.6316 | 0.7367 | 0.4185 | 100.0% | 975/975 | 83 |
| vanilla | 0.7436 | 0.6307 | 0.7314 | 0.4266 | 100.0% | 975/975 | 86 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.6065
**Best LLM protocol**: cot macro-F1 0.6482 (+0.0417 vs crowd)

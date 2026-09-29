# crowdtruth_cause - llama3.1-8b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7744 | 0.6331 | 0.7454 | 0.4054 | 100.0% | 975/975 | 92 |
| topk | 0.7692 | 0.5983 | 0.7276 | 0.3363 | 100.0% | 975/975 | 80 |
| vanilla | 0.7744 | 0.6187 | 0.7389 | 0.3750 | 100.0% | 975/975 | 89 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.6065
**Best LLM protocol**: cot macro-F1 0.6331 (+0.0266 vs crowd)

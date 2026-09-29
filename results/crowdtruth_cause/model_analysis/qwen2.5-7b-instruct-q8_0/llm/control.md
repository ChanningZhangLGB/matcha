# crowdtruth_cause - qwen2.5-7b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7528 | 0.6100 | 0.7264 | 0.3740 | 100.0% | 975/975 | 98 |
| topk | 0.7426 | 0.6224 | 0.7275 | 0.4094 | 100.0% | 975/975 | 85 |
| vanilla | 0.7415 | 0.6326 | 0.7313 | 0.4324 | 100.0% | 975/975 | 91 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.6065
**Best LLM protocol**: vanilla macro-F1 0.6326 (+0.0261 vs crowd)

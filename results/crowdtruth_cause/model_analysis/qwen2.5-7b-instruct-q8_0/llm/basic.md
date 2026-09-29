# crowdtruth_cause - qwen2.5-7b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7579 | 0.6261 | 0.7356 | 0.4040 | 100.0% | 975/975 | 97 |
| topk | 0.7477 | 0.6562 | 0.7437 | 0.4788 | 100.0% | 975/975 | 85 |
| vanilla | 0.7538 | 0.6596 | 0.7480 | 0.4805 | 100.0% | 975/975 | 89 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.6065
**Best LLM protocol**: vanilla macro-F1 0.6596 (+0.0532 vs crowd)

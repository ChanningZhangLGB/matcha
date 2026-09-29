# labelme - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8190 | 0.8214 | 0.8197 | 100.0% | 1,000/1,000 | 90 |
| topk | 0.8060 | 0.8045 | 0.8054 | 100.0% | 1,000/1,000 | 84 |
| vanilla | 0.8070 | 0.8083 | 0.8082 | 100.0% | 1,000/1,000 | 90 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7861
**Best LLM protocol**: cot macro-F1 0.8214 (+0.0353 vs crowd)

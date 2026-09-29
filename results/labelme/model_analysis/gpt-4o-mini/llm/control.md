# labelme - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8120 | 0.8068 | 0.8071 | 100.0% | 1,000/1,000 | 89 |
| topk | 0.8130 | 0.8045 | 0.8043 | 100.0% | 1,000/1,000 | 82 |
| vanilla | 0.8140 | 0.8081 | 0.8093 | 100.0% | 1,000/1,000 | 89 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7861
**Best LLM protocol**: vanilla macro-F1 0.8081 (+0.0220 vs crowd)

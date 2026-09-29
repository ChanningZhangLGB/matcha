# labelme - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8030 | 0.8005 | 0.8025 | 100.0% | 1,000/1,000 | 90 |
| topk | 0.7940 | 0.7866 | 0.7891 | 100.0% | 1,000/1,000 | 84 |
| vanilla | 0.7960 | 0.7886 | 0.7922 | 100.0% | 1,000/1,000 | 90 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7861
**Best LLM protocol**: cot macro-F1 0.8005 (+0.0145 vs crowd)

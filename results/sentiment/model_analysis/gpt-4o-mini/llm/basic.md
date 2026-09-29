# sentiment - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-pos | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9094 | 0.9093 | 0.9093 | 0.9059 | 100.0% | 4,999/4,999 | 89 |
| topk | 0.8950 | 0.8944 | 0.8944 | 0.8869 | 100.0% | 4,999/4,999 | 85 |
| vanilla | 0.9056 | 0.9053 | 0.9053 | 0.8999 | 100.0% | 4,999/4,999 | 90 |

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene macro-F1 0.9166
**Best LLM protocol**: cot macro-F1 0.9093 (-0.0073 vs crowd)

# sentiment - qwen2.5-7b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-pos | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9050 | 0.9049 | 0.9049 | 0.9071 | 100.0% | 4,999/4,999 | 87 |
| topk | 0.9061 | 0.9061 | 0.9061 | 0.9045 | 100.0% | 4,997/4,999 | 83 |
| vanilla | 0.9102 | 0.9102 | 0.9102 | 0.9102 | 100.0% | 4,999/4,999 | 85 |

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene macro-F1 0.9166
**Best LLM protocol**: vanilla macro-F1 0.9102 (-0.0064 vs crowd)

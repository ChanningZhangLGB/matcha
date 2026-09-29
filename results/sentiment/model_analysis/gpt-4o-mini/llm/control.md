# sentiment - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-pos | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9154 | 0.9152 | 0.9152 | 0.9116 | 100.0% | 4,999/4,999 | 89 |
| topk | 0.9012 | 0.9007 | 0.9006 | 0.8934 | 100.0% | 4,999/4,999 | 84 |
| vanilla | 0.9104 | 0.9101 | 0.9101 | 0.9050 | 100.0% | 4,999/4,999 | 89 |

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene macro-F1 0.9166
**Best LLM protocol**: cot macro-F1 0.9152 (-0.0014 vs crowd)

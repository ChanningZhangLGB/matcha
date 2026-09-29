# sentiment - qwen2.5-7b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-pos | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9058 | 0.9057 | 0.9057 | 0.9076 | 100.0% | 4,999/4,999 | 88 |
| topk | 0.8980 | 0.8977 | 0.8977 | 0.8927 | 100.0% | 4,999/4,999 | 85 |
| vanilla | 0.9124 | 0.9124 | 0.9124 | 0.9125 | 100.0% | 4,999/4,999 | 84 |

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene macro-F1 0.9166
**Best LLM protocol**: vanilla macro-F1 0.9124 (-0.0042 vs crowd)

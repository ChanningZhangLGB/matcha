# sentiment - llama3.1-8b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-pos | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8774 | 0.8766 | 0.8766 | 0.8866 | 100.0% | 4,999/4,999 | 84 |
| topk | 0.8968 | 0.8965 | 0.8965 | 0.8912 | 100.0% | 4,999/4,999 | 82 |
| vanilla | 0.9010 | 0.9009 | 0.9009 | 0.9033 | 100.0% | 4,999/4,999 | 86 |

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene macro-F1 0.9166
**Best LLM protocol**: vanilla macro-F1 0.9009 (-0.0157 vs crowd)

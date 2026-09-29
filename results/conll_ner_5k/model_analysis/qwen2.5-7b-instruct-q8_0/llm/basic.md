# conll_ner_5k - qwen2.5-7b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8662 | 0.5124 | 0.8716 | 24.5% | 1,226/5,001 | 86 |
| topk | 0.7908 | 0.3681 | 0.8033 | 30.0% | 1,501/5,001 | 99 |
| vanilla | 0.8477 | 0.4970 | 0.8500 | 33.2% | 1,661/5,001 | 88 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7529
**Best LLM protocol**: cot macro-F1 0.5124 (-0.2406 vs crowd)

**Notes**

- `vanilla`: 163 sentence(s) dropped on tag/token length mismatch
- `cot`: 147 sentence(s) dropped on tag/token length mismatch
- `topk`: 173 sentence(s) dropped on tag/token length mismatch

# conll_ner_5k - qwen2.5-7b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6285 | 0.3248 | 0.6279 | 38.8% | 1,938/5,001 | 100 |
| topk | 0.8204 | 0.3145 | 0.8240 | 88.9% | 4,448/5,001 | 98 |
| vanilla | 0.8556 | 0.3228 | 0.8423 | 97.9% | 4,895/5,001 | 100 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7529
**Best LLM protocol**: cot macro-F1 0.3248 (-0.4281 vs crowd)

**Notes**

- `vanilla`: 106 sentence(s) dropped on tag/token length mismatch
- `cot`: 3063 sentence(s) dropped on tag/token length mismatch
- `topk`: 553 sentence(s) dropped on tag/token length mismatch

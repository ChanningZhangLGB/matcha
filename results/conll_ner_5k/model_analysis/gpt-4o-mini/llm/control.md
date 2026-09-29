# conll_ner_5k - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8907 | 0.6133 | 0.8860 | 33.3% | 1,665/5,001 | 96 |
| topk | 0.7985 | 0.4475 | 0.7903 | 18.9% | 943/5,001 | 92 |
| vanilla | 0.8660 | 0.5628 | 0.8691 | 43.1% | 2,157/5,001 | 96 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7529
**Best LLM protocol**: cot macro-F1 0.6133 (-0.1396 vs crowd)

**Notes**

- `vanilla`: 117 sentence(s) dropped on tag/token length mismatch
- `cot`: 142 sentence(s) dropped on tag/token length mismatch
- `topk`: 210 sentence(s) dropped on tag/token length mismatch

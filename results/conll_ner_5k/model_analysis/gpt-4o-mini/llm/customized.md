# conll_ner_5k - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.9315 | 0.5896 | 0.9237 | 99.6% | 4,980/5,001 | 95 |
| topk | 0.8971 | 0.4497 | 0.8925 | 94.1% | 4,705/5,001 | 88 |
| vanilla | 0.9062 | 0.4557 | 0.9003 | 96.1% | 4,806/5,001 | 95 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7529
**Best LLM protocol**: cot macro-F1 0.5896 (-0.1633 vs crowd)

**Notes**

- `vanilla`: 195 sentence(s) dropped on tag/token length mismatch
- `cot`: 21 sentence(s) dropped on tag/token length mismatch
- `topk`: 296 sentence(s) dropped on tag/token length mismatch

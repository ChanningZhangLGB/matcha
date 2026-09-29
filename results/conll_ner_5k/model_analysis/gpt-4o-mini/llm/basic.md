# conll_ner_5k - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8739 | 0.5872 | 0.8700 | 37.3% | 1,864/5,001 | 97 |
| topk | 0.8145 | 0.4891 | 0.8112 | 19.6% | 981/5,001 | 90 |
| vanilla | 0.8550 | 0.5080 | 0.8620 | 39.0% | 1,952/5,001 | 95 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7529
**Best LLM protocol**: cot macro-F1 0.5872 (-0.1657 vs crowd)

**Notes**

- `vanilla`: 124 sentence(s) dropped on tag/token length mismatch
- `cot`: 132 sentence(s) dropped on tag/token length mismatch
- `topk`: 199 sentence(s) dropped on tag/token length mismatch

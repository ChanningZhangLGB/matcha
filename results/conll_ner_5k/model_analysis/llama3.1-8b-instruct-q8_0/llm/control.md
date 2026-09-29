# conll_ner_5k - llama3.1-8b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7895 | 0.3832 | 0.7983 | 31.9% | 1,596/5,001 | 71 |
| topk | 0.7292 | 0.2861 | 0.7422 | 20.5% | 1,023/5,001 | 96 |
| vanilla | 0.7999 | 0.3304 | 0.8084 | 43.8% | 2,189/5,001 | 98 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7529
**Best LLM protocol**: cot macro-F1 0.3832 (-0.3697 vs crowd)

**Notes**

- `vanilla`: 78 sentence(s) dropped on tag/token length mismatch
- `cot`: 116 sentence(s) dropped on tag/token length mismatch
- `topk`: 105 sentence(s) dropped on tag/token length mismatch

# conll_ner_5k - llama3.1-8b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7647 | 0.3789 | 0.7930 | 39.8% | 1,989/5,001 | 72 |
| topk | 0.7088 | 0.3463 | 0.7180 | 22.6% | 1,130/5,001 | 92 |
| vanilla | 0.7911 | 0.3073 | 0.8094 | 39.5% | 1,977/5,001 | 79 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7529
**Best LLM protocol**: cot macro-F1 0.3789 (-0.3740 vs crowd)

**Notes**

- `vanilla`: 125 sentence(s) dropped on tag/token length mismatch
- `cot`: 93 sentence(s) dropped on tag/token length mismatch
- `topk`: 89 sentence(s) dropped on tag/token length mismatch

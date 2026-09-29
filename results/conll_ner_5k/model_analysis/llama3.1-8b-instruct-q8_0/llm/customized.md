# conll_ner_5k - llama3.1-8b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6366 | 0.2345 | 0.6842 | 83.9% | 4,194/5,001 | 97 |
| topk | 0.2508 | 0.1433 | 0.1571 | 31.6% | 1,579/5,001 | 80 |
| vanilla | 0.7854 | 0.2344 | 0.7851 | 92.3% | 4,617/5,001 | 92 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7529
**Best LLM protocol**: cot macro-F1 0.2345 (-0.5184 vs crowd)

**Notes**

- `vanilla`: 384 sentence(s) dropped on tag/token length mismatch
- `cot`: 806 sentence(s) dropped on tag/token length mismatch
- `topk`: 3421 sentence(s) dropped on tag/token length mismatch

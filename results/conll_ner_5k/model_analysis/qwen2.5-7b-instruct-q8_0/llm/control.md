# conll_ner_5k - qwen2.5-7b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8262 | 0.4494 | 0.8365 | 27.2% | 1,358/5,001 | 83 |
| topk | 0.7803 | 0.3664 | 0.7994 | 32.0% | 1,602/5,001 | 99 |
| vanilla | 0.8011 | 0.3883 | 0.8177 | 29.9% | 1,493/5,001 | 88 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.7529
**Best LLM protocol**: cot macro-F1 0.4494 (-0.3036 vs crowd)

**Notes**

- `vanilla`: 158 sentence(s) dropped on tag/token length mismatch
- `cot`: 144 sentence(s) dropped on tag/token length mismatch
- `topk`: 144 sentence(s) dropped on tag/token length mismatch

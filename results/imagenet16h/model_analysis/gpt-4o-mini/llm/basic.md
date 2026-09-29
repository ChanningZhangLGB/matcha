# imagenet16h - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7896 | 0.7454 | 0.7920 | 100.0% | 4,800/4,800 | 79 |
| topk | 0.7917 | 0.7521 | 0.7991 | 100.0% | 4,800/4,800 | 74 |
| vanilla | 0.7875 | 0.7544 | 0.8016 | 100.0% | 4,800/4,800 | 75 |

**Crowd baseline** (best of 8 aggregators): Wawa macro-F1 0.8760
**Best LLM protocol**: vanilla macro-F1 0.7544 (-0.1215 vs crowd)

**Notes**

- `vanilla`: 110 answer(s) dropped (not a valid category/letter)
- `cot`: 16 answer(s) dropped (not a valid category/letter)
- `topk`: 4 answer(s) dropped (not a valid category/letter)

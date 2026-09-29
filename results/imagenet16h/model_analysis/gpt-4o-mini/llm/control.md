# imagenet16h - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7892 | 0.7544 | 0.8015 | 100.0% | 4,800/4,800 | 80 |
| topk | 0.7833 | 0.7526 | 0.7996 | 100.0% | 4,800/4,800 | 76 |
| vanilla | 0.7419 | 0.7580 | 0.8054 | 100.0% | 4,800/4,800 | 68 |

**Crowd baseline** (best of 8 aggregators): Wawa macro-F1 0.8760
**Best LLM protocol**: vanilla macro-F1 0.7580 (-0.1179 vs crowd)

**Notes**

- `vanilla`: 807 answer(s) dropped (not a valid category/letter)
- `cot`: 114 answer(s) dropped (not a valid category/letter)
- `topk`: 156 answer(s) dropped (not a valid category/letter)

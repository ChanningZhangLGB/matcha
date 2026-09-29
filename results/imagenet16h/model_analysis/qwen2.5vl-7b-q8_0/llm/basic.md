# imagenet16h - qwen2.5vl-7b-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6175 | 0.6019 | 0.6395 | 100.0% | 4,800/4,800 | 75 |
| topk | 0.6375 | 0.6130 | 0.6513 | 100.0% | 4,800/4,800 | 71 |
| vanilla | 0.6456 | 0.6228 | 0.6617 | 100.0% | 4,800/4,800 | 79 |

**Notes**

- `vanilla`: 82 answer(s) dropped (not a valid category/letter)
- `cot`: 339 answer(s) dropped (not a valid category/letter)
- `topk`: 2 answer(s) dropped (not a valid category/letter)

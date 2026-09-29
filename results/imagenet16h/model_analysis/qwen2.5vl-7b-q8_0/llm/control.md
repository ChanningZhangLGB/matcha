# imagenet16h - qwen2.5vl-7b-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6240 | 0.6122 | 0.6505 | 100.0% | 4,800/4,800 | 82 |
| topk | 0.6377 | 0.6119 | 0.6501 | 100.0% | 4,800/4,800 | 73 |
| vanilla | 0.6485 | 0.6267 | 0.6659 | 100.0% | 4,800/4,800 | 82 |

**Notes**

- `vanilla`: 192 answer(s) dropped (not a valid category/letter)
- `cot`: 391 answer(s) dropped (not a valid category/letter)
- `topk`: 1 answer(s) dropped (not a valid category/letter)

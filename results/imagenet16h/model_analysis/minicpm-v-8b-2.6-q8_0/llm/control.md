# imagenet16h - minicpm-v-8b-2.6-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6119 | 0.6273 | 0.6665 | 100.0% | 4,800/4,800 | 71 |
| topk | 0.5854 | 0.6586 | 0.6998 | 100.0% | 4,800/4,800 | 82 |
| vanilla | 0.5727 | 0.6530 | 0.6938 | 100.0% | 4,800/4,800 | 68 |

**Notes**

- `vanilla`: 1796 answer(s) dropped (not a valid category/letter)
- `cot`: 862 answer(s) dropped (not a valid category/letter)
- `topk`: 1685 answer(s) dropped (not a valid category/letter)

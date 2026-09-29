# imagenet16h - minicpm-v-8b-2.6-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6212 | 0.6391 | 0.6790 | 100.0% | 4,800/4,800 | 69 |
| topk | 0.6277 | 0.6619 | 0.7033 | 100.0% | 4,800/4,800 | 71 |
| vanilla | 0.6042 | 0.6664 | 0.7081 | 100.0% | 4,800/4,800 | 67 |

**Notes**

- `vanilla`: 1509 answer(s) dropped (not a valid category/letter)
- `cot`: 905 answer(s) dropped (not a valid category/letter)
- `topk`: 1118 answer(s) dropped (not a valid category/letter)

# labelme - minicpm-v-8b-2.6-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7510 | 0.6604 | 0.7436 | 100.0% | 1,000/1,000 | 88 |
| topk | 0.7390 | 0.6091 | 0.6842 | 100.0% | 1,000/1,000 | 88 |
| vanilla | 0.7470 | 0.6269 | 0.7084 | 100.0% | 1,000/1,000 | 89 |

**Notes**

- `vanilla`: 2 answer(s) dropped (not a valid category/letter)
- `cot`: 6 answer(s) dropped (not a valid category/letter)
- `topk`: 1 answer(s) dropped (not a valid category/letter)

# labelme - minicpm-v-8b-2.6-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7430 | 0.6465 | 0.7311 | 100.0% | 1,000/1,000 | 88 |
| topk | 0.7490 | 0.6945 | 0.6944 | 100.0% | 1,000/1,000 | 90 |
| vanilla | 0.7500 | 0.6273 | 0.7101 | 100.0% | 1,000/1,000 | 89 |

**Notes**

- `vanilla`: 2 answer(s) dropped (not a valid category/letter)
- `cot`: 5 answer(s) dropped (not a valid category/letter)

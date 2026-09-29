# labelme - minicpm-v-8b-2.6-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7240 | 0.7229 | 0.7262 | 100.0% | 1,000/1,000 | 89 |
| topk | 0.7490 | 0.6549 | 0.7399 | 100.0% | 1,000/1,000 | 86 |
| vanilla | 0.7460 | 0.7267 | 0.7313 | 100.0% | 1,000/1,000 | 90 |

**Notes**

- `topk`: 2 answer(s) dropped (not a valid category/letter)

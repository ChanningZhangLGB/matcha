# labelme - qwen2.5vl-7b-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7190 | 0.6290 | 0.7130 | 100.0% | 1,000/1,000 | 90 |
| topk | 0.7610 | 0.7135 | 0.7183 | 100.0% | 1,000/1,000 | 85 |
| vanilla | 0.7480 | 0.7140 | 0.7196 | 100.0% | 1,000/1,000 | 90 |

**Notes**

- `cot`: 1 answer(s) dropped (not a valid category/letter)

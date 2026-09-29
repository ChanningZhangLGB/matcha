# quiz - qwen2.5-7b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7597 | 0.7092 | 0.7617 | 99.4% | 154/155 | 99 |
| topk | 0.7355 | 0.6624 | 0.7334 | 100.0% | 155/155 | 83 |
| vanilla | 0.7097 | 0.6486 | 0.7085 | 100.0% | 155/155 | 100 |

**Crowd baseline** (best of 8 aggregators): MACE macro-F1 0.7547
**Best LLM protocol**: cot macro-F1 0.7092 (-0.0455 vs crowd)

**Notes**

- `cot`: 1 answer(s) dropped (not a valid category/letter)

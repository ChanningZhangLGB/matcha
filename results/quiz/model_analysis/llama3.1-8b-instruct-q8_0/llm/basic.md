# quiz - llama3.1-8b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6688 | 0.5555 | 0.6668 | 99.4% | 154/155 | 86 |
| topk | 0.6323 | 0.5254 | 0.6260 | 100.0% | 155/155 | 78 |
| vanilla | 0.6387 | 0.5281 | 0.6338 | 100.0% | 155/155 | 90 |

**Crowd baseline** (best of 8 aggregators): MACE macro-F1 0.7547
**Best LLM protocol**: cot macro-F1 0.5555 (-0.1992 vs crowd)

**Notes**

- `cot`: 1 answer(s) dropped (not a valid category/letter)

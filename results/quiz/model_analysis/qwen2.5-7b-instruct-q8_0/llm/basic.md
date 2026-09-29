# quiz - qwen2.5-7b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7290 | 0.6766 | 0.7264 | 100.0% | 155/155 | 98 |
| topk | 0.7355 | 0.6838 | 0.7335 | 100.0% | 155/155 | 88 |
| vanilla | 0.7161 | 0.6686 | 0.7144 | 100.0% | 155/155 | 96 |

**Crowd baseline** (best of 8 aggregators): MACE macro-F1 0.7547
**Best LLM protocol**: topk macro-F1 0.6838 (-0.0709 vs crowd)

# quiz - llama3.1-8b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.4903 | 0.4355 | 0.4993 | 100.0% | 155/155 | 91 |
| topk | 0.5161 | 0.4638 | 0.5186 | 100.0% | 155/155 | 84 |
| vanilla | 0.4387 | 0.3548 | 0.4473 | 100.0% | 155/155 | 99 |

**Crowd baseline** (best of 8 aggregators): MACE macro-F1 0.7547
**Best LLM protocol**: topk macro-F1 0.4638 (-0.2909 vs crowd)

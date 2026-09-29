# quiz - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8710 | 0.8883 | 0.8708 | 100.0% | 155/155 | 91 |
| topk | 0.8258 | 0.8566 | 0.8272 | 100.0% | 155/155 | 79 |
| vanilla | 0.8452 | 0.8730 | 0.8464 | 100.0% | 155/155 | 91 |

**Crowd baseline** (best of 8 aggregators): MACE macro-F1 0.7547
**Best LLM protocol**: cot macro-F1 0.8883 (+0.1336 vs crowd)

# quiz - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.8129 | 0.7972 | 0.8158 | 100.0% | 155/155 | 91 |
| topk | 0.8065 | 0.8302 | 0.8074 | 100.0% | 155/155 | 79 |
| vanilla | 0.8000 | 0.8238 | 0.8006 | 100.0% | 155/155 | 90 |

**Crowd baseline** (best of 8 aggregators): MACE macro-F1 0.7547
**Best LLM protocol**: topk macro-F1 0.8302 (+0.0755 vs crowd)

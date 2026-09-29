# pico_5k - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-in | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9271 | 0.7244 | 0.9225 | 0.4881 | 100.0% | 5,034/5,034 | 92 |
| topk | 0.9350 | 0.7004 | 0.9227 | 0.4352 | 100.0% | 5,034/5,034 | 92 |
| vanilla | 0.9331 | 0.7533 | 0.9298 | 0.5427 | 100.0% | 5,034/5,034 | 92 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.8414
**Best LLM protocol**: vanilla macro-F1 0.7533 (-0.0881 vs crowd)

**Notes**

- `topk`: 1/24 spans not found verbatim (dropped)

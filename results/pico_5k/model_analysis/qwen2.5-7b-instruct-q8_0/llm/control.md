# pico_5k - qwen2.5-7b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-in | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8423 | 0.6012 | 0.8611 | 0.2911 | 100.0% | 5,034/5,034 | 100 |
| topk | 0.8802 | 0.6234 | 0.8841 | 0.3124 | 100.0% | 5,034/5,034 | 98 |
| vanilla | 0.8403 | 0.5480 | 0.8527 | 0.1846 | 100.0% | 5,034/5,034 | 100 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.8414
**Best LLM protocol**: topk macro-F1 0.6234 (-0.2180 vs crowd)

**Notes**

- `vanilla`: 3/35 spans not found verbatim (dropped)
- `cot`: 3/30 spans not found verbatim (dropped)
- `topk`: 2/21 spans not found verbatim (dropped)

# pico_5k - qwen2.5-7b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-in | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9058 | 0.6586 | 0.9021 | 0.3680 | 100.0% | 5,034/5,034 | 100 |
| topk | 0.9174 | 0.6764 | 0.9105 | 0.3971 | 100.0% | 5,034/5,034 | 100 |
| vanilla | 0.8683 | 0.6201 | 0.8775 | 0.3130 | 100.0% | 5,034/5,034 | 98 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.8414
**Best LLM protocol**: topk macro-F1 0.6764 (-0.1650 vs crowd)

**Notes**

- `vanilla`: 3/24 spans not found verbatim (dropped)
- `cot`: 1/24 spans not found verbatim (dropped)
- `topk`: 2/24 spans not found verbatim (dropped)

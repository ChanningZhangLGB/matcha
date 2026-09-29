# pico_5k - qwen2.5-7b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-in | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8925 | 0.6656 | 0.8965 | 0.3901 | 100.0% | 5,034/5,034 | 100 |
| topk | 0.9279 | 0.7126 | 0.9211 | 0.4638 | 100.0% | 5,034/5,034 | 95 |
| vanilla | 0.9013 | 0.6622 | 0.9004 | 0.3780 | 100.0% | 5,034/5,034 | 97 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.8414
**Best LLM protocol**: topk macro-F1 0.7126 (-0.1288 vs crowd)

**Notes**

- `vanilla`: 3/53 spans not found verbatim (dropped)
- `cot`: 3/47 spans not found verbatim (dropped)
- `topk`: 1/26 spans not found verbatim (dropped)

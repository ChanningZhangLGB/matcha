# pico_5k - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-in | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9263 | 0.7507 | 0.9261 | 0.5414 | 100.0% | 5,034/5,034 | 92 |
| topk | 0.9413 | 0.7331 | 0.9303 | 0.4974 | 97.8% | 4,924/5,034 | 93 |
| vanilla | 0.9102 | 0.7139 | 0.9126 | 0.4769 | 100.0% | 5,034/5,034 | 94 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.8414
**Best LLM protocol**: cot macro-F1 0.7507 (-0.0907 vs crowd)

**Notes**

- `cot`: 1/53 spans not found verbatim (dropped)

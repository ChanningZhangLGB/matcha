# pico_5k - llama3.1-8b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-in | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9446 | 0.7452 | 0.9341 | 0.5198 | 100.0% | 5,034/5,034 | 100 |
| topk | 0.8984 | 0.6777 | 0.9008 | 0.4110 | 96.3% | 4,850/5,034 | 98 |
| vanilla | 0.8925 | 0.6722 | 0.8975 | 0.4035 | 100.0% | 5,034/5,034 | 100 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.8414
**Best LLM protocol**: cot macro-F1 0.7452 (-0.0962 vs crowd)

**Notes**

- `vanilla`: 3/41 spans not found verbatim (dropped)
- `cot`: 8/36 spans not found verbatim (dropped)
- `topk`: 6/47 spans not found verbatim (dropped)

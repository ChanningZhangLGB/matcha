# pico_5k - llama3.1-8b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-in | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8200 | 0.5940 | 0.8479 | 0.2911 | 100.0% | 5,034/5,034 | 99 |
| topk | 0.8357 | 0.6194 | 0.8599 | 0.3325 | 100.0% | 5,034/5,034 | 91 |
| vanilla | 0.8196 | 0.6082 | 0.8495 | 0.3204 | 100.0% | 5,034/5,034 | 100 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.8414
**Best LLM protocol**: topk macro-F1 0.6194 (-0.2219 vs crowd)

**Notes**

- `vanilla`: 1/56 spans not found verbatim (dropped)
- `cot`: 1/35 spans not found verbatim (dropped)
- `topk`: 3/55 spans not found verbatim (dropped)

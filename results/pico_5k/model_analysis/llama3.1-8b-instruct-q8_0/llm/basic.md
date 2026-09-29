# pico_5k - llama3.1-8b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-in | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9050 | 0.6848 | 0.9057 | 0.4213 | 100.0% | 5,034/5,034 | 100 |
| topk | 0.8641 | 0.6453 | 0.8788 | 0.3667 | 100.0% | 5,034/5,034 | 80 |
| vanilla | 0.9019 | 0.6721 | 0.9022 | 0.3976 | 100.0% | 5,034/5,034 | 100 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.8414
**Best LLM protocol**: cot macro-F1 0.6848 (-0.1566 vs crowd)

**Notes**

- `vanilla`: 4/61 spans not found verbatim (dropped)
- `cot`: 2/43 spans not found verbatim (dropped)
- `topk`: 1/69 spans not found verbatim (dropped)

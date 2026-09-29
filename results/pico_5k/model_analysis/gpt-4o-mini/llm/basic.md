# pico_5k - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-in | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.9233 | 0.7005 | 0.9171 | 0.4422 | 100.0% | 5,034/5,034 | 91 |
| topk | 0.9398 | 0.7071 | 0.9260 | 0.4461 | 100.0% | 5,034/5,034 | 92 |
| vanilla | 0.9293 | 0.7344 | 0.9251 | 0.5069 | 100.0% | 5,034/5,034 | 92 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.8414
**Best LLM protocol**: vanilla macro-F1 0.7344 (-0.1070 vs crowd)

**Notes**

- `cot`: 2/65 spans not found verbatim (dropped)
- `topk`: 1/39 spans not found verbatim (dropped)

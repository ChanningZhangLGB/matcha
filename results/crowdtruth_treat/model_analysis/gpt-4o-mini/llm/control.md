# crowdtruth_treat - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8116 | 0.8093 | 0.8104 | 0.7884 | 100.0% | 621/621 | 89 |
| topk | 0.8196 | 0.8174 | 0.8185 | 0.7971 | 100.0% | 621/621 | 83 |
| vanilla | 0.8261 | 0.8239 | 0.8250 | 0.8043 | 100.0% | 621/621 | 86 |

**Crowd baseline** (best of 8 aggregators): GLAD macro-F1 0.8256
**Best LLM protocol**: vanilla macro-F1 0.8239 (-0.0016 vs crowd)

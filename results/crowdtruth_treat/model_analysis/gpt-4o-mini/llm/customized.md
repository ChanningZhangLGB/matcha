# crowdtruth_treat - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8132 | 0.8089 | 0.8104 | 0.7803 | 100.0% | 621/621 | 88 |
| topk | 0.7810 | 0.7698 | 0.7725 | 0.7190 | 100.0% | 621/621 | 82 |
| vanilla | 0.7842 | 0.7757 | 0.7780 | 0.7320 | 100.0% | 621/621 | 86 |

**Crowd baseline** (best of 8 aggregators): GLAD macro-F1 0.8256
**Best LLM protocol**: cot macro-F1 0.8089 (-0.0166 vs crowd)

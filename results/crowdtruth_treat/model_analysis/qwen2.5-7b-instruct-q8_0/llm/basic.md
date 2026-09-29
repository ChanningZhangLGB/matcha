# crowdtruth_treat - qwen2.5-7b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7939 | 0.7889 | 0.7907 | 0.7567 | 100.0% | 621/621 | 97 |
| topk | 0.7858 | 0.7789 | 0.7810 | 0.7397 | 100.0% | 621/621 | 85 |
| vanilla | 0.7762 | 0.7675 | 0.7699 | 0.7226 | 100.0% | 621/621 | 89 |

**Crowd baseline** (best of 8 aggregators): GLAD macro-F1 0.8256
**Best LLM protocol**: cot macro-F1 0.7889 (-0.0366 vs crowd)

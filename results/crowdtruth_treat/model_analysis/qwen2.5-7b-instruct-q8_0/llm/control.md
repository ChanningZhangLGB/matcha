# crowdtruth_treat - qwen2.5-7b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8003 | 0.7975 | 0.7988 | 0.7737 | 100.0% | 621/621 | 98 |
| topk | 0.8100 | 0.8062 | 0.8076 | 0.7790 | 100.0% | 621/621 | 85 |
| vanilla | 0.7890 | 0.7841 | 0.7858 | 0.7514 | 100.0% | 621/621 | 91 |

**Crowd baseline** (best of 8 aggregators): GLAD macro-F1 0.8256
**Best LLM protocol**: topk macro-F1 0.8062 (-0.0194 vs crowd)

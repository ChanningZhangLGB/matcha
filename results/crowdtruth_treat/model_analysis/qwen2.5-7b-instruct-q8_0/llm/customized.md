# crowdtruth_treat - qwen2.5-7b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8052 | 0.7998 | 0.8015 | 0.7669 | 100.0% | 621/621 | 96 |
| topk | 0.7971 | 0.7934 | 0.7949 | 0.7658 | 100.0% | 621/621 | 84 |
| vanilla | 0.7617 | 0.7506 | 0.7534 | 0.6980 | 100.0% | 621/621 | 88 |

**Crowd baseline** (best of 8 aggregators): GLAD macro-F1 0.8256
**Best LLM protocol**: cot macro-F1 0.7998 (-0.0258 vs crowd)

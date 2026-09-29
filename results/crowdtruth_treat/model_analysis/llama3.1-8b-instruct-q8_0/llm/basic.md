# crowdtruth_treat - llama3.1-8b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7826 | 0.7763 | 0.7783 | 0.7389 | 100.0% | 621/621 | 92 |
| topk | 0.6940 | 0.6574 | 0.6634 | 0.5455 | 100.0% | 621/621 | 80 |
| vanilla | 0.6940 | 0.6558 | 0.6619 | 0.5411 | 100.0% | 621/621 | 89 |

**Crowd baseline** (best of 8 aggregators): GLAD macro-F1 0.8256
**Best LLM protocol**: cot macro-F1 0.7763 (-0.0492 vs crowd)

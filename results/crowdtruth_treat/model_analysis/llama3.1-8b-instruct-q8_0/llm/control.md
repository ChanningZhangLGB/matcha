# crowdtruth_treat - llama3.1-8b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7681 | 0.7628 | 0.7647 | 0.7273 | 100.0% | 621/621 | 92 |
| topk | 0.7520 | 0.7351 | 0.7386 | 0.6681 | 100.0% | 621/621 | 81 |
| vanilla | 0.7585 | 0.7428 | 0.7462 | 0.6795 | 100.0% | 621/621 | 88 |

**Crowd baseline** (best of 8 aggregators): GLAD macro-F1 0.8256
**Best LLM protocol**: cot macro-F1 0.7628 (-0.0628 vs crowd)

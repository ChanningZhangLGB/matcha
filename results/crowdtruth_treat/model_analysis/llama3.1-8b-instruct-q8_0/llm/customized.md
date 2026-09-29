# crowdtruth_treat - llama3.1-8b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.8145 | 0.8127 | 0.8137 | 0.7943 | 99.8% | 620/621 | 92 |
| topk | 0.8454 | 0.8447 | 0.8452 | 0.8339 | 100.0% | 621/621 | 80 |
| vanilla | 0.8309 | 0.8289 | 0.8299 | 0.8101 | 100.0% | 621/621 | 91 |

**Crowd baseline** (best of 8 aggregators): GLAD macro-F1 0.8256
**Best LLM protocol**: topk macro-F1 0.8447 (+0.0191 vs crowd)

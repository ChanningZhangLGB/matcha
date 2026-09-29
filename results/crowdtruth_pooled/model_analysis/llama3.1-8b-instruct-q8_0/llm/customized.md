# crowdtruth_pooled - llama3.1-8b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7704 | 0.7337 | 0.7655 | 0.6347 | 99.9% | 1,594/1,596 | 92 |
| topk | 0.7061 | 0.6839 | 0.7109 | 0.6002 | 100.0% | 1,596/1,596 | 80 |
| vanilla | 0.7093 | 0.6819 | 0.7120 | 0.5887 | 100.0% | 1,596/1,596 | 91 |

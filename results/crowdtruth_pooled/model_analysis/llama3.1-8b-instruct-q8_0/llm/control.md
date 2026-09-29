# crowdtruth_pooled - llama3.1-8b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7657 | 0.7184 | 0.7555 | 0.6030 | 100.0% | 1,596/1,596 | 92 |
| topk | 0.7500 | 0.6868 | 0.7321 | 0.5461 | 100.0% | 1,596/1,596 | 81 |
| vanilla | 0.7531 | 0.6926 | 0.7366 | 0.5563 | 100.0% | 1,596/1,596 | 88 |

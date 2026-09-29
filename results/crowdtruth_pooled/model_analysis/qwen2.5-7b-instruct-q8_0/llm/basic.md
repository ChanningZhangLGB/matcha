# crowdtruth_pooled - qwen2.5-7b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7719 | 0.7224 | 0.7602 | 0.6052 | 100.0% | 1,596/1,596 | 97 |
| topk | 0.7625 | 0.7214 | 0.7559 | 0.6144 | 100.0% | 1,596/1,596 | 85 |
| vanilla | 0.7625 | 0.7182 | 0.7542 | 0.6064 | 100.0% | 1,596/1,596 | 89 |

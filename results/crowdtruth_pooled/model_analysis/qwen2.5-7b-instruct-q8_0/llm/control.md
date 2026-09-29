# crowdtruth_pooled - qwen2.5-7b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7713 | 0.7236 | 0.7606 | 0.6088 | 100.0% | 1,596/1,596 | 98 |
| topk | 0.7688 | 0.7250 | 0.7603 | 0.6152 | 100.0% | 1,596/1,596 | 85 |
| vanilla | 0.7600 | 0.7166 | 0.7523 | 0.6056 | 100.0% | 1,596/1,596 | 91 |

# crowdtruth_pooled - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7794 | 0.7316 | 0.7681 | 0.6182 | 100.0% | 1,596/1,596 | 88 |
| topk | 0.7744 | 0.7184 | 0.7589 | 0.5928 | 100.0% | 1,596/1,596 | 82 |
| vanilla | 0.7769 | 0.7257 | 0.7639 | 0.6071 | 100.0% | 1,596/1,596 | 86 |

# crowdtruth_pooled - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7845 | 0.7282 | 0.7680 | 0.6046 | 100.0% | 1,596/1,596 | 88 |
| topk | 0.7644 | 0.6816 | 0.7339 | 0.5192 | 100.0% | 1,596/1,596 | 82 |
| vanilla | 0.7632 | 0.6873 | 0.7369 | 0.5333 | 100.0% | 1,596/1,596 | 86 |

# crowdtruth_pooled - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7782 | 0.7403 | 0.7722 | 0.6410 | 100.0% | 1,596/1,596 | 89 |
| topk | 0.7801 | 0.7390 | 0.7724 | 0.6355 | 100.0% | 1,596/1,596 | 83 |
| vanilla | 0.7757 | 0.7376 | 0.7698 | 0.6377 | 100.0% | 1,596/1,596 | 86 |

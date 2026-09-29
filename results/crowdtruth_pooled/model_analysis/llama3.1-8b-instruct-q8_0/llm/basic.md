# crowdtruth_pooled - llama3.1-8b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7776 | 0.7229 | 0.7625 | 0.5998 | 100.0% | 1,596/1,596 | 92 |
| topk | 0.7400 | 0.6407 | 0.7015 | 0.4518 | 100.0% | 1,596/1,596 | 80 |
| vanilla | 0.7431 | 0.6479 | 0.7069 | 0.4648 | 100.0% | 1,596/1,596 | 89 |

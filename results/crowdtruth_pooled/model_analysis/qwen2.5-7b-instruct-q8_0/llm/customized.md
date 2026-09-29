# crowdtruth_pooled - qwen2.5-7b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7744 | 0.7114 | 0.7548 | 0.5765 | 100.0% | 1,596/1,596 | 96 |
| topk | 0.7732 | 0.7098 | 0.7535 | 0.5741 | 100.0% | 1,596/1,596 | 84 |
| vanilla | 0.7575 | 0.6786 | 0.7299 | 0.5193 | 100.0% | 1,596/1,596 | 88 |

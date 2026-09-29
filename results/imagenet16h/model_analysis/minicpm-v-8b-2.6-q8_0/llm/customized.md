# imagenet16h - minicpm-v-8b-2.6-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6644 | 0.6681 | 0.6681 | 100.0% | 4,800/4,800 | 71 |
| topk | 0.6498 | 0.6682 | 0.6682 | 100.0% | 4,800/4,800 | 61 |
| vanilla | 0.6479 | 0.6743 | 0.6743 | 100.0% | 4,800/4,800 | 67 |

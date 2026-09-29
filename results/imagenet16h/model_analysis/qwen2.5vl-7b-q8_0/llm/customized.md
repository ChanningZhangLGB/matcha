# imagenet16h - qwen2.5vl-7b-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6275 | 0.6313 | 0.6313 | 100.0% | 4,800/4,800 | 78 |
| topk | 0.6308 | 0.6358 | 0.6358 | 100.0% | 4,800/4,800 | 70 |
| vanilla | 0.6438 | 0.6457 | 0.6457 | 100.0% | 4,800/4,800 | 76 |

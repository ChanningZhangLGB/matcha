# labelme - qwen2.5vl-7b-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7410 | 0.7356 | 0.7386 | 100.0% | 1,000/1,000 | 90 |
| topk | 0.7500 | 0.7215 | 0.7261 | 100.0% | 1,000/1,000 | 88 |
| vanilla | 0.7530 | 0.7212 | 0.7265 | 100.0% | 1,000/1,000 | 89 |

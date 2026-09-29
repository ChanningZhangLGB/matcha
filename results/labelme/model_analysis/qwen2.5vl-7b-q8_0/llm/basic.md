# labelme - qwen2.5vl-7b-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7480 | 0.7309 | 0.7357 | 100.0% | 1,000/1,000 | 89 |
| topk | 0.7770 | 0.7262 | 0.7328 | 100.0% | 1,000/1,000 | 89 |
| vanilla | 0.7750 | 0.7290 | 0.7364 | 100.0% | 1,000/1,000 | 90 |

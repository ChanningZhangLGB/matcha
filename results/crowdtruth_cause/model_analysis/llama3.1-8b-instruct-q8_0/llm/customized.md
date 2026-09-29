# crowdtruth_cause - llama3.1-8b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7423 | 0.6333 | 0.7318 | 0.4334 | 99.9% | 974/975 | 92 |
| topk | 0.6174 | 0.5489 | 0.6356 | 0.3731 | 100.0% | 975/975 | 80 |
| vanilla | 0.6318 | 0.5573 | 0.6469 | 0.3757 | 100.0% | 975/975 | 91 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.6065
**Best LLM protocol**: cot macro-F1 0.6333 (+0.0269 vs crowd)

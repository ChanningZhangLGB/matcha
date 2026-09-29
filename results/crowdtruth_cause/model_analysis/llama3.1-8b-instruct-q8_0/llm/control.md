# crowdtruth_cause - llama3.1-8b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-yes | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot | 0.7641 | 0.6474 | 0.7475 | 0.4444 | 100.0% | 975/975 | 92 |
| topk | 0.7487 | 0.6250 | 0.7313 | 0.4096 | 100.0% | 975/975 | 81 |
| vanilla | 0.7497 | 0.6298 | 0.7337 | 0.4190 | 100.0% | 975/975 | 88 |

**Crowd baseline** (best of 8 aggregators): DawidSkene macro-F1 0.6065
**Best LLM protocol**: cot macro-F1 0.6474 (+0.0409 vs crowd)

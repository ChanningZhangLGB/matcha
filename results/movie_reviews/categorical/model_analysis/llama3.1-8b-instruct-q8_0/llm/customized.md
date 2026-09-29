# movie_reviews - llama3.1-8b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6494 | 0.6297 | 0.6550 | 99.4% | 1,489/1,498 | 81 |
| topk | 0.4927 | 0.4806 | 0.4692 | 100.0% | 1,498/1,498 | 74 |
| vanilla | 0.5694 | 0.5540 | 0.5698 | 100.0% | 1,498/1,498 | 80 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.7826
**Best LLM protocol**: cot macro-F1 0.6297 (-0.1529 vs crowd)

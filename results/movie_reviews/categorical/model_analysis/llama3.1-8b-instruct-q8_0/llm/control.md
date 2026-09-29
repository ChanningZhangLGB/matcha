# movie_reviews - llama3.1-8b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7396 | 0.7120 | 0.7459 | 99.7% | 1,494/1,498 | 81 |
| topk | 0.6615 | 0.6411 | 0.6645 | 100.0% | 1,498/1,498 | 79 |
| vanilla | 0.7136 | 0.6905 | 0.7211 | 100.0% | 1,498/1,498 | 81 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.7826
**Best LLM protocol**: cot macro-F1 0.7120 (-0.0705 vs crowd)

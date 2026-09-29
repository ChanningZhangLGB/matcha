# movie_reviews - qwen2.5-7b-instruct-q8_0 as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6497 | 0.6337 | 0.6624 | 99.9% | 1,496/1,498 | 89 |
| topk | 0.6335 | 0.6199 | 0.6519 | 100.0% | 1,498/1,498 | 49 |
| vanilla | 0.6756 | 0.6534 | 0.6904 | 100.0% | 1,498/1,498 | 84 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.7826
**Best LLM protocol**: vanilla macro-F1 0.6534 (-0.1291 vs crowd)

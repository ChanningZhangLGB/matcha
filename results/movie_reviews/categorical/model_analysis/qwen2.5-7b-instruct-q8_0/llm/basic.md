# movie_reviews - qwen2.5-7b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7206 | 0.6921 | 0.7283 | 99.9% | 1,496/1,498 | 88 |
| topk | 0.6589 | 0.6367 | 0.6587 | 100.0% | 1,498/1,498 | 48 |
| vanilla | 0.7316 | 0.6993 | 0.7407 | 100.0% | 1,498/1,498 | 84 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.7826
**Best LLM protocol**: vanilla macro-F1 0.6993 (-0.0832 vs crowd)

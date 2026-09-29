# movie_reviews - gpt-4o-mini as a single annotator (control prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6969 | 0.6793 | 0.7057 | 100.0% | 1,498/1,498 | 86 |
| topk | 0.7530 | 0.7314 | 0.7590 | 100.0% | 1,498/1,498 | 65 |
| vanilla | 0.7583 | 0.7361 | 0.7631 | 100.0% | 1,498/1,498 | 87 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.7826
**Best LLM protocol**: vanilla macro-F1 0.7361 (-0.0465 vs crowd)

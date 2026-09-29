# movie_reviews - gpt-4o-mini as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7154 | 0.6934 | 0.7218 | 99.9% | 1,497/1,498 | 85 |
| topk | 0.7630 | 0.7394 | 0.7639 | 100.0% | 1,498/1,498 | 62 |
| vanilla | 0.7690 | 0.7449 | 0.7692 | 100.0% | 1,498/1,498 | 85 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.7826
**Best LLM protocol**: vanilla macro-F1 0.7449 (-0.0376 vs crowd)

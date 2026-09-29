# movie_reviews - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6119 | 0.5948 | 0.6156 | 99.6% | 1,492/1,498 | 85 |
| topk | 0.5939 | 0.5688 | 0.5829 | 70.0% | 1,049/1,498 | 69 |
| vanilla | 0.5929 | 0.5718 | 0.5893 | 99.9% | 1,496/1,498 | 85 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.7826
**Best LLM protocol**: cot macro-F1 0.5948 (-0.1877 vs crowd)

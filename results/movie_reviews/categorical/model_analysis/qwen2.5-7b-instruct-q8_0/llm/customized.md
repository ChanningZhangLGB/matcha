# movie_reviews - qwen2.5-7b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.6584 | 0.6363 | 0.6587 | 99.9% | 1,496/1,498 | 90 |
| topk | 0.6876 | 0.6678 | 0.6958 | 100.0% | 1,498/1,498 | 60 |
| vanilla | 0.5941 | 0.5842 | 0.6053 | 100.0% | 1,498/1,498 | 86 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.7826
**Best LLM protocol**: topk macro-F1 0.6678 (-0.1147 vs crowd)

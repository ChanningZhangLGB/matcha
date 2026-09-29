# movie_reviews - llama3.1-8b-instruct-q8_0 as a single annotator (basic prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|
| cot | 0.7714 | 0.7474 | 0.7722 | 99.6% | 1,492/1,498 | 81 |
| topk | 0.6842 | 0.6581 | 0.6786 | 100.0% | 1,498/1,498 | 75 |
| vanilla | 0.7657 | 0.7410 | 0.7654 | 100.0% | 1,498/1,498 | 81 |

**Crowd baseline** (best of 8 aggregators): ZeroBasedSkill macro-F1 0.7826
**Best LLM protocol**: cot macro-F1 0.7474 (-0.0352 vs crowd)

# sentiment - qwen2.5-7b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-pos | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot [assert=negative] | 0.8487 | 0.8462 | 0.8461 | 0.8262 | 100.0% | 4,998/4,999 | 92 |
| cot [assert=positive] | 0.8956 | 0.8956 | 0.8956 | 0.8961 | 100.0% | 4,998/4,999 | 92 |
| topk [assert=negative] | 0.8954 | 0.8953 | 0.8952 | 0.8916 | 100.0% | 4,999/4,999 | 90 |
| topk [assert=positive] | 0.8794 | 0.8785 | 0.8785 | 0.8681 | 100.0% | 4,999/4,999 | 90 |
| vanilla [assert=negative] | 0.8836 | 0.8832 | 0.8832 | 0.8765 | 100.0% | 4,999/4,999 | 91 |
| vanilla [assert=positive] | 0.8976 | 0.8975 | 0.8975 | 0.8941 | 100.0% | 4,999/4,999 | 91 |

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene macro-F1 0.9166
**Best LLM protocol**: vanilla [assert=positive] macro-F1 0.8975 (-0.0191 vs crowd)

**Notes**

- `vanilla [agreement]`: the two framings agree on 93.0% of 4,999 sentences; disagreement is acquiescence bias, not signal
- `cot [agreement]`: the two framings agree on 86.1% of 4,997 sentences; disagreement is acquiescence bias, not signal
- `topk [agreement]`: the two framings agree on 93.8% of 4,999 sentences; disagreement is acquiescence bias, not signal

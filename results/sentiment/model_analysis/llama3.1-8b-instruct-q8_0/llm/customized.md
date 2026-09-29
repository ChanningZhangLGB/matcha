# sentiment - llama3.1-8b-instruct-q8_0 as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-pos | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot [assert=negative] | 0.8392 | 0.8362 | 0.8362 | 0.8142 | 100.0% | 4,999/4,999 | 92 |
| cot [assert=positive] | 0.8744 | 0.8742 | 0.8742 | 0.8789 | 100.0% | 4,999/4,999 | 92 |
| topk [assert=negative] | 0.8782 | 0.8779 | 0.8779 | 0.8719 | 100.0% | 4,999/4,999 | 86 |
| topk [assert=positive] | 0.8620 | 0.8605 | 0.8605 | 0.8463 | 100.0% | 4,999/4,999 | 86 |
| vanilla [assert=negative] | 0.8802 | 0.8795 | 0.8795 | 0.8704 | 100.0% | 4,999/4,999 | 96 |
| vanilla [assert=positive] | 0.8934 | 0.8932 | 0.8932 | 0.8892 | 100.0% | 4,999/4,999 | 96 |

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene macro-F1 0.9166
**Best LLM protocol**: vanilla [assert=positive] macro-F1 0.8932 (-0.0234 vs crowd)

**Notes**

- `vanilla [agreement]`: the two framings agree on 93.0% of 4,999 sentences; disagreement is acquiescence bias, not signal
- `cot [agreement]`: the two framings agree on 82.0% of 4,999 sentences; disagreement is acquiescence bias, not signal
- `topk [agreement]`: the two framings agree on 91.6% of 4,999 sentences; disagreement is acquiescence bias, not signal

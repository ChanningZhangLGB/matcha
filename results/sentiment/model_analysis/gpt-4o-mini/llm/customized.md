# sentiment - gpt-4o-mini as a single annotator (customized prompts)

Scored directly against ground truth, after the same recast applied to the
human labels. Top-K uses its highest-probability guess.

| Protocol | accuracy | macro-f1 | weighted-f1 | f1-pos | coverage | n | mean conf |
|---|--:|--:|--:|--:|--:|--:|--:|
| cot [assert=negative] | 0.8882 | 0.8876 | 0.8876 | 0.8798 | 100.0% | 4,999/4,999 | 91 |
| cot [assert=positive] | 0.8924 | 0.8919 | 0.8919 | 0.8848 | 100.0% | 4,999/4,999 | 91 |
| topk [assert=negative] | 0.8786 | 0.8777 | 0.8777 | 0.8677 | 100.0% | 4,999/4,999 | 81 |
| topk [assert=positive] | 0.8668 | 0.8651 | 0.8651 | 0.8499 | 100.0% | 4,999/4,999 | 81 |
| vanilla [assert=negative] | 0.8792 | 0.8784 | 0.8784 | 0.8686 | 100.0% | 4,999/4,999 | 91 |
| vanilla [assert=positive] | 0.9024 | 0.9020 | 0.9020 | 0.8959 | 100.0% | 4,999/4,999 | 91 |

**Crowd baseline** (best of 8 aggregators): OneCoinDawidSkene macro-F1 0.9166
**Best LLM protocol**: vanilla [assert=positive] macro-F1 0.9020 (-0.0146 vs crowd)

**Notes**

- `vanilla [agreement]`: the two framings agree on 94.4% of 4,999 sentences; disagreement is acquiescence bias, not signal
- `cot [agreement]`: the two framings agree on 94.8% of 4,999 sentences; disagreement is acquiescence bias, not signal
- `topk [agreement]`: the two framings agree on 94.8% of 4,999 sentences; disagreement is acquiescence bias, not signal

# sentiment - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **4,999** sentences |
| Annotators | 203 |
| Judgments | 27,746 (5.55 per instance) |
| Classes | 2 |
| Recast | none - native task/worker/label |
| Ground truth | Pang & Lee polarity label (from review star rating) |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `pos` | 2,502 | 50.1% |
| `neg` | 2,497 | 49.9% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | f1-pos | sec |
|---|--:|--:|--:|--:|--:|
| OneCoinDawidSkene | 0.9166 | 0.9166 | 0.9166 | 0.9169 | 0.7 |
| GLAD | 0.9166 | 0.9166 | 0.9166 | 0.9169 | 46.0 |
| DawidSkene | 0.9152 | 0.9152 | 0.9152 | 0.9149 | 0.6 |
| MACE | 0.9148 | 0.9148 | 0.9148 | 0.9154 | 31.9 |
| MMSR | 0.9008 | 0.9008 | 0.9008 | 0.9022 | 4.3 |
| Wawa | 0.8948 | 0.8947 | 0.8947 | 0.8971 | 0.2 |
| ZeroBasedSkill | 0.8946 | 0.8945 | 0.8945 | 0.8969 | 4.0 |
| MajorityVote | 0.8822 | 0.8820 | 0.8820 | 0.8869 | 0.2 |

**Best:** OneCoinDawidSkene (macro-F1 0.9166)  
**Worst:** MajorityVote (macro-F1 0.8820)  
**Spread:** 0.0346

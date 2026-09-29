# crowdtruth_cause - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **975** sentences |
| Annotators | 304 |
| Judgments | 14,920 (15.30 per instance) |
| Classes | 2 |
| Recast | none - RelEx multi-select reduced to binary [CAUSES] |
| Ground truth | medical expert judgement |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `no` | 728 | 74.7% |
| `yes` | 247 | 25.3% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | f1-yes | sec |
|---|--:|--:|--:|--:|--:|
| DawidSkene | 0.7600 | 0.6065 | 0.7277 | 0.3607 | 0.2 |
| MACE | 0.7692 | 0.5556 | 0.7076 | 0.2475 | 21.0 |
| MMSR | 0.7662 | 0.5533 | 0.7054 | 0.2450 | 8.9 |
| GLAD | 0.7672 | 0.5517 | 0.7050 | 0.2408 | 4.6 |
| MajorityVote | 0.7631 | 0.5462 | 0.7010 | 0.2326 | 0.0 |
| Wawa | 0.7631 | 0.5462 | 0.7010 | 0.2326 | 0.1 |
| ZeroBasedSkill | 0.7631 | 0.5462 | 0.7010 | 0.2326 | 2.6 |
| OneCoinDawidSkene | 0.7651 | 0.5401 | 0.6988 | 0.2184 | 1.9 |

**Best:** DawidSkene (macro-F1 0.6065)  
**Worst:** OneCoinDawidSkene (macro-F1 0.5401)  
**Spread:** 0.0663

> **Accuracy ranks differently.** Top accuracy is MACE (0.7692) while DawidSkene leads macro-F1. With this class balance, accuracy is the misleading metric - report macro-F1.

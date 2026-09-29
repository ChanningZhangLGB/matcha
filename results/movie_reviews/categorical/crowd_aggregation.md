# movie_reviews - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **1,498** reviews |
| Annotators | 135 |
| Judgments | 7,430 (4.96 per instance) |
| Classes | 3 |
| Recast | **bin** - ratings [0,1] -> poor / medium / good |
| Ground truth | the review author's own rating |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `medium` | 741 | 49.5% |
| `good` | 570 | 38.1% |
| `poor` | 187 | 12.5% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | sec |
|---|--:|--:|--:|--:|
| ZeroBasedSkill | 0.7924 | 0.7826 | 0.7953 | 2.2 |
| MACE | 0.7904 | 0.7815 | 0.7931 | 20.6 |
| Wawa | 0.7864 | 0.7765 | 0.7896 | 0.1 |
| OneCoinDawidSkene | 0.7824 | 0.7762 | 0.7819 | 0.3 |
| GLAD | 0.7824 | 0.7730 | 0.7858 | 18.1 |
| DawidSkene | 0.7824 | 0.7680 | 0.7915 | 0.1 |
| MajorityVote | 0.7710 | 0.7598 | 0.7761 | 0.0 |
| MMSR | 0.7417 | 0.7331 | 0.7434 | 1.3 |

**Best:** ZeroBasedSkill (macro-F1 0.7826)  
**Worst:** MMSR (macro-F1 0.7331)  
**Spread:** 0.0494

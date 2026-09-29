# crowdtruth_pooled - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **1,596** sentence-relation pairs |
| Annotators | 304 |
| Judgments | 24,530 (15.37 per instance) |
| Classes | 2 |
| Recast | cause+treat pooled as two binary subtasks; 621 sentences counted twice |
| Ground truth | medical expert judgement |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `no` | 1,055 | 66.1% |
| `yes` | 541 | 33.9% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | f1-yes | sec |
|---|--:|--:|--:|--:|--:|
| DawidSkene | 0.7957 | 0.7495 | 0.7841 | 0.6418 | 0.2 |
| MACE | 0.7876 | 0.7259 | 0.7678 | 0.5959 | 25.5 |
| GLAD | 0.7851 | 0.7192 | 0.7630 | 0.5832 | 14.9 |
| MMSR | 0.7845 | 0.7164 | 0.7611 | 0.5774 | 9.4 |
| OneCoinDawidSkene | 0.7807 | 0.7100 | 0.7561 | 0.5668 | 0.5 |
| MajorityVote | 0.7738 | 0.6997 | 0.7477 | 0.5504 | 0.1 |
| Wawa | 0.7738 | 0.6997 | 0.7477 | 0.5504 | 0.1 |
| ZeroBasedSkill | 0.7738 | 0.6997 | 0.7477 | 0.5504 | 3.1 |

**Best:** DawidSkene (macro-F1 0.7495)  
**Worst:** ZeroBasedSkill (macro-F1 0.6997)  
**Spread:** 0.0498

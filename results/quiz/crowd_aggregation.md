# quiz - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **155** multiple-choice questions (6 subsets pooled) |
| Annotators | 360 |
| Judgments | 8,930 (57.61 per instance) |
| Classes | 6 |
| Recast | none - native task/worker/label; 6 subsets pooled, ids and worker ids namespaced per subset (separate worker pools) |
| Ground truth | the quiz answer key (truth.csv) |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `B` | 39 | 25.2% |
| `D` | 37 | 23.9% |
| `C` | 35 | 22.6% |
| `A` | 23 | 14.8% |
| `E` | 18 | 11.6% |
| `F` | 3 | 1.9% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | sec |
|---|--:|--:|--:|--:|
| MACE | 0.7226 | 0.7547 | 0.7245 | 27.8 |
| OneCoinDawidSkene | 0.6968 | 0.7346 | 0.6990 | 0.9 |
| ZeroBasedSkill | 0.6645 | 0.7078 | 0.6661 | 2.1 |
| Wawa | 0.6581 | 0.6525 | 0.6598 | 0.0 |
| GLAD | 0.6387 | 0.6382 | 0.6401 | 20.4 |
| MMSR | 0.6323 | 0.6084 | 0.6358 | 9.5 |
| MajorityVote | 0.6065 | 0.5894 | 0.6101 | 0.0 |
| DawidSkene | 0.6065 | 0.5542 | 0.6142 | 0.1 |

**Best:** MACE (macro-F1 0.7547)  
**Worst:** DawidSkene (macro-F1 0.5542)  
**Spread:** 0.2005

# imagenet16h - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **4,800** images (16-way object classification; image x noise level) |
| Annotators | 145 |
| Judgments | 28,997 (6.04 per instance) |
| Classes | 16 |
| Recast | none - native task/worker/label; instance unit is (image x phase-noise level), 1,200 x 4 |
| Ground truth | the true ImageNet category |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `bird` | 300 | 6.2% |
| `dog` | 300 | 6.2% |
| `cat` | 300 | 6.2% |
| `bear` | 300 | 6.2% |
| `elephant` | 300 | 6.2% |
| `airplane` | 300 | 6.2% |
| `clock` | 300 | 6.2% |
| `chair` | 300 | 6.2% |
| `car` | 300 | 6.2% |
| `bottle` | 300 | 6.2% |
| `bicycle` | 300 | 6.2% |
| `boat` | 300 | 6.2% |
| `knife` | 300 | 6.2% |
| `keyboard` | 300 | 6.2% |
| `truck` | 300 | 6.2% |
| `oven` | 300 | 6.2% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | sec |
|---|--:|--:|--:|--:|
| Wawa | 0.8767 | 0.8760 | 0.8760 | 0.4 |
| DawidSkene | 0.8760 | 0.8758 | 0.8758 | 0.9 |
| GLAD | 0.8765 | 0.8758 | 0.8758 | 59.0 |
| MACE | 0.8765 | 0.8758 | 0.8758 | 197.9 |
| ZeroBasedSkill | 0.8762 | 0.8755 | 0.8755 | 7.9 |
| OneCoinDawidSkene | 0.8760 | 0.8753 | 0.8753 | 3.4 |
| MMSR | 0.8746 | 0.8739 | 0.8739 | 10.8 |
| MajorityVote | 0.8715 | 0.8706 | 0.8706 | 0.1 |

**Best:** Wawa (macro-F1 0.8760)  
**Worst:** MajorityVote (macro-F1 0.8706)  
**Spread:** 0.0053

# labelme - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **1,000** images (8-way scene classification) |
| Annotators | 59 |
| Judgments | 2,547 (2.55 per instance) |
| Classes | 8 |
| Recast | none - native task/worker/label; 18 all-empty worker columns dropped at melt time |
| Ground truth | the original LabelMe scene class |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `opencountry` | 154 | 15.4% |
| `forest` | 138 | 13.8% |
| `coast` | 134 | 13.4% |
| `tallbuilding` | 131 | 13.1% |
| `mountain` | 128 | 12.8% |
| `insidecity` | 116 | 11.6% |
| `street` | 110 | 11.0% |
| `highway` | 89 | 8.9% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | sec |
|---|--:|--:|--:|--:|
| DawidSkene | 0.7920 | 0.7861 | 0.7856 | 2.2 |
| ZeroBasedSkill | 0.7780 | 0.7739 | 0.7745 | 2.2 |
| GLAD | 0.7750 | 0.7701 | 0.7717 | 5.3 |
| MACE | 0.7730 | 0.7682 | 0.7700 | 44.9 |
| MMSR | 0.7670 | 0.7617 | 0.7634 | 0.4 |
| OneCoinDawidSkene | 0.7670 | 0.7613 | 0.7624 | 0.9 |
| Wawa | 0.7640 | 0.7583 | 0.7594 | 0.1 |
| MajorityVote | 0.7620 | 0.7556 | 0.7561 | 0.0 |

**Best:** DawidSkene (macro-F1 0.7861)  
**Worst:** MajorityVote (macro-F1 0.7556)  
**Spread:** 0.0305

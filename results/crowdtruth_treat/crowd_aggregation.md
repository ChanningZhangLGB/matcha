# crowdtruth_treat - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **621** sentences |
| Annotators | 286 |
| Judgments | 9,610 (15.48 per instance) |
| Classes | 2 |
| Recast | none - RelEx multi-select reduced to binary [TREATS] |
| Ground truth | medical expert judgement |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `no` | 327 | 52.7% |
| `yes` | 294 | 47.3% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | f1-yes | sec |
|---|--:|--:|--:|--:|--:|
| GLAD | 0.8293 | 0.8256 | 0.8269 | 0.8000 | 9.7 |
| DawidSkene | 0.8245 | 0.8219 | 0.8231 | 0.8007 | 0.1 |
| OneCoinDawidSkene | 0.8213 | 0.8161 | 0.8177 | 0.7853 | 0.3 |
| MACE | 0.8180 | 0.8132 | 0.8148 | 0.7831 | 18.1 |
| MMSR | 0.8132 | 0.8066 | 0.8085 | 0.7708 | 7.2 |
| ZeroBasedSkill | 0.8035 | 0.7971 | 0.7990 | 0.7608 | 2.2 |
| Wawa | 0.7987 | 0.7917 | 0.7937 | 0.7535 | 0.1 |
| MajorityVote | 0.7907 | 0.7827 | 0.7849 | 0.7410 | 0.0 |

**Best:** GLAD (macro-F1 0.8256)  
**Worst:** MajorityVote (macro-F1 0.7827)  
**Spread:** 0.0429

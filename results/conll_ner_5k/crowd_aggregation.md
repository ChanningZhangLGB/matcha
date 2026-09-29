# conll_ner_5k - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **5,001** tokens (from 392 sentences) |
| Annotators | 47 |
| Judgments | 23,366 (4.67 per instance) |
| Classes | 9 |
| Recast | **tok** - one task per token; 392 of 5,985 sentences, seed 42 |
| Ground truth | original CoNLL-2003 expert annotation |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `O` | 4,081 | 81.6% |
| `B-PER` | 194 | 3.9% |
| `B-LOC` | 184 | 3.7% |
| `B-ORG` | 166 | 3.3% |
| `I-PER` | 142 | 2.8% |
| `I-ORG` | 89 | 1.8% |
| `B-MISC` | 84 | 1.7% |
| `I-MISC` | 40 | 0.8% |
| `I-LOC` | 21 | 0.4% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | sec |
|---|--:|--:|--:|--:|
| DawidSkene | 0.9418 | 0.7529 | 0.9394 | 0.2 |
| ZeroBasedSkill | 0.9248 | 0.6844 | 0.9157 | 3.6 |
| GLAD | 0.9240 | 0.6825 | 0.9149 | 48.8 |
| Wawa | 0.9234 | 0.6818 | 0.9132 | 0.1 |
| MMSR | 0.9242 | 0.6794 | 0.9150 | 2.5 |
| MACE | 0.9234 | 0.6776 | 0.9135 | 69.8 |
| MajorityVote | 0.9142 | 0.6253 | 0.9003 | 0.1 |
| OneCoinDawidSkene | 0.9108 | 0.5889 | 0.8935 | 0.6 |

**Best:** DawidSkene (macro-F1 0.7529)  
**Worst:** OneCoinDawidSkene (macro-F1 0.5889)  
**Spread:** 0.1640

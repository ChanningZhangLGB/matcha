# pico_5k - crowd aggregation vs ground truth

## Corpus

| | |
|---|---|
| Instances (tasks scored) | **5,034** tokens (from 22 abstracts) |
| Annotators | 50 |
| Judgments | 31,119 (6.18 per instance) |
| Classes | 2 |
| Recast | **tok** - one task per token; 22 of 191 gold abstracts, seed 42 |
| Ground truth | a single professional annotator (`MedicalStudent`) |

**Gold label distribution**

| Label | n | % |
|---|--:|--:|
| `out` | 4,627 | 91.9% |
| `in` | 407 | 8.1% |

## Aggregators (8 unsupervised crowd-kit methods)

Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground truth at `fit()`.

| Method | accuracy | macro-f1 | weighted-f1 | f1-in | sec |
|---|--:|--:|--:|--:|--:|
| ZeroBasedSkill | 0.9615 | 0.8414 | 0.9571 | 0.7034 | 4.0 |
| MajorityVote | 0.9607 | 0.8372 | 0.9560 | 0.6954 | 0.2 |
| Wawa | 0.9601 | 0.8340 | 0.9553 | 0.6893 | 0.2 |
| DawidSkene | 0.9491 | 0.8323 | 0.9496 | 0.6923 | 0.4 |
| GLAD | 0.9587 | 0.8265 | 0.9534 | 0.6750 | 31.7 |
| MACE | 0.9567 | 0.8228 | 0.9519 | 0.6687 | 34.3 |
| OneCoinDawidSkene | 0.9575 | 0.8110 | 0.9505 | 0.6445 | 0.6 |
| MMSR | 0.9201 | 0.7320 | 0.9202 | 0.5074 | 2.9 |

**Best:** ZeroBasedSkill (macro-F1 0.8414)  
**Worst:** MMSR (macro-F1 0.7320)  
**Spread:** 0.1094

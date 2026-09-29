# conll_ner_5k / entropy — rank-based splits (qwen2.5-7b-instruct-q8_0)

4,941 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **48**

⚠️ **3,817 instances (77.3%) sit at u = 0.** Any cut beyond the 22.7% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 247 | 4,694 | 0.6931 | yes — 156 share u=0.6931 |
| 10% | 494 | 4,447 | 0.6365 | yes — 316 share u=0.6365 |
| 15% | 741 | 4,200 | 0.6365 | yes — 316 share u=0.6365 |
| 20% | 988 | 3,953 | 0.5004 | yes — 41 share u=0.5004 |
| 25% | 1,235 | 3,706 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 30% | 1,482 | 3,459 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 35% | 1,729 | 3,212 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 40% | 1,976 | 2,965 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 45% | 2,223 | 2,718 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 50% | 2,470 | 2,471 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 55% | 2,718 | 2,223 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 60% | 2,965 | 1,976 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 65% | 3,212 | 1,729 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 70% | 3,459 | 1,482 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 75% | 3,706 | 1,235 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 80% | 3,953 | 988 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 85% | 4,200 | 741 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 90% | 4,447 | 494 | -0.0000 | yes — 3,817 share u=-0.0000 |
| 95% | 4,694 | 247 | -0.0000 | yes — 3,817 share u=-0.0000 |

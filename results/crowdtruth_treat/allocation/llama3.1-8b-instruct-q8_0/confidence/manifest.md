# crowdtruth_treat / confidence — rank-based splits (llama3.1-8b-instruct-q8_0)

621 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **16**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 31 | 590 | 0.2000 | no |
| 10% | 62 | 559 | 0.1889 | yes — 32 share u=0.1889 |
| 15% | 93 | 528 | 0.1778 | yes — 36 share u=0.1778 |
| 20% | 124 | 497 | 0.1667 | yes — 60 share u=0.1667 |
| 25% | 155 | 466 | 0.1667 | yes — 60 share u=0.1667 |
| 30% | 186 | 435 | 0.1556 | yes — 46 share u=0.1556 |
| 35% | 217 | 404 | 0.1444 | yes — 43 share u=0.1444 |
| 40% | 248 | 373 | 0.1444 | yes — 43 share u=0.1444 |
| 45% | 279 | 342 | 0.1333 | yes — 85 share u=0.1333 |
| 50% | 310 | 311 | 0.1333 | yes — 85 share u=0.1333 |
| 55% | 342 | 279 | 0.1222 | yes — 78 share u=0.1222 |
| 60% | 373 | 248 | 0.1222 | yes — 78 share u=0.1222 |
| 65% | 404 | 217 | 0.1222 | yes — 78 share u=0.1222 |
| 70% | 435 | 186 | 0.1111 | yes — 54 share u=0.1111 |
| 75% | 466 | 155 | 0.1111 | no |
| 80% | 497 | 124 | 0.1000 | yes — 41 share u=0.1000 |
| 85% | 528 | 93 | 0.0889 | yes — 39 share u=0.0889 |
| 90% | 559 | 62 | 0.0778 | yes — 29 share u=0.0778 |
| 95% | 590 | 31 | 0.0667 | yes — 32 share u=0.0667 |

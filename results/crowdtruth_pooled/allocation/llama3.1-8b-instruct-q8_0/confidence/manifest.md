# crowdtruth_pooled / confidence — rank-based splits (llama3.1-8b-instruct-q8_0)

1,596 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **17**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 80 | 1,516 | 0.1889 | yes — 73 share u=0.1889 |
| 10% | 160 | 1,436 | 0.1778 | yes — 96 share u=0.1778 |
| 15% | 239 | 1,357 | 0.1778 | yes — 96 share u=0.1778 |
| 20% | 319 | 1,277 | 0.1667 | yes — 150 share u=0.1667 |
| 25% | 399 | 1,197 | 0.1556 | yes — 121 share u=0.1556 |
| 30% | 479 | 1,117 | 0.1556 | yes — 121 share u=0.1556 |
| 35% | 559 | 1,037 | 0.1444 | yes — 114 share u=0.1444 |
| 40% | 638 | 958 | 0.1333 | yes — 203 share u=0.1333 |
| 45% | 718 | 878 | 0.1333 | yes — 203 share u=0.1333 |
| 50% | 798 | 798 | 0.1333 | yes — 203 share u=0.1333 |
| 55% | 878 | 718 | 0.1222 | yes — 188 share u=0.1222 |
| 60% | 958 | 638 | 0.1222 | yes — 188 share u=0.1222 |
| 65% | 1,037 | 559 | 0.1111 | yes — 130 share u=0.1111 |
| 70% | 1,117 | 479 | 0.1111 | yes — 130 share u=0.1111 |
| 75% | 1,197 | 399 | 0.1000 | yes — 112 share u=0.1000 |
| 80% | 1,277 | 319 | 0.0889 | yes — 110 share u=0.0889 |
| 85% | 1,357 | 239 | 0.0889 | yes — 110 share u=0.0889 |
| 90% | 1,436 | 160 | 0.0778 | yes — 80 share u=0.0778 |
| 95% | 1,516 | 80 | 0.0667 | yes — 97 share u=0.0667 |

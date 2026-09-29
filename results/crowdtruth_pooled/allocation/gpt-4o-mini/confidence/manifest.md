# crowdtruth_pooled / confidence — rank-based splits (gpt-4o-mini)

1,596 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **32**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 80 | 1,516 | 0.1944 | yes — 27 share u=0.1944 |
| 10% | 160 | 1,436 | 0.1778 | yes — 59 share u=0.1778 |
| 15% | 239 | 1,357 | 0.1722 | yes — 52 share u=0.1722 |
| 20% | 319 | 1,277 | 0.1667 | yes — 86 share u=0.1667 |
| 25% | 399 | 1,197 | 0.1611 | yes — 120 share u=0.1611 |
| 30% | 479 | 1,117 | 0.1556 | yes — 120 share u=0.1556 |
| 35% | 559 | 1,037 | 0.1556 | yes — 120 share u=0.1556 |
| 40% | 638 | 958 | 0.1500 | yes — 116 share u=0.1500 |
| 45% | 718 | 878 | 0.1444 | yes — 144 share u=0.1444 |
| 50% | 798 | 798 | 0.1444 | yes — 144 share u=0.1444 |
| 55% | 878 | 718 | 0.1389 | yes — 131 share u=0.1389 |
| 60% | 958 | 638 | 0.1389 | yes — 131 share u=0.1389 |
| 65% | 1,037 | 559 | 0.1333 | yes — 100 share u=0.1333 |
| 70% | 1,117 | 479 | 0.1278 | yes — 85 share u=0.1278 |
| 75% | 1,197 | 399 | 0.1222 | yes — 81 share u=0.1222 |
| 80% | 1,277 | 319 | 0.1167 | yes — 104 share u=0.1167 |
| 85% | 1,357 | 239 | 0.1111 | yes — 79 share u=0.1111 |
| 90% | 1,436 | 160 | 0.1056 | yes — 57 share u=0.1056 |
| 95% | 1,516 | 80 | 0.1000 | yes — 48 share u=0.1000 |

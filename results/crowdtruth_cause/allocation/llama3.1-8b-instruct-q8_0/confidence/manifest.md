# crowdtruth_cause / confidence — rank-based splits (llama3.1-8b-instruct-q8_0)

975 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **17**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 49 | 926 | 0.1889 | yes — 41 share u=0.1889 |
| 10% | 98 | 877 | 0.1778 | yes — 60 share u=0.1778 |
| 15% | 146 | 829 | 0.1778 | no |
| 20% | 195 | 780 | 0.1667 | yes — 90 share u=0.1667 |
| 25% | 244 | 731 | 0.1556 | yes — 75 share u=0.1556 |
| 30% | 292 | 683 | 0.1556 | yes — 75 share u=0.1556 |
| 35% | 341 | 634 | 0.1444 | yes — 71 share u=0.1444 |
| 40% | 390 | 585 | 0.1333 | yes — 118 share u=0.1333 |
| 45% | 439 | 536 | 0.1333 | yes — 118 share u=0.1333 |
| 50% | 488 | 487 | 0.1333 | yes — 118 share u=0.1333 |
| 55% | 536 | 439 | 0.1222 | yes — 110 share u=0.1222 |
| 60% | 585 | 390 | 0.1222 | yes — 110 share u=0.1222 |
| 65% | 634 | 341 | 0.1111 | yes — 76 share u=0.1111 |
| 70% | 682 | 293 | 0.1111 | yes — 76 share u=0.1111 |
| 75% | 731 | 244 | 0.1000 | yes — 71 share u=0.1000 |
| 80% | 780 | 195 | 0.0889 | yes — 71 share u=0.0889 |
| 85% | 829 | 146 | 0.0778 | yes — 51 share u=0.0778 |
| 90% | 878 | 97 | 0.0778 | yes — 51 share u=0.0778 |
| 95% | 926 | 49 | 0.0667 | yes — 65 share u=0.0667 |

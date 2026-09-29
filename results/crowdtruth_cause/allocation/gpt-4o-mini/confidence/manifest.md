# crowdtruth_cause / confidence — rank-based splits (gpt-4o-mini)

975 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **32**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 49 | 926 | 0.1944 | yes — 16 share u=0.1944 |
| 10% | 98 | 877 | 0.1778 | yes — 39 share u=0.1778 |
| 15% | 146 | 829 | 0.1722 | yes — 35 share u=0.1722 |
| 20% | 195 | 780 | 0.1667 | yes — 55 share u=0.1667 |
| 25% | 244 | 731 | 0.1611 | yes — 79 share u=0.1611 |
| 30% | 292 | 683 | 0.1611 | yes — 79 share u=0.1611 |
| 35% | 341 | 634 | 0.1556 | yes — 74 share u=0.1556 |
| 40% | 390 | 585 | 0.1500 | yes — 73 share u=0.1500 |
| 45% | 439 | 536 | 0.1500 | yes — 73 share u=0.1500 |
| 50% | 488 | 487 | 0.1444 | yes — 89 share u=0.1444 |
| 55% | 536 | 439 | 0.1444 | yes — 89 share u=0.1444 |
| 60% | 585 | 390 | 0.1389 | yes — 80 share u=0.1389 |
| 65% | 634 | 341 | 0.1333 | yes — 58 share u=0.1333 |
| 70% | 682 | 293 | 0.1278 | yes — 52 share u=0.1278 |
| 75% | 731 | 244 | 0.1222 | yes — 50 share u=0.1222 |
| 80% | 780 | 195 | 0.1167 | yes — 61 share u=0.1167 |
| 85% | 829 | 146 | 0.1167 | yes — 61 share u=0.1167 |
| 90% | 878 | 97 | 0.1111 | yes — 45 share u=0.1111 |
| 95% | 926 | 49 | 0.1000 | yes — 28 share u=0.1000 |

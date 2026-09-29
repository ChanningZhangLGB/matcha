# crowdtruth_cause / confidence — rank-based splits (qwen2.5-7b-instruct-q8_0)

975 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **34**

⚠️ **32 instances (3.3%) sit at u = 0.** Any cut beyond the 96.7% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 49 | 926 | 0.1500 | yes — 30 share u=0.1500 |
| 10% | 98 | 877 | 0.1444 | yes — 25 share u=0.1444 |
| 15% | 146 | 829 | 0.1333 | yes — 57 share u=0.1333 |
| 20% | 195 | 780 | 0.1333 | yes — 57 share u=0.1333 |
| 25% | 244 | 731 | 0.1278 | yes — 55 share u=0.1278 |
| 30% | 292 | 683 | 0.1222 | yes — 54 share u=0.1222 |
| 35% | 341 | 634 | 0.1167 | yes — 86 share u=0.1167 |
| 40% | 390 | 585 | 0.1167 | yes — 86 share u=0.1167 |
| 45% | 439 | 536 | 0.1111 | yes — 61 share u=0.1111 |
| 50% | 488 | 487 | 0.1056 | yes — 38 share u=0.1056 |
| 55% | 536 | 439 | 0.1000 | yes — 56 share u=0.1000 |
| 60% | 585 | 390 | 0.0944 | yes — 39 share u=0.0944 |
| 65% | 634 | 341 | 0.0833 | yes — 44 share u=0.0833 |
| 70% | 682 | 293 | 0.0778 | yes — 33 share u=0.0778 |
| 75% | 731 | 244 | 0.0722 | yes — 27 share u=0.0722 |
| 80% | 780 | 195 | 0.0611 | yes — 28 share u=0.0611 |
| 85% | 829 | 146 | 0.0500 | yes — 21 share u=0.0500 |
| 90% | 878 | 97 | 0.0333 | yes — 10 share u=0.0333 |
| 95% | 926 | 49 | 0.0167 | yes — 15 share u=0.0167 |

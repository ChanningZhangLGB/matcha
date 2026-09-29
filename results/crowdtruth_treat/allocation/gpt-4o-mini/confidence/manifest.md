# crowdtruth_treat / confidence — rank-based splits (gpt-4o-mini)

621 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **31**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 31 | 590 | 0.1944 | yes — 11 share u=0.1944 |
| 10% | 62 | 559 | 0.1833 | yes — 12 share u=0.1833 |
| 15% | 93 | 528 | 0.1722 | yes — 17 share u=0.1722 |
| 20% | 124 | 497 | 0.1667 | yes — 31 share u=0.1667 |
| 25% | 155 | 466 | 0.1611 | yes — 41 share u=0.1611 |
| 30% | 186 | 435 | 0.1556 | yes — 46 share u=0.1556 |
| 35% | 217 | 404 | 0.1556 | yes — 46 share u=0.1556 |
| 40% | 248 | 373 | 0.1500 | yes — 43 share u=0.1500 |
| 45% | 279 | 342 | 0.1444 | yes — 55 share u=0.1444 |
| 50% | 310 | 311 | 0.1444 | yes — 55 share u=0.1444 |
| 55% | 342 | 279 | 0.1389 | yes — 51 share u=0.1389 |
| 60% | 373 | 248 | 0.1333 | yes — 42 share u=0.1333 |
| 65% | 404 | 217 | 0.1333 | yes — 42 share u=0.1333 |
| 70% | 435 | 186 | 0.1278 | yes — 33 share u=0.1278 |
| 75% | 466 | 155 | 0.1222 | yes — 31 share u=0.1222 |
| 80% | 497 | 124 | 0.1167 | yes — 43 share u=0.1167 |
| 85% | 528 | 93 | 0.1111 | yes — 34 share u=0.1111 |
| 90% | 559 | 62 | 0.1056 | yes — 24 share u=0.1056 |
| 95% | 590 | 31 | 0.1000 | yes — 20 share u=0.1000 |

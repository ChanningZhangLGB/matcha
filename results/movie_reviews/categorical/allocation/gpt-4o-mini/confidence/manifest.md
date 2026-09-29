# movie_reviews / confidence — rank-based splits (gpt-4o-mini)

1,498 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **74**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 75 | 1,423 | 0.2722 | yes — 22 share u=0.2722 |
| 10% | 150 | 1,348 | 0.2611 | yes — 20 share u=0.2611 |
| 15% | 225 | 1,273 | 0.2500 | yes — 51 share u=0.2500 |
| 20% | 300 | 1,198 | 0.2438 | yes — 20 share u=0.2438 |
| 25% | 374 | 1,124 | 0.2333 | yes — 82 share u=0.2333 |
| 30% | 449 | 1,049 | 0.2313 | yes — 25 share u=0.2313 |
| 35% | 524 | 974 | 0.2222 | yes — 98 share u=0.2222 |
| 40% | 599 | 899 | 0.2222 | yes — 98 share u=0.2222 |
| 45% | 674 | 824 | 0.2125 | yes — 139 share u=0.2125 |
| 50% | 749 | 749 | 0.2125 | yes — 139 share u=0.2125 |
| 55% | 824 | 674 | 0.2111 | yes — 57 share u=0.2111 |
| 60% | 899 | 599 | 0.2056 | yes — 45 share u=0.2056 |
| 65% | 974 | 524 | 0.2000 | yes — 81 share u=0.2000 |
| 70% | 1,049 | 449 | 0.1889 | yes — 47 share u=0.1889 |
| 75% | 1,124 | 374 | 0.1833 | yes — 44 share u=0.1833 |
| 80% | 1,198 | 300 | 0.1722 | yes — 31 share u=0.1722 |
| 85% | 1,273 | 225 | 0.1611 | yes — 36 share u=0.1611 |
| 90% | 1,348 | 150 | 0.1500 | yes — 41 share u=0.1500 |
| 95% | 1,423 | 75 | 0.1389 | yes — 23 share u=0.1389 |

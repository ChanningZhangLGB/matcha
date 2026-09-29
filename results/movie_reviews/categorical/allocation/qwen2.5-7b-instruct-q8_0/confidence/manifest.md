# movie_reviews / confidence — rank-based splits (qwen2.5-7b-instruct-q8_0)

1,498 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **63**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 75 | 1,423 | 0.3056 | yes — 44 share u=0.3056 |
| 10% | 150 | 1,348 | 0.3000 | yes — 97 share u=0.3000 |
| 15% | 225 | 1,273 | 0.2944 | yes — 56 share u=0.2944 |
| 20% | 300 | 1,198 | 0.2889 | yes — 103 share u=0.2889 |
| 25% | 374 | 1,124 | 0.2833 | yes — 68 share u=0.2833 |
| 30% | 449 | 1,049 | 0.2778 | yes — 129 share u=0.2778 |
| 35% | 524 | 974 | 0.2778 | yes — 129 share u=0.2778 |
| 40% | 599 | 899 | 0.2722 | yes — 57 share u=0.2722 |
| 45% | 674 | 824 | 0.2667 | yes — 78 share u=0.2667 |
| 50% | 749 | 749 | 0.2556 | yes — 67 share u=0.2556 |
| 55% | 824 | 674 | 0.2500 | yes — 27 share u=0.2500 |
| 60% | 899 | 599 | 0.2333 | yes — 34 share u=0.2333 |
| 65% | 974 | 524 | 0.2222 | yes — 48 share u=0.2222 |
| 70% | 1,049 | 449 | 0.2000 | yes — 36 share u=0.2000 |
| 75% | 1,124 | 374 | 0.1889 | yes — 32 share u=0.1889 |
| 80% | 1,198 | 300 | 0.1778 | yes — 71 share u=0.1778 |
| 85% | 1,273 | 225 | 0.1611 | yes — 15 share u=0.1611 |
| 90% | 1,348 | 150 | 0.1444 | yes — 29 share u=0.1444 |
| 95% | 1,423 | 75 | 0.1167 | yes — 12 share u=0.1167 |

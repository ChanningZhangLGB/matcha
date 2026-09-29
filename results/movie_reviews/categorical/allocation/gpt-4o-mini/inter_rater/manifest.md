# movie_reviews / inter_rater — rank-based splits (gpt-4o-mini)

1,498 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **14**

⚠️ **904 instances (60.3%) sit at u = 0.** Any cut beyond the 39.7% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 75 | 1,423 | 0.5556 | yes — 64 share u=0.5556 |
| 10% | 150 | 1,348 | 0.5357 | yes — 51 share u=0.5357 |
| 15% | 225 | 1,273 | 0.5000 | yes — 107 share u=0.5000 |
| 20% | 300 | 1,198 | 0.4286 | yes — 64 share u=0.4286 |
| 25% | 374 | 1,124 | 0.3889 | yes — 115 share u=0.3889 |
| 30% | 449 | 1,049 | 0.3889 | yes — 115 share u=0.3889 |
| 35% | 524 | 974 | 0.2500 | yes — 77 share u=0.2500 |
| 40% | 599 | 899 | 0.0000 | yes — 904 share u=0.0000 |
| 45% | 674 | 824 | 0.0000 | yes — 904 share u=0.0000 |
| 50% | 749 | 749 | 0.0000 | yes — 904 share u=0.0000 |
| 55% | 824 | 674 | 0.0000 | yes — 904 share u=0.0000 |
| 60% | 899 | 599 | 0.0000 | yes — 904 share u=0.0000 |
| 65% | 974 | 524 | 0.0000 | yes — 904 share u=0.0000 |
| 70% | 1,049 | 449 | 0.0000 | yes — 904 share u=0.0000 |
| 75% | 1,124 | 374 | 0.0000 | yes — 904 share u=0.0000 |
| 80% | 1,198 | 300 | 0.0000 | yes — 904 share u=0.0000 |
| 85% | 1,273 | 225 | 0.0000 | yes — 904 share u=0.0000 |
| 90% | 1,348 | 150 | 0.0000 | yes — 904 share u=0.0000 |
| 95% | 1,423 | 75 | 0.0000 | yes — 904 share u=0.0000 |

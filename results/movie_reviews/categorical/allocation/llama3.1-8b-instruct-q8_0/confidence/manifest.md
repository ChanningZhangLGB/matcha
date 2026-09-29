# movie_reviews / confidence — rank-based splits (llama3.1-8b-instruct-q8_0)

1,498 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **30**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 75 | 1,423 | 0.2444 | yes — 164 share u=0.2444 |
| 10% | 150 | 1,348 | 0.2444 | yes — 164 share u=0.2444 |
| 15% | 225 | 1,273 | 0.2222 | yes — 381 share u=0.2222 |
| 20% | 300 | 1,198 | 0.2222 | yes — 381 share u=0.2222 |
| 25% | 374 | 1,124 | 0.2222 | yes — 381 share u=0.2222 |
| 30% | 449 | 1,049 | 0.2222 | yes — 381 share u=0.2222 |
| 35% | 524 | 974 | 0.2222 | yes — 381 share u=0.2222 |
| 40% | 599 | 899 | 0.2222 | yes — 381 share u=0.2222 |
| 45% | 674 | 824 | 0.2000 | yes — 589 share u=0.2000 |
| 50% | 749 | 749 | 0.2000 | yes — 589 share u=0.2000 |
| 55% | 824 | 674 | 0.2000 | yes — 589 share u=0.2000 |
| 60% | 899 | 599 | 0.2000 | yes — 589 share u=0.2000 |
| 65% | 974 | 524 | 0.2000 | yes — 589 share u=0.2000 |
| 70% | 1,049 | 449 | 0.2000 | yes — 589 share u=0.2000 |
| 75% | 1,124 | 374 | 0.2000 | yes — 589 share u=0.2000 |
| 80% | 1,198 | 300 | 0.2000 | yes — 589 share u=0.2000 |
| 85% | 1,273 | 225 | 0.1889 | yes — 96 share u=0.1889 |
| 90% | 1,348 | 150 | 0.1778 | yes — 64 share u=0.1778 |
| 95% | 1,423 | 75 | 0.1556 | yes — 23 share u=0.1556 |

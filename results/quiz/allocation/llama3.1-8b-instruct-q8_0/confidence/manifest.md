# quiz / confidence — rank-based splits (llama3.1-8b-instruct-q8_0)

155 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **22**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 8 | 147 | 0.2111 | yes — 2 share u=0.2111 |
| 10% | 16 | 139 | 0.2000 | yes — 11 share u=0.2000 |
| 15% | 23 | 132 | 0.1778 | yes — 12 share u=0.1778 |
| 20% | 31 | 124 | 0.1778 | yes — 12 share u=0.1778 |
| 25% | 39 | 116 | 0.1667 | yes — 6 share u=0.1667 |
| 30% | 46 | 109 | 0.1556 | yes — 16 share u=0.1556 |
| 35% | 54 | 101 | 0.1556 | yes — 16 share u=0.1556 |
| 40% | 62 | 93 | 0.1444 | no |
| 45% | 70 | 85 | 0.1333 | yes — 12 share u=0.1333 |
| 50% | 78 | 77 | 0.1222 | yes — 9 share u=0.1222 |
| 55% | 85 | 70 | 0.1111 | yes — 14 share u=0.1111 |
| 60% | 93 | 62 | 0.1111 | yes — 14 share u=0.1111 |
| 65% | 101 | 54 | 0.1000 | yes — 10 share u=0.1000 |
| 70% | 108 | 47 | 0.1000 | no |
| 75% | 116 | 39 | 0.0889 | yes — 23 share u=0.0889 |
| 80% | 124 | 31 | 0.0889 | yes — 23 share u=0.0889 |
| 85% | 132 | 23 | 0.0889 | no |
| 90% | 140 | 15 | 0.0667 | yes — 11 share u=0.0667 |
| 95% | 147 | 8 | 0.0667 | yes — 11 share u=0.0667 |

# quiz / confidence — rank-based splits (gpt-4o-mini)

155 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **39**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 8 | 147 | 0.2111 | no |
| 10% | 16 | 139 | 0.1944 | no |
| 15% | 23 | 132 | 0.1889 | yes — 9 share u=0.1889 |
| 20% | 31 | 124 | 0.1778 | yes — 3 share u=0.1778 |
| 25% | 39 | 116 | 0.1667 | yes — 10 share u=0.1667 |
| 30% | 46 | 109 | 0.1667 | yes — 10 share u=0.1667 |
| 35% | 54 | 101 | 0.1556 | yes — 6 share u=0.1556 |
| 40% | 62 | 93 | 0.1444 | yes — 9 share u=0.1444 |
| 45% | 70 | 85 | 0.1333 | yes — 8 share u=0.1333 |
| 50% | 78 | 77 | 0.1278 | no |
| 55% | 85 | 70 | 0.1111 | yes — 7 share u=0.1111 |
| 60% | 93 | 62 | 0.1056 | no |
| 65% | 101 | 54 | 0.0944 | yes — 8 share u=0.0944 |
| 70% | 108 | 47 | 0.0889 | yes — 7 share u=0.0889 |
| 75% | 116 | 39 | 0.0833 | yes — 10 share u=0.0833 |
| 80% | 124 | 31 | 0.0778 | yes — 7 share u=0.0778 |
| 85% | 132 | 23 | 0.0722 | yes — 9 share u=0.0722 |
| 90% | 140 | 15 | 0.0611 | yes — 6 share u=0.0611 |
| 95% | 147 | 8 | 0.0556 | no |

# quiz / confidence — rank-based splits (qwen2.5-7b-instruct-q8_0)

155 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **32**

⚠️ **59 instances (38.1%) sit at u = 0.** Any cut beyond the 61.9% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 8 | 147 | 0.1944 | no |
| 10% | 16 | 139 | 0.1667 | yes — 4 share u=0.1667 |
| 15% | 23 | 132 | 0.1444 | no |
| 20% | 31 | 124 | 0.1222 | yes — 2 share u=0.1222 |
| 25% | 39 | 116 | 0.1111 | yes — 8 share u=0.1111 |
| 30% | 46 | 109 | 0.0889 | yes — 8 share u=0.0889 |
| 35% | 54 | 101 | 0.0833 | yes — 5 share u=0.0833 |
| 40% | 62 | 93 | 0.0611 | yes — 2 share u=0.0611 |
| 45% | 70 | 85 | 0.0444 | yes — 7 share u=0.0444 |
| 50% | 78 | 77 | 0.0222 | yes — 17 share u=0.0222 |
| 55% | 85 | 70 | 0.0222 | yes — 17 share u=0.0222 |
| 60% | 93 | 62 | 0.0222 | no |
| 65% | 101 | 54 | 0.0000 | yes — 59 share u=0.0000 |
| 70% | 108 | 47 | 0.0000 | yes — 59 share u=0.0000 |
| 75% | 116 | 39 | 0.0000 | yes — 59 share u=0.0000 |
| 80% | 124 | 31 | 0.0000 | yes — 59 share u=0.0000 |
| 85% | 132 | 23 | 0.0000 | yes — 59 share u=0.0000 |
| 90% | 140 | 15 | 0.0000 | yes — 59 share u=0.0000 |
| 95% | 147 | 8 | 0.0000 | yes — 59 share u=0.0000 |

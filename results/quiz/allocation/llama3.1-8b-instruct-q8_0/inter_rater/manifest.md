# quiz / inter_rater — rank-based splits (llama3.1-8b-instruct-q8_0)

155 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **16**

⚠️ **51 instances (32.9%) sit at u = 0.** Any cut beyond the 67.1% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 8 | 147 | 0.7500 | yes — 5 share u=0.7500 |
| 10% | 16 | 139 | 0.7222 | yes — 8 share u=0.7222 |
| 15% | 23 | 132 | 0.6667 | yes — 2 share u=0.6667 |
| 20% | 31 | 124 | 0.6389 | yes — 16 share u=0.6389 |
| 25% | 39 | 116 | 0.6389 | yes — 16 share u=0.6389 |
| 30% | 46 | 109 | 0.5556 | yes — 10 share u=0.5556 |
| 35% | 54 | 101 | 0.5000 | yes — 22 share u=0.5000 |
| 40% | 62 | 93 | 0.5000 | yes — 22 share u=0.5000 |
| 45% | 70 | 85 | 0.5000 | yes — 22 share u=0.5000 |
| 50% | 78 | 77 | 0.3889 | yes — 17 share u=0.3889 |
| 55% | 85 | 70 | 0.3889 | yes — 17 share u=0.3889 |
| 60% | 93 | 62 | 0.3889 | no |
| 65% | 101 | 54 | 0.2222 | yes — 11 share u=0.2222 |
| 70% | 108 | 47 | 0.0000 | yes — 51 share u=0.0000 |
| 75% | 116 | 39 | 0.0000 | yes — 51 share u=0.0000 |
| 80% | 124 | 31 | 0.0000 | yes — 51 share u=0.0000 |
| 85% | 132 | 23 | 0.0000 | yes — 51 share u=0.0000 |
| 90% | 140 | 15 | 0.0000 | yes — 51 share u=0.0000 |
| 95% | 147 | 8 | 0.0000 | yes — 51 share u=0.0000 |

# quiz / entropy — rank-based splits (llama3.1-8b-instruct-q8_0)

155 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **19**

⚠️ **51 instances (32.9%) sit at u = 0.** Any cut beyond the 67.1% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 8 | 147 | 1.2149 | yes — 3 share u=1.2149 |
| 10% | 16 | 139 | 1.0609 | yes — 8 share u=1.0609 |
| 15% | 23 | 132 | 1.0027 | no |
| 20% | 31 | 124 | 0.9369 | yes — 16 share u=0.9369 |
| 25% | 39 | 116 | 0.9369 | yes — 16 share u=0.9369 |
| 30% | 46 | 109 | 0.8487 | no |
| 35% | 54 | 101 | 0.6616 | no |
| 40% | 62 | 93 | 0.6365 | yes — 22 share u=0.6365 |
| 45% | 70 | 85 | 0.6365 | yes — 22 share u=0.6365 |
| 50% | 78 | 77 | 0.5297 | yes — 17 share u=0.5297 |
| 55% | 85 | 70 | 0.5297 | yes — 17 share u=0.5297 |
| 60% | 93 | 62 | 0.5297 | no |
| 65% | 101 | 54 | 0.3488 | yes — 11 share u=0.3488 |
| 70% | 108 | 47 | -0.0000 | yes — 51 share u=-0.0000 |
| 75% | 116 | 39 | -0.0000 | yes — 51 share u=-0.0000 |
| 80% | 124 | 31 | -0.0000 | yes — 51 share u=-0.0000 |
| 85% | 132 | 23 | -0.0000 | yes — 51 share u=-0.0000 |
| 90% | 140 | 15 | -0.0000 | yes — 51 share u=-0.0000 |
| 95% | 147 | 8 | -0.0000 | yes — 51 share u=-0.0000 |

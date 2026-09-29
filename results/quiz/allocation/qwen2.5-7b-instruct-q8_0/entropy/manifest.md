# quiz / entropy — rank-based splits (qwen2.5-7b-instruct-q8_0)

155 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **17**

⚠️ **60 instances (38.7%) sit at u = 0.** Any cut beyond the 61.3% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 8 | 147 | 1.0609 | yes — 7 share u=1.0609 |
| 10% | 16 | 139 | 0.9950 | no |
| 15% | 23 | 132 | 0.8487 | yes — 8 share u=0.8487 |
| 20% | 31 | 124 | 0.6870 | yes — 2 share u=0.6870 |
| 25% | 39 | 116 | 0.6365 | yes — 18 share u=0.6365 |
| 30% | 46 | 109 | 0.6365 | yes — 18 share u=0.6365 |
| 35% | 54 | 101 | 0.6365 | no |
| 40% | 62 | 93 | 0.5297 | no |
| 45% | 70 | 85 | 0.3488 | yes — 33 share u=0.3488 |
| 50% | 78 | 77 | 0.3488 | yes — 33 share u=0.3488 |
| 55% | 85 | 70 | 0.3488 | yes — 33 share u=0.3488 |
| 60% | 93 | 62 | 0.3488 | yes — 33 share u=0.3488 |
| 65% | 101 | 54 | -0.0000 | yes — 60 share u=-0.0000 |
| 70% | 108 | 47 | -0.0000 | yes — 60 share u=-0.0000 |
| 75% | 116 | 39 | -0.0000 | yes — 60 share u=-0.0000 |
| 80% | 124 | 31 | -0.0000 | yes — 60 share u=-0.0000 |
| 85% | 132 | 23 | -0.0000 | yes — 60 share u=-0.0000 |
| 90% | 140 | 15 | -0.0000 | yes — 60 share u=-0.0000 |
| 95% | 147 | 8 | -0.0000 | yes — 60 share u=-0.0000 |

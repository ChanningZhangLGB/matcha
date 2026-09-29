# quiz / entropy — rank-based splits (gpt-4o-mini)

155 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **11** (heavily tied)

⚠️ **120 instances (77.4%) sit at u = 0.** Any cut beyond the 22.6% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 8 | 147 | 0.8487 | yes — 3 share u=0.8487 |
| 10% | 16 | 139 | 0.6837 | no |
| 15% | 23 | 132 | 0.6365 | no |
| 20% | 31 | 124 | 0.3488 | yes — 7 share u=0.3488 |
| 25% | 39 | 116 | -0.0000 | yes — 120 share u=-0.0000 |
| 30% | 46 | 109 | -0.0000 | yes — 120 share u=-0.0000 |
| 35% | 54 | 101 | -0.0000 | yes — 120 share u=-0.0000 |
| 40% | 62 | 93 | -0.0000 | yes — 120 share u=-0.0000 |
| 45% | 70 | 85 | -0.0000 | yes — 120 share u=-0.0000 |
| 50% | 78 | 77 | -0.0000 | yes — 120 share u=-0.0000 |
| 55% | 85 | 70 | -0.0000 | yes — 120 share u=-0.0000 |
| 60% | 93 | 62 | -0.0000 | yes — 120 share u=-0.0000 |
| 65% | 101 | 54 | -0.0000 | yes — 120 share u=-0.0000 |
| 70% | 108 | 47 | -0.0000 | yes — 120 share u=-0.0000 |
| 75% | 116 | 39 | -0.0000 | yes — 120 share u=-0.0000 |
| 80% | 124 | 31 | -0.0000 | yes — 120 share u=-0.0000 |
| 85% | 132 | 23 | -0.0000 | yes — 120 share u=-0.0000 |
| 90% | 140 | 15 | -0.0000 | yes — 120 share u=-0.0000 |
| 95% | 147 | 8 | -0.0000 | yes — 120 share u=-0.0000 |

# crowdtruth_pooled / entropy — rank-based splits (llama3.1-8b-instruct-q8_0)

1,596 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **6** (heavily tied)

⚠️ **976 instances (61.2%) sit at u = 0.** Any cut beyond the 38.8% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 80 | 1,516 | 0.6870 | yes — 139 share u=0.6870 |
| 10% | 160 | 1,436 | 0.6365 | yes — 114 share u=0.6365 |
| 15% | 239 | 1,357 | 0.6365 | yes — 114 share u=0.6365 |
| 20% | 319 | 1,277 | 0.5297 | yes — 215 share u=0.5297 |
| 25% | 399 | 1,197 | 0.5297 | yes — 215 share u=0.5297 |
| 30% | 479 | 1,117 | 0.3488 | yes — 151 share u=0.3488 |
| 35% | 559 | 1,037 | 0.3488 | yes — 151 share u=0.3488 |
| 40% | 638 | 958 | -0.0000 | yes — 976 share u=-0.0000 |
| 45% | 718 | 878 | -0.0000 | yes — 976 share u=-0.0000 |
| 50% | 798 | 798 | -0.0000 | yes — 976 share u=-0.0000 |
| 55% | 878 | 718 | -0.0000 | yes — 976 share u=-0.0000 |
| 60% | 958 | 638 | -0.0000 | yes — 976 share u=-0.0000 |
| 65% | 1,037 | 559 | -0.0000 | yes — 976 share u=-0.0000 |
| 70% | 1,117 | 479 | -0.0000 | yes — 976 share u=-0.0000 |
| 75% | 1,197 | 399 | -0.0000 | yes — 976 share u=-0.0000 |
| 80% | 1,277 | 319 | -0.0000 | yes — 976 share u=-0.0000 |
| 85% | 1,357 | 239 | -0.0000 | yes — 976 share u=-0.0000 |
| 90% | 1,436 | 160 | -0.0000 | yes — 976 share u=-0.0000 |
| 95% | 1,516 | 80 | -0.0000 | yes — 976 share u=-0.0000 |

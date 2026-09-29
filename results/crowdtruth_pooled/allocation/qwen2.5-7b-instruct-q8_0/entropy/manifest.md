# crowdtruth_pooled / entropy — rank-based splits (qwen2.5-7b-instruct-q8_0)

1,596 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **5** (heavily tied)

⚠️ **1,139 instances (71.4%) sit at u = 0.** Any cut beyond the 28.6% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 80 | 1,516 | 0.6870 | yes — 100 share u=0.6870 |
| 10% | 160 | 1,436 | 0.6365 | yes — 100 share u=0.6365 |
| 15% | 239 | 1,357 | 0.5297 | yes — 124 share u=0.5297 |
| 20% | 319 | 1,277 | 0.5297 | yes — 124 share u=0.5297 |
| 25% | 399 | 1,197 | 0.3488 | yes — 133 share u=0.3488 |
| 30% | 479 | 1,117 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 35% | 559 | 1,037 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 40% | 638 | 958 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 45% | 718 | 878 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 50% | 798 | 798 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 55% | 878 | 718 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 60% | 958 | 638 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 65% | 1,037 | 559 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 70% | 1,117 | 479 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 75% | 1,197 | 399 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 80% | 1,277 | 319 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 85% | 1,357 | 239 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 90% | 1,436 | 160 | -0.0000 | yes — 1,139 share u=-0.0000 |
| 95% | 1,516 | 80 | -0.0000 | yes — 1,139 share u=-0.0000 |

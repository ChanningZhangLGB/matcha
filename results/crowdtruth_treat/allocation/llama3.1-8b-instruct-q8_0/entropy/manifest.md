# crowdtruth_treat / entropy — rank-based splits (llama3.1-8b-instruct-q8_0)

621 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **6** (heavily tied)

⚠️ **397 instances (63.9%) sit at u = 0.** Any cut beyond the 36.1% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 31 | 590 | 0.6870 | yes — 69 share u=0.6870 |
| 10% | 62 | 559 | 0.6870 | yes — 69 share u=0.6870 |
| 15% | 93 | 528 | 0.6365 | yes — 43 share u=0.6365 |
| 20% | 124 | 497 | 0.5297 | yes — 76 share u=0.5297 |
| 25% | 155 | 466 | 0.5297 | yes — 76 share u=0.5297 |
| 30% | 186 | 435 | 0.5297 | yes — 76 share u=0.5297 |
| 35% | 217 | 404 | 0.3488 | yes — 35 share u=0.3488 |
| 40% | 248 | 373 | -0.0000 | yes — 397 share u=-0.0000 |
| 45% | 279 | 342 | -0.0000 | yes — 397 share u=-0.0000 |
| 50% | 310 | 311 | -0.0000 | yes — 397 share u=-0.0000 |
| 55% | 342 | 279 | -0.0000 | yes — 397 share u=-0.0000 |
| 60% | 373 | 248 | -0.0000 | yes — 397 share u=-0.0000 |
| 65% | 404 | 217 | -0.0000 | yes — 397 share u=-0.0000 |
| 70% | 435 | 186 | -0.0000 | yes — 397 share u=-0.0000 |
| 75% | 466 | 155 | -0.0000 | yes — 397 share u=-0.0000 |
| 80% | 497 | 124 | -0.0000 | yes — 397 share u=-0.0000 |
| 85% | 528 | 93 | -0.0000 | yes — 397 share u=-0.0000 |
| 90% | 559 | 62 | -0.0000 | yes — 397 share u=-0.0000 |
| 95% | 590 | 31 | -0.0000 | yes — 397 share u=-0.0000 |

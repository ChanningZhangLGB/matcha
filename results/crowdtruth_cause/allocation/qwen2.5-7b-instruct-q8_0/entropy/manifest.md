# crowdtruth_cause / entropy — rank-based splits (qwen2.5-7b-instruct-q8_0)

975 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **5** (heavily tied)

⚠️ **692 instances (71.0%) sit at u = 0.** Any cut beyond the 29.0% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 49 | 926 | 0.6870 | yes — 74 share u=0.6870 |
| 10% | 98 | 877 | 0.6365 | yes — 68 share u=0.6365 |
| 15% | 146 | 829 | 0.5297 | yes — 76 share u=0.5297 |
| 20% | 195 | 780 | 0.5297 | yes — 76 share u=0.5297 |
| 25% | 244 | 731 | 0.3488 | yes — 65 share u=0.3488 |
| 30% | 292 | 683 | -0.0000 | yes — 692 share u=-0.0000 |
| 35% | 341 | 634 | -0.0000 | yes — 692 share u=-0.0000 |
| 40% | 390 | 585 | -0.0000 | yes — 692 share u=-0.0000 |
| 45% | 439 | 536 | -0.0000 | yes — 692 share u=-0.0000 |
| 50% | 488 | 487 | -0.0000 | yes — 692 share u=-0.0000 |
| 55% | 536 | 439 | -0.0000 | yes — 692 share u=-0.0000 |
| 60% | 585 | 390 | -0.0000 | yes — 692 share u=-0.0000 |
| 65% | 634 | 341 | -0.0000 | yes — 692 share u=-0.0000 |
| 70% | 682 | 293 | -0.0000 | yes — 692 share u=-0.0000 |
| 75% | 731 | 244 | -0.0000 | yes — 692 share u=-0.0000 |
| 80% | 780 | 195 | -0.0000 | yes — 692 share u=-0.0000 |
| 85% | 829 | 146 | -0.0000 | yes — 692 share u=-0.0000 |
| 90% | 878 | 97 | -0.0000 | yes — 692 share u=-0.0000 |
| 95% | 926 | 49 | -0.0000 | yes — 692 share u=-0.0000 |

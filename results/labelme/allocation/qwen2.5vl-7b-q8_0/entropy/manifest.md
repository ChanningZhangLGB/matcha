# labelme / entropy — rank-based splits (qwen2.5vl-7b-q8_0)

1,000 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **12** (heavily tied)

⚠️ **744 instances (74.4%) sit at u = 0.** Any cut beyond the 25.6% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 50 | 950 | 0.6870 | yes — 34 share u=0.6870 |
| 10% | 100 | 900 | 0.6365 | yes — 44 share u=0.6365 |
| 15% | 150 | 850 | 0.5297 | yes — 53 share u=0.5297 |
| 20% | 200 | 800 | 0.3488 | yes — 89 share u=0.3488 |
| 25% | 250 | 750 | 0.3488 | yes — 89 share u=0.3488 |
| 30% | 300 | 700 | -0.0000 | yes — 744 share u=-0.0000 |
| 35% | 350 | 650 | -0.0000 | yes — 744 share u=-0.0000 |
| 40% | 400 | 600 | -0.0000 | yes — 744 share u=-0.0000 |
| 45% | 450 | 550 | -0.0000 | yes — 744 share u=-0.0000 |
| 50% | 500 | 500 | -0.0000 | yes — 744 share u=-0.0000 |
| 55% | 550 | 450 | -0.0000 | yes — 744 share u=-0.0000 |
| 60% | 600 | 400 | -0.0000 | yes — 744 share u=-0.0000 |
| 65% | 650 | 350 | -0.0000 | yes — 744 share u=-0.0000 |
| 70% | 700 | 300 | -0.0000 | yes — 744 share u=-0.0000 |
| 75% | 750 | 250 | -0.0000 | yes — 744 share u=-0.0000 |
| 80% | 800 | 200 | -0.0000 | yes — 744 share u=-0.0000 |
| 85% | 850 | 150 | -0.0000 | yes — 744 share u=-0.0000 |
| 90% | 900 | 100 | -0.0000 | yes — 744 share u=-0.0000 |
| 95% | 950 | 50 | -0.0000 | yes — 744 share u=-0.0000 |

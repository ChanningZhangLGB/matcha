# labelme / entropy — rank-based splits (minicpm-v-8b-2.6-q8_0)

1,000 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **16**

⚠️ **680 instances (68.0%) sit at u = 0.** Any cut beyond the 32.0% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 50 | 950 | 0.8487 | yes — 10 share u=0.8487 |
| 10% | 100 | 900 | 0.6837 | yes — 12 share u=0.6837 |
| 15% | 150 | 850 | 0.6365 | yes — 42 share u=0.6365 |
| 20% | 200 | 800 | 0.5297 | yes — 77 share u=0.5297 |
| 25% | 250 | 750 | 0.3488 | yes — 91 share u=0.3488 |
| 30% | 300 | 700 | 0.3488 | yes — 91 share u=0.3488 |
| 35% | 350 | 650 | -0.0000 | yes — 680 share u=-0.0000 |
| 40% | 400 | 600 | -0.0000 | yes — 680 share u=-0.0000 |
| 45% | 450 | 550 | -0.0000 | yes — 680 share u=-0.0000 |
| 50% | 500 | 500 | -0.0000 | yes — 680 share u=-0.0000 |
| 55% | 550 | 450 | -0.0000 | yes — 680 share u=-0.0000 |
| 60% | 600 | 400 | -0.0000 | yes — 680 share u=-0.0000 |
| 65% | 650 | 350 | -0.0000 | yes — 680 share u=-0.0000 |
| 70% | 700 | 300 | -0.0000 | yes — 680 share u=-0.0000 |
| 75% | 750 | 250 | -0.0000 | yes — 680 share u=-0.0000 |
| 80% | 800 | 200 | -0.0000 | yes — 680 share u=-0.0000 |
| 85% | 850 | 150 | -0.0000 | yes — 680 share u=-0.0000 |
| 90% | 900 | 100 | -0.0000 | yes — 680 share u=-0.0000 |
| 95% | 950 | 50 | -0.0000 | yes — 680 share u=-0.0000 |

# labelme / entropy — rank-based splits (gpt-4o-mini)

1,000 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **13**

⚠️ **769 instances (76.9%) sit at u = 0.** Any cut beyond the 23.1% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 50 | 950 | 0.6837 | yes — 5 share u=0.6837 |
| 10% | 100 | 900 | 0.5297 | yes — 60 share u=0.5297 |
| 15% | 150 | 850 | 0.5297 | yes — 60 share u=0.5297 |
| 20% | 200 | 800 | 0.3488 | yes — 74 share u=0.3488 |
| 25% | 250 | 750 | -0.0000 | yes — 769 share u=-0.0000 |
| 30% | 300 | 700 | -0.0000 | yes — 769 share u=-0.0000 |
| 35% | 350 | 650 | -0.0000 | yes — 769 share u=-0.0000 |
| 40% | 400 | 600 | -0.0000 | yes — 769 share u=-0.0000 |
| 45% | 450 | 550 | -0.0000 | yes — 769 share u=-0.0000 |
| 50% | 500 | 500 | -0.0000 | yes — 769 share u=-0.0000 |
| 55% | 550 | 450 | -0.0000 | yes — 769 share u=-0.0000 |
| 60% | 600 | 400 | -0.0000 | yes — 769 share u=-0.0000 |
| 65% | 650 | 350 | -0.0000 | yes — 769 share u=-0.0000 |
| 70% | 700 | 300 | -0.0000 | yes — 769 share u=-0.0000 |
| 75% | 750 | 250 | -0.0000 | yes — 769 share u=-0.0000 |
| 80% | 800 | 200 | -0.0000 | yes — 769 share u=-0.0000 |
| 85% | 850 | 150 | -0.0000 | yes — 769 share u=-0.0000 |
| 90% | 900 | 100 | -0.0000 | yes — 769 share u=-0.0000 |
| 95% | 950 | 50 | -0.0000 | yes — 769 share u=-0.0000 |

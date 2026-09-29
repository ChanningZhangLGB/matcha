# labelme / confidence — rank-based splits (minicpm-v-8b-2.6-q8_0)

1,000 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **28**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 50 | 950 | 0.2222 | no |
| 10% | 100 | 900 | 0.1889 | yes — 36 share u=0.1889 |
| 15% | 150 | 850 | 0.1667 | yes — 26 share u=0.1667 |
| 20% | 200 | 800 | 0.1444 | yes — 47 share u=0.1444 |
| 25% | 250 | 750 | 0.1333 | yes — 54 share u=0.1333 |
| 30% | 300 | 700 | 0.1222 | yes — 48 share u=0.1222 |
| 35% | 350 | 650 | 0.1111 | yes — 83 share u=0.1111 |
| 40% | 400 | 600 | 0.1111 | yes — 83 share u=0.1111 |
| 45% | 450 | 550 | 0.1000 | yes — 76 share u=0.1000 |
| 50% | 500 | 500 | 0.1000 | yes — 76 share u=0.1000 |
| 55% | 550 | 450 | 0.0889 | yes — 90 share u=0.0889 |
| 60% | 600 | 400 | 0.0778 | yes — 277 share u=0.0778 |
| 65% | 650 | 350 | 0.0778 | yes — 277 share u=0.0778 |
| 70% | 700 | 300 | 0.0778 | yes — 277 share u=0.0778 |
| 75% | 750 | 250 | 0.0778 | yes — 277 share u=0.0778 |
| 80% | 800 | 200 | 0.0778 | yes — 277 share u=0.0778 |
| 85% | 850 | 150 | 0.0778 | yes — 277 share u=0.0778 |
| 90% | 900 | 100 | 0.0722 | yes — 37 share u=0.0722 |
| 95% | 950 | 50 | 0.0667 | yes — 74 share u=0.0667 |

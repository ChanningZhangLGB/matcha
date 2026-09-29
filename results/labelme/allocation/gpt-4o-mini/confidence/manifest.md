# labelme / confidence — rank-based splits (gpt-4o-mini)

1,000 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **38**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 50 | 950 | 0.2000 | yes — 31 share u=0.2000 |
| 10% | 100 | 900 | 0.1778 | yes — 32 share u=0.1778 |
| 15% | 150 | 850 | 0.1667 | yes — 55 share u=0.1667 |
| 20% | 200 | 800 | 0.1667 | yes — 55 share u=0.1667 |
| 25% | 250 | 750 | 0.1556 | no |
| 30% | 300 | 700 | 0.1444 | yes — 29 share u=0.1444 |
| 35% | 350 | 650 | 0.1389 | yes — 45 share u=0.1389 |
| 40% | 400 | 600 | 0.1333 | yes — 83 share u=0.1333 |
| 45% | 450 | 550 | 0.1278 | yes — 35 share u=0.1278 |
| 50% | 500 | 500 | 0.1222 | yes — 65 share u=0.1222 |
| 55% | 550 | 450 | 0.1167 | yes — 34 share u=0.1167 |
| 60% | 600 | 400 | 0.1111 | yes — 32 share u=0.1111 |
| 65% | 650 | 350 | 0.1056 | yes — 42 share u=0.1056 |
| 70% | 700 | 300 | 0.0944 | yes — 54 share u=0.0944 |
| 75% | 750 | 250 | 0.0944 | yes — 54 share u=0.0944 |
| 80% | 800 | 200 | 0.0833 | yes — 31 share u=0.0833 |
| 85% | 850 | 150 | 0.0778 | yes — 47 share u=0.0778 |
| 90% | 900 | 100 | 0.0722 | yes — 51 share u=0.0722 |
| 95% | 950 | 50 | 0.0667 | yes — 68 share u=0.0667 |

# labelme / confidence — rank-based splits (qwen2.5vl-7b-q8_0)

1,000 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **28**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 50 | 950 | 0.1611 | yes — 8 share u=0.1611 |
| 10% | 100 | 900 | 0.1444 | yes — 25 share u=0.1444 |
| 15% | 150 | 850 | 0.1333 | yes — 37 share u=0.1333 |
| 20% | 200 | 800 | 0.1222 | yes — 59 share u=0.1222 |
| 25% | 250 | 750 | 0.1222 | yes — 59 share u=0.1222 |
| 30% | 300 | 700 | 0.1111 | yes — 130 share u=0.1111 |
| 35% | 350 | 650 | 0.1111 | yes — 130 share u=0.1111 |
| 40% | 400 | 600 | 0.1111 | yes — 130 share u=0.1111 |
| 45% | 450 | 550 | 0.1000 | yes — 391 share u=0.1000 |
| 50% | 500 | 500 | 0.1000 | yes — 391 share u=0.1000 |
| 55% | 550 | 450 | 0.1000 | yes — 391 share u=0.1000 |
| 60% | 600 | 400 | 0.1000 | yes — 391 share u=0.1000 |
| 65% | 650 | 350 | 0.1000 | yes — 391 share u=0.1000 |
| 70% | 700 | 300 | 0.1000 | yes — 391 share u=0.1000 |
| 75% | 750 | 250 | 0.1000 | yes — 391 share u=0.1000 |
| 80% | 800 | 200 | 0.1000 | yes — 391 share u=0.1000 |
| 85% | 850 | 150 | 0.0944 | yes — 63 share u=0.0944 |
| 90% | 900 | 100 | 0.0889 | yes — 37 share u=0.0889 |
| 95% | 950 | 50 | 0.0778 | yes — 22 share u=0.0778 |

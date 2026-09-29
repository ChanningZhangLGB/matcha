# imagenet16h / confidence — rank-based splits (minicpm-v-8b-2.6-q8_0)

4,800 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **95**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 240 | 4,560 | 0.6111 | yes — 38 share u=0.6111 |
| 10% | 480 | 4,320 | 0.5556 | yes — 363 share u=0.5556 |
| 15% | 720 | 4,080 | 0.5556 | yes — 363 share u=0.5556 |
| 20% | 960 | 3,840 | 0.5333 | yes — 126 share u=0.5333 |
| 25% | 1,200 | 3,600 | 0.5111 | yes — 56 share u=0.5111 |
| 30% | 1,440 | 3,360 | 0.4611 | no |
| 35% | 1,680 | 3,120 | 0.4111 | yes — 69 share u=0.4111 |
| 40% | 1,920 | 2,880 | 0.3667 | yes — 37 share u=0.3667 |
| 45% | 2,160 | 2,640 | 0.3167 | yes — 28 share u=0.3167 |
| 50% | 2,400 | 2,400 | 0.2833 | yes — 53 share u=0.2833 |
| 55% | 2,640 | 2,160 | 0.2667 | yes — 85 share u=0.2667 |
| 60% | 2,880 | 1,920 | 0.2500 | yes — 60 share u=0.2500 |
| 65% | 3,120 | 1,680 | 0.2278 | yes — 48 share u=0.2278 |
| 70% | 3,360 | 1,440 | 0.2111 | yes — 200 share u=0.2111 |
| 75% | 3,600 | 1,200 | 0.2000 | yes — 507 share u=0.2000 |
| 80% | 3,840 | 960 | 0.2000 | yes — 507 share u=0.2000 |
| 85% | 4,080 | 720 | 0.2000 | yes — 507 share u=0.2000 |
| 90% | 4,320 | 480 | 0.1778 | yes — 152 share u=0.1778 |
| 95% | 4,560 | 240 | 0.1556 | yes — 89 share u=0.1556 |

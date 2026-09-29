# imagenet16h / entropy — rank-based splits (minicpm-v-8b-2.6-q8_0)

4,800 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **25**

⚠️ **2,629 instances (54.8%) sit at u = 0.** Any cut beyond the 45.2% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 240 | 4,560 | 1.2730 | yes — 68 share u=1.2730 |
| 10% | 480 | 4,320 | 1.1491 | yes — 196 share u=1.1491 |
| 15% | 720 | 4,080 | 1.0027 | yes — 42 share u=1.0027 |
| 20% | 960 | 3,840 | 0.9369 | yes — 207 share u=0.9369 |
| 25% | 1,200 | 3,600 | 0.8487 | yes — 237 share u=0.8487 |
| 30% | 1,440 | 3,360 | 0.6837 | yes — 40 share u=0.6837 |
| 35% | 1,680 | 3,120 | 0.6365 | yes — 348 share u=0.6365 |
| 40% | 1,920 | 2,880 | 0.5297 | yes — 141 share u=0.5297 |
| 45% | 2,160 | 2,640 | 0.3488 | yes — 241 share u=0.3488 |
| 50% | 2,400 | 2,400 | -0.0000 | yes — 2,629 share u=-0.0000 |
| 55% | 2,640 | 2,160 | -0.0000 | yes — 2,629 share u=-0.0000 |
| 60% | 2,880 | 1,920 | -0.0000 | yes — 2,629 share u=-0.0000 |
| 65% | 3,120 | 1,680 | -0.0000 | yes — 2,629 share u=-0.0000 |
| 70% | 3,360 | 1,440 | -0.0000 | yes — 2,629 share u=-0.0000 |
| 75% | 3,600 | 1,200 | -0.0000 | yes — 2,629 share u=-0.0000 |
| 80% | 3,840 | 960 | -0.0000 | yes — 2,629 share u=-0.0000 |
| 85% | 4,080 | 720 | -0.0000 | yes — 2,629 share u=-0.0000 |
| 90% | 4,320 | 480 | -0.0000 | yes — 2,629 share u=-0.0000 |
| 95% | 4,560 | 240 | -0.0000 | yes — 2,629 share u=-0.0000 |

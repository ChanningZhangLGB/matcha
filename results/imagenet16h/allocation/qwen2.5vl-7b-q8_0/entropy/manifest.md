# imagenet16h / entropy — rank-based splits (qwen2.5vl-7b-q8_0)

4,800 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **27**

⚠️ **2,694 instances (56.1%) sit at u = 0.** Any cut beyond the 43.9% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 240 | 4,560 | 1.3031 | yes — 12 share u=1.3031 |
| 10% | 480 | 4,320 | 1.1491 | yes — 123 share u=1.1491 |
| 15% | 720 | 4,080 | 0.9950 | yes — 62 share u=0.9950 |
| 20% | 960 | 3,840 | 0.8487 | yes — 211 share u=0.8487 |
| 25% | 1,200 | 3,600 | 0.6870 | yes — 112 share u=0.6870 |
| 30% | 1,440 | 3,360 | 0.6365 | yes — 195 share u=0.6365 |
| 35% | 1,680 | 3,120 | 0.5297 | yes — 259 share u=0.5297 |
| 40% | 1,920 | 2,880 | 0.3488 | yes — 316 share u=0.3488 |
| 45% | 2,160 | 2,640 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 50% | 2,400 | 2,400 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 55% | 2,640 | 2,160 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 60% | 2,880 | 1,920 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 65% | 3,120 | 1,680 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 70% | 3,360 | 1,440 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 75% | 3,600 | 1,200 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 80% | 3,840 | 960 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 85% | 4,080 | 720 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 90% | 4,320 | 480 | -0.0000 | yes — 2,694 share u=-0.0000 |
| 95% | 4,560 | 240 | -0.0000 | yes — 2,694 share u=-0.0000 |

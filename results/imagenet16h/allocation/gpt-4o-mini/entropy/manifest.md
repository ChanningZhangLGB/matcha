# imagenet16h / entropy — rank-based splits (gpt-4o-mini)

4,800 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **27**

⚠️ **3,415 instances (71.1%) sit at u = 0.** Any cut beyond the 28.9% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 240 | 4,560 | 1.3689 | yes — 14 share u=1.3689 |
| 10% | 480 | 4,320 | 1.1491 | yes — 85 share u=1.1491 |
| 15% | 720 | 4,080 | 0.9369 | yes — 66 share u=0.9369 |
| 20% | 960 | 3,840 | 0.6365 | yes — 51 share u=0.6365 |
| 25% | 1,200 | 3,600 | 0.3488 | yes — 287 share u=0.3488 |
| 30% | 1,440 | 3,360 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 35% | 1,680 | 3,120 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 40% | 1,920 | 2,880 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 45% | 2,160 | 2,640 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 50% | 2,400 | 2,400 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 55% | 2,640 | 2,160 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 60% | 2,880 | 1,920 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 65% | 3,120 | 1,680 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 70% | 3,360 | 1,440 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 75% | 3,600 | 1,200 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 80% | 3,840 | 960 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 85% | 4,080 | 720 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 90% | 4,320 | 480 | -0.0000 | yes — 3,415 share u=-0.0000 |
| 95% | 4,560 | 240 | -0.0000 | yes — 3,415 share u=-0.0000 |

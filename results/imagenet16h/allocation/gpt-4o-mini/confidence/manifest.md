# imagenet16h / confidence — rank-based splits (gpt-4o-mini)

4,800 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **122**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 240 | 4,560 | 0.5500 | yes — 15 share u=0.5500 |
| 10% | 480 | 4,320 | 0.4722 | yes — 23 share u=0.4722 |
| 15% | 720 | 4,080 | 0.3944 | yes — 26 share u=0.3944 |
| 20% | 960 | 3,840 | 0.3444 | no |
| 25% | 1,200 | 3,600 | 0.3000 | yes — 44 share u=0.3000 |
| 30% | 1,440 | 3,360 | 0.2778 | yes — 79 share u=0.2778 |
| 35% | 1,680 | 3,120 | 0.2556 | yes — 32 share u=0.2556 |
| 40% | 1,920 | 2,880 | 0.2278 | yes — 47 share u=0.2278 |
| 45% | 2,160 | 2,640 | 0.2000 | yes — 70 share u=0.2000 |
| 50% | 2,400 | 2,400 | 0.1833 | yes — 66 share u=0.1833 |
| 55% | 2,640 | 2,160 | 0.1722 | yes — 180 share u=0.1722 |
| 60% | 2,880 | 1,920 | 0.1667 | yes — 265 share u=0.1667 |
| 65% | 3,120 | 1,680 | 0.1611 | yes — 382 share u=0.1611 |
| 70% | 3,360 | 1,440 | 0.1611 | yes — 382 share u=0.1611 |
| 75% | 3,600 | 1,200 | 0.1500 | yes — 176 share u=0.1500 |
| 80% | 3,840 | 960 | 0.1444 | yes — 136 share u=0.1444 |
| 85% | 4,080 | 720 | 0.1333 | yes — 164 share u=0.1333 |
| 90% | 4,320 | 480 | 0.1222 | yes — 109 share u=0.1222 |
| 95% | 4,560 | 240 | 0.1056 | yes — 81 share u=0.1056 |

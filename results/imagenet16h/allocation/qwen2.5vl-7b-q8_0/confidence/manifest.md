# imagenet16h / confidence — rank-based splits (qwen2.5vl-7b-q8_0)

4,800 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **57**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 240 | 4,560 | 0.3222 | yes — 72 share u=0.3222 |
| 10% | 480 | 4,320 | 0.3000 | yes — 260 share u=0.3000 |
| 15% | 720 | 4,080 | 0.2889 | yes — 322 share u=0.2889 |
| 20% | 960 | 3,840 | 0.2889 | yes — 322 share u=0.2889 |
| 25% | 1,200 | 3,600 | 0.2778 | yes — 328 share u=0.2778 |
| 30% | 1,440 | 3,360 | 0.2667 | yes — 344 share u=0.2667 |
| 35% | 1,680 | 3,120 | 0.2667 | yes — 344 share u=0.2667 |
| 40% | 1,920 | 2,880 | 0.2556 | yes — 304 share u=0.2556 |
| 45% | 2,160 | 2,640 | 0.2444 | yes — 369 share u=0.2444 |
| 50% | 2,400 | 2,400 | 0.2444 | yes — 369 share u=0.2444 |
| 55% | 2,640 | 2,160 | 0.2333 | yes — 447 share u=0.2333 |
| 60% | 2,880 | 1,920 | 0.2333 | yes — 447 share u=0.2333 |
| 65% | 3,120 | 1,680 | 0.2222 | yes — 467 share u=0.2222 |
| 70% | 3,360 | 1,440 | 0.2222 | yes — 467 share u=0.2222 |
| 75% | 3,600 | 1,200 | 0.2111 | yes — 150 share u=0.2111 |
| 80% | 3,840 | 960 | 0.2000 | yes — 95 share u=0.2000 |
| 85% | 4,080 | 720 | 0.1667 | yes — 68 share u=0.1667 |
| 90% | 4,320 | 480 | 0.1444 | yes — 125 share u=0.1444 |
| 95% | 4,560 | 240 | 0.1278 | yes — 57 share u=0.1278 |

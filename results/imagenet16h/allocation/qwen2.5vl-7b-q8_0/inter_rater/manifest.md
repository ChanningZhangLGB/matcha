# imagenet16h / inter_rater — rank-based splits (qwen2.5vl-7b-q8_0)

4,800 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **19**

⚠️ **2,694 instances (56.1%) sit at u = 0.** Any cut beyond the 43.9% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 240 | 4,560 | 0.7778 | yes — 94 share u=0.7778 |
| 10% | 480 | 4,320 | 0.7222 | yes — 124 share u=0.7222 |
| 15% | 720 | 4,080 | 0.6667 | yes — 101 share u=0.6667 |
| 20% | 960 | 3,840 | 0.5556 | yes — 323 share u=0.5556 |
| 25% | 1,200 | 3,600 | 0.5556 | yes — 323 share u=0.5556 |
| 30% | 1,440 | 3,360 | 0.4167 | yes — 117 share u=0.4167 |
| 35% | 1,680 | 3,120 | 0.3889 | yes — 259 share u=0.3889 |
| 40% | 1,920 | 2,880 | 0.2222 | yes — 316 share u=0.2222 |
| 45% | 2,160 | 2,640 | 0.0000 | yes — 2,694 share u=0.0000 |
| 50% | 2,400 | 2,400 | 0.0000 | yes — 2,694 share u=0.0000 |
| 55% | 2,640 | 2,160 | 0.0000 | yes — 2,694 share u=0.0000 |
| 60% | 2,880 | 1,920 | 0.0000 | yes — 2,694 share u=0.0000 |
| 65% | 3,120 | 1,680 | 0.0000 | yes — 2,694 share u=0.0000 |
| 70% | 3,360 | 1,440 | 0.0000 | yes — 2,694 share u=0.0000 |
| 75% | 3,600 | 1,200 | 0.0000 | yes — 2,694 share u=0.0000 |
| 80% | 3,840 | 960 | 0.0000 | yes — 2,694 share u=0.0000 |
| 85% | 4,080 | 720 | 0.0000 | yes — 2,694 share u=0.0000 |
| 90% | 4,320 | 480 | 0.0000 | yes — 2,694 share u=0.0000 |
| 95% | 4,560 | 240 | 0.0000 | yes — 2,694 share u=0.0000 |

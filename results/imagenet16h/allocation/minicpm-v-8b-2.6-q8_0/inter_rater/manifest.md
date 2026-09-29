# imagenet16h / inter_rater — rank-based splits (minicpm-v-8b-2.6-q8_0)

4,800 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **18**

⚠️ **2,629 instances (54.8%) sit at u = 0.** Any cut beyond the 45.2% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 240 | 4,560 | 0.7778 | yes — 68 share u=0.7778 |
| 10% | 480 | 4,320 | 0.7222 | yes — 125 share u=0.7222 |
| 15% | 720 | 4,080 | 0.6667 | yes — 135 share u=0.6667 |
| 20% | 960 | 3,840 | 0.6389 | yes — 207 share u=0.6389 |
| 25% | 1,200 | 3,600 | 0.5556 | yes — 314 share u=0.5556 |
| 30% | 1,440 | 3,360 | 0.5000 | yes — 348 share u=0.5000 |
| 35% | 1,680 | 3,120 | 0.5000 | yes — 348 share u=0.5000 |
| 40% | 1,920 | 2,880 | 0.3889 | yes — 141 share u=0.3889 |
| 45% | 2,160 | 2,640 | 0.2222 | yes — 241 share u=0.2222 |
| 50% | 2,400 | 2,400 | 0.0000 | yes — 2,629 share u=0.0000 |
| 55% | 2,640 | 2,160 | 0.0000 | yes — 2,629 share u=0.0000 |
| 60% | 2,880 | 1,920 | 0.0000 | yes — 2,629 share u=0.0000 |
| 65% | 3,120 | 1,680 | 0.0000 | yes — 2,629 share u=0.0000 |
| 70% | 3,360 | 1,440 | 0.0000 | yes — 2,629 share u=0.0000 |
| 75% | 3,600 | 1,200 | 0.0000 | yes — 2,629 share u=0.0000 |
| 80% | 3,840 | 960 | 0.0000 | yes — 2,629 share u=0.0000 |
| 85% | 4,080 | 720 | 0.0000 | yes — 2,629 share u=0.0000 |
| 90% | 4,320 | 480 | 0.0000 | yes — 2,629 share u=0.0000 |
| 95% | 4,560 | 240 | 0.0000 | yes — 2,629 share u=0.0000 |

# crowdtruth_pooled / confidence — rank-based splits (qwen2.5-7b-instruct-q8_0)

1,596 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **34**

⚠️ **57 instances (3.6%) sit at u = 0.** Any cut beyond the 96.4% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 80 | 1,516 | 0.1500 | yes — 43 share u=0.1500 |
| 10% | 160 | 1,436 | 0.1389 | yes — 70 share u=0.1389 |
| 15% | 239 | 1,357 | 0.1333 | yes — 89 share u=0.1333 |
| 20% | 319 | 1,277 | 0.1278 | yes — 88 share u=0.1278 |
| 25% | 399 | 1,197 | 0.1222 | yes — 85 share u=0.1222 |
| 30% | 479 | 1,117 | 0.1222 | yes — 85 share u=0.1222 |
| 35% | 559 | 1,037 | 0.1167 | yes — 142 share u=0.1167 |
| 40% | 638 | 958 | 0.1111 | yes — 100 share u=0.1111 |
| 45% | 718 | 878 | 0.1111 | yes — 100 share u=0.1111 |
| 50% | 798 | 798 | 0.1000 | yes — 92 share u=0.1000 |
| 55% | 878 | 718 | 0.1000 | yes — 92 share u=0.1000 |
| 60% | 958 | 638 | 0.0889 | yes — 72 share u=0.0889 |
| 65% | 1,037 | 559 | 0.0833 | yes — 77 share u=0.0833 |
| 70% | 1,117 | 479 | 0.0778 | yes — 57 share u=0.0778 |
| 75% | 1,197 | 399 | 0.0667 | yes — 46 share u=0.0667 |
| 80% | 1,277 | 319 | 0.0611 | yes — 46 share u=0.0611 |
| 85% | 1,357 | 239 | 0.0444 | yes — 25 share u=0.0444 |
| 90% | 1,436 | 160 | 0.0333 | yes — 16 share u=0.0333 |
| 95% | 1,516 | 80 | 0.0167 | yes — 25 share u=0.0167 |

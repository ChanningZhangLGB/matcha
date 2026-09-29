# crowdtruth_treat / confidence — rank-based splits (qwen2.5-7b-instruct-q8_0)

621 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **34**

⚠️ **25 instances (4.0%) sit at u = 0.** Any cut beyond the 96.0% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 31 | 590 | 0.1500 | yes — 13 share u=0.1500 |
| 10% | 62 | 559 | 0.1389 | yes — 28 share u=0.1389 |
| 15% | 93 | 528 | 0.1333 | yes — 32 share u=0.1333 |
| 20% | 124 | 497 | 0.1278 | yes — 33 share u=0.1278 |
| 25% | 155 | 466 | 0.1222 | yes — 31 share u=0.1222 |
| 30% | 186 | 435 | 0.1167 | yes — 56 share u=0.1167 |
| 35% | 217 | 404 | 0.1167 | yes — 56 share u=0.1167 |
| 40% | 248 | 373 | 0.1111 | yes — 39 share u=0.1111 |
| 45% | 279 | 342 | 0.1056 | yes — 24 share u=0.1056 |
| 50% | 310 | 311 | 0.1000 | yes — 36 share u=0.1000 |
| 55% | 342 | 279 | 0.0944 | yes — 24 share u=0.0944 |
| 60% | 373 | 248 | 0.0889 | yes — 31 share u=0.0889 |
| 65% | 404 | 217 | 0.0833 | yes — 33 share u=0.0833 |
| 70% | 435 | 186 | 0.0778 | yes — 24 share u=0.0778 |
| 75% | 466 | 155 | 0.0667 | yes — 20 share u=0.0667 |
| 80% | 497 | 124 | 0.0556 | yes — 15 share u=0.0556 |
| 85% | 528 | 93 | 0.0444 | yes — 10 share u=0.0444 |
| 90% | 559 | 62 | 0.0278 | yes — 10 share u=0.0278 |
| 95% | 590 | 31 | 0.0167 | yes — 10 share u=0.0167 |

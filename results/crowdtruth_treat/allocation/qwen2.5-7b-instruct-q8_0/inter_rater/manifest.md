# crowdtruth_treat / inter_rater — rank-based splits (qwen2.5-7b-instruct-q8_0)

621 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **5** (heavily tied)

⚠️ **447 instances (72.0%) sit at u = 0.** Any cut beyond the 28.0% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 31 | 590 | 0.5000 | yes — 32 share u=0.5000 |
| 10% | 62 | 559 | 0.3889 | yes — 48 share u=0.3889 |
| 15% | 93 | 528 | 0.3889 | yes — 48 share u=0.3889 |
| 20% | 124 | 497 | 0.2222 | yes — 68 share u=0.2222 |
| 25% | 155 | 466 | 0.2222 | yes — 68 share u=0.2222 |
| 30% | 186 | 435 | 0.0000 | yes — 447 share u=0.0000 |
| 35% | 217 | 404 | 0.0000 | yes — 447 share u=0.0000 |
| 40% | 248 | 373 | 0.0000 | yes — 447 share u=0.0000 |
| 45% | 279 | 342 | 0.0000 | yes — 447 share u=0.0000 |
| 50% | 310 | 311 | 0.0000 | yes — 447 share u=0.0000 |
| 55% | 342 | 279 | 0.0000 | yes — 447 share u=0.0000 |
| 60% | 373 | 248 | 0.0000 | yes — 447 share u=0.0000 |
| 65% | 404 | 217 | 0.0000 | yes — 447 share u=0.0000 |
| 70% | 435 | 186 | 0.0000 | yes — 447 share u=0.0000 |
| 75% | 466 | 155 | 0.0000 | yes — 447 share u=0.0000 |
| 80% | 497 | 124 | 0.0000 | yes — 447 share u=0.0000 |
| 85% | 528 | 93 | 0.0000 | yes — 447 share u=0.0000 |
| 90% | 559 | 62 | 0.0000 | yes — 447 share u=0.0000 |
| 95% | 590 | 31 | 0.0000 | yes — 447 share u=0.0000 |

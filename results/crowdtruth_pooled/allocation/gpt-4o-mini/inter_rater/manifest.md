# crowdtruth_pooled / inter_rater — rank-based splits (gpt-4o-mini)

1,596 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **5** (heavily tied)

⚠️ **1,264 instances (79.2%) sit at u = 0.** Any cut beyond the 20.8% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 80 | 1,516 | 0.5000 | yes — 73 share u=0.5000 |
| 10% | 160 | 1,436 | 0.3889 | yes — 91 share u=0.3889 |
| 15% | 239 | 1,357 | 0.2222 | yes — 106 share u=0.2222 |
| 20% | 319 | 1,277 | 0.2222 | yes — 106 share u=0.2222 |
| 25% | 399 | 1,197 | 0.0000 | yes — 1,264 share u=0.0000 |
| 30% | 479 | 1,117 | 0.0000 | yes — 1,264 share u=0.0000 |
| 35% | 559 | 1,037 | 0.0000 | yes — 1,264 share u=0.0000 |
| 40% | 638 | 958 | 0.0000 | yes — 1,264 share u=0.0000 |
| 45% | 718 | 878 | 0.0000 | yes — 1,264 share u=0.0000 |
| 50% | 798 | 798 | 0.0000 | yes — 1,264 share u=0.0000 |
| 55% | 878 | 718 | 0.0000 | yes — 1,264 share u=0.0000 |
| 60% | 958 | 638 | 0.0000 | yes — 1,264 share u=0.0000 |
| 65% | 1,037 | 559 | 0.0000 | yes — 1,264 share u=0.0000 |
| 70% | 1,117 | 479 | 0.0000 | yes — 1,264 share u=0.0000 |
| 75% | 1,197 | 399 | 0.0000 | yes — 1,264 share u=0.0000 |
| 80% | 1,277 | 319 | 0.0000 | yes — 1,264 share u=0.0000 |
| 85% | 1,357 | 239 | 0.0000 | yes — 1,264 share u=0.0000 |
| 90% | 1,436 | 160 | 0.0000 | yes — 1,264 share u=0.0000 |
| 95% | 1,516 | 80 | 0.0000 | yes — 1,264 share u=0.0000 |

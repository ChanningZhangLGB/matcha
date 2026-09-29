# sentiment / inter_rater — rank-based splits (qwen2.5-7b-instruct-q8_0)

4,999 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **8** (heavily tied)

⚠️ **3,959 instances (79.2%) sit at u = 0.** Any cut beyond the 20.8% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 250 | 4,749 | 0.4848 | yes — 132 share u=0.4848 |
| 10% | 500 | 4,499 | 0.3030 | yes — 208 share u=0.3030 |
| 15% | 750 | 4,249 | 0.1667 | yes — 334 share u=0.1667 |
| 20% | 1,000 | 3,999 | 0.1667 | yes — 334 share u=0.1667 |
| 25% | 1,250 | 3,749 | 0.0000 | yes — 3,959 share u=0.0000 |
| 30% | 1,500 | 3,499 | 0.0000 | yes — 3,959 share u=0.0000 |
| 35% | 1,750 | 3,249 | 0.0000 | yes — 3,959 share u=0.0000 |
| 40% | 2,000 | 2,999 | 0.0000 | yes — 3,959 share u=0.0000 |
| 45% | 2,250 | 2,749 | 0.0000 | yes — 3,959 share u=0.0000 |
| 50% | 2,500 | 2,499 | 0.0000 | yes — 3,959 share u=0.0000 |
| 55% | 2,749 | 2,250 | 0.0000 | yes — 3,959 share u=0.0000 |
| 60% | 2,999 | 2,000 | 0.0000 | yes — 3,959 share u=0.0000 |
| 65% | 3,249 | 1,750 | 0.0000 | yes — 3,959 share u=0.0000 |
| 70% | 3,499 | 1,500 | 0.0000 | yes — 3,959 share u=0.0000 |
| 75% | 3,749 | 1,250 | 0.0000 | yes — 3,959 share u=0.0000 |
| 80% | 3,999 | 1,000 | 0.0000 | yes — 3,959 share u=0.0000 |
| 85% | 4,249 | 750 | 0.0000 | yes — 3,959 share u=0.0000 |
| 90% | 4,499 | 500 | 0.0000 | yes — 3,959 share u=0.0000 |
| 95% | 4,749 | 250 | 0.0000 | yes — 3,959 share u=0.0000 |

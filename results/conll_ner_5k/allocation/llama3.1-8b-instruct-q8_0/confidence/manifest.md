# conll_ner_5k / confidence — rank-based splits (llama3.1-8b-instruct-q8_0)

4,956 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **162**

⚠️ **1,470 instances (29.7%) sit at u = 0.** Any cut beyond the 70.3% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 248 | 4,708 | 0.4000 | yes — 32 share u=0.4000 |
| 10% | 496 | 4,460 | 0.2500 | yes — 67 share u=0.2500 |
| 15% | 743 | 4,213 | 0.2000 | yes — 458 share u=0.2000 |
| 20% | 991 | 3,965 | 0.2000 | yes — 458 share u=0.2000 |
| 25% | 1,239 | 3,717 | 0.1667 | yes — 185 share u=0.1667 |
| 30% | 1,487 | 3,469 | 0.1333 | yes — 312 share u=0.1333 |
| 35% | 1,735 | 3,221 | 0.1250 | yes — 44 share u=0.1250 |
| 40% | 1,982 | 2,974 | 0.1000 | yes — 633 share u=0.1000 |
| 45% | 2,230 | 2,726 | 0.1000 | yes — 633 share u=0.1000 |
| 50% | 2,478 | 2,478 | 0.0800 | yes — 39 share u=0.0800 |
| 55% | 2,726 | 2,230 | 0.0667 | yes — 287 share u=0.0667 |
| 60% | 2,974 | 1,982 | 0.0500 | yes — 195 share u=0.0500 |
| 65% | 3,221 | 1,735 | 0.0375 | yes — 18 share u=0.0375 |
| 70% | 3,469 | 1,487 | 0.0125 | yes — 10 share u=0.0125 |
| 75% | 3,717 | 1,239 | 0.0000 | yes — 1,470 share u=0.0000 |
| 80% | 3,965 | 991 | 0.0000 | yes — 1,470 share u=0.0000 |
| 85% | 4,213 | 743 | 0.0000 | yes — 1,470 share u=0.0000 |
| 90% | 4,460 | 496 | 0.0000 | yes — 1,470 share u=0.0000 |
| 95% | 4,708 | 248 | 0.0000 | yes — 1,470 share u=0.0000 |

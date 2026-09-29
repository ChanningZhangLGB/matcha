# conll_ner_5k / entropy — rank-based splits (llama3.1-8b-instruct-q8_0)

4,956 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **59**

⚠️ **3,030 instances (61.1%) sit at u = 0.** Any cut beyond the 38.9% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 248 | 4,708 | 1.0609 | yes — 12 share u=1.0609 |
| 10% | 496 | 4,460 | 0.8487 | yes — 17 share u=0.8487 |
| 15% | 743 | 4,213 | 0.6931 | yes — 361 share u=0.6931 |
| 20% | 991 | 3,965 | 0.6730 | yes — 60 share u=0.6730 |
| 25% | 1,239 | 3,717 | 0.6365 | yes — 396 share u=0.6365 |
| 30% | 1,487 | 3,469 | 0.5623 | yes — 140 share u=0.5623 |
| 35% | 1,735 | 3,221 | 0.4506 | yes — 79 share u=0.4506 |
| 40% | 1,982 | 2,974 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 45% | 2,230 | 2,726 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 50% | 2,478 | 2,478 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 55% | 2,726 | 2,230 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 60% | 2,974 | 1,982 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 65% | 3,221 | 1,735 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 70% | 3,469 | 1,487 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 75% | 3,717 | 1,239 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 80% | 3,965 | 991 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 85% | 4,213 | 743 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 90% | 4,460 | 496 | -0.0000 | yes — 3,030 share u=-0.0000 |
| 95% | 4,708 | 248 | -0.0000 | yes — 3,030 share u=-0.0000 |

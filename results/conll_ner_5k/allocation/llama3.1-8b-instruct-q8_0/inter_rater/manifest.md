# conll_ner_5k / inter_rater — rank-based splits (llama3.1-8b-instruct-q8_0)

4,470 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **47**

⚠️ **2,544 instances (56.9%) sit at u = 0.** Any cut beyond the 43.1% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 224 | 4,246 | 1.0000 | yes — 438 share u=1.0000 |
| 10% | 447 | 4,023 | 0.9000 | yes — 7 share u=0.9000 |
| 15% | 670 | 3,800 | 0.7000 | yes — 29 share u=0.7000 |
| 20% | 894 | 3,576 | 0.6667 | yes — 425 share u=0.6667 |
| 25% | 1,118 | 3,352 | 0.6667 | yes — 425 share u=0.6667 |
| 30% | 1,341 | 3,129 | 0.5357 | no |
| 35% | 1,564 | 2,906 | 0.4286 | yes — 34 share u=0.4286 |
| 40% | 1,788 | 2,682 | 0.2857 | yes — 83 share u=0.2857 |
| 45% | 2,012 | 2,458 | 0.0000 | yes — 2,544 share u=0.0000 |
| 50% | 2,235 | 2,235 | 0.0000 | yes — 2,544 share u=0.0000 |
| 55% | 2,458 | 2,012 | 0.0000 | yes — 2,544 share u=0.0000 |
| 60% | 2,682 | 1,788 | 0.0000 | yes — 2,544 share u=0.0000 |
| 65% | 2,906 | 1,564 | 0.0000 | yes — 2,544 share u=0.0000 |
| 70% | 3,129 | 1,341 | 0.0000 | yes — 2,544 share u=0.0000 |
| 75% | 3,352 | 1,118 | 0.0000 | yes — 2,544 share u=0.0000 |
| 80% | 3,576 | 894 | 0.0000 | yes — 2,544 share u=0.0000 |
| 85% | 3,800 | 670 | 0.0000 | yes — 2,544 share u=0.0000 |
| 90% | 4,023 | 447 | 0.0000 | yes — 2,544 share u=0.0000 |
| 95% | 4,246 | 224 | 0.0000 | yes — 2,544 share u=0.0000 |

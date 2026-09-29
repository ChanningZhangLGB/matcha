# sentiment / confidence — rank-based splits (qwen2.5-7b-instruct-q8_0)

4,999 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **78**

⚠️ **13 instances (0.3%) sit at u = 0.** Any cut beyond the 99.7% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 250 | 4,749 | 0.2417 | yes — 56 share u=0.2417 |
| 10% | 500 | 4,499 | 0.2167 | yes — 45 share u=0.2167 |
| 15% | 750 | 4,249 | 0.1958 | yes — 52 share u=0.1958 |
| 20% | 1,000 | 3,999 | 0.1833 | yes — 103 share u=0.1833 |
| 25% | 1,250 | 3,749 | 0.1667 | yes — 81 share u=0.1667 |
| 30% | 1,500 | 3,499 | 0.1542 | yes — 87 share u=0.1542 |
| 35% | 1,750 | 3,249 | 0.1417 | yes — 94 share u=0.1417 |
| 40% | 2,000 | 2,999 | 0.1292 | yes — 91 share u=0.1292 |
| 45% | 2,250 | 2,749 | 0.1167 | yes — 144 share u=0.1167 |
| 50% | 2,500 | 2,499 | 0.1125 | yes — 146 share u=0.1125 |
| 55% | 2,749 | 2,250 | 0.1042 | yes — 115 share u=0.1042 |
| 60% | 2,999 | 2,000 | 0.0958 | yes — 126 share u=0.0958 |
| 65% | 3,249 | 1,750 | 0.0875 | yes — 88 share u=0.0875 |
| 70% | 3,499 | 1,500 | 0.0750 | yes — 92 share u=0.0750 |
| 75% | 3,749 | 1,250 | 0.0667 | yes — 88 share u=0.0667 |
| 80% | 3,999 | 1,000 | 0.0542 | yes — 110 share u=0.0542 |
| 85% | 4,249 | 750 | 0.0417 | yes — 86 share u=0.0417 |
| 90% | 4,499 | 500 | 0.0333 | yes — 143 share u=0.0333 |
| 95% | 4,749 | 250 | 0.0292 | yes — 217 share u=0.0292 |

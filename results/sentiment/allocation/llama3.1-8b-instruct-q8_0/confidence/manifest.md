# sentiment / confidence — rank-based splits (llama3.1-8b-instruct-q8_0)

4,999 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **31**

⚠️ **115 instances (2.3%) sit at u = 0.** Any cut beyond the 97.7% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 250 | 4,749 | 0.2000 | yes — 307 share u=0.2000 |
| 10% | 500 | 4,499 | 0.1917 | yes — 190 share u=0.1917 |
| 15% | 750 | 4,249 | 0.1833 | yes — 285 share u=0.1833 |
| 20% | 1,000 | 3,999 | 0.1750 | yes — 231 share u=0.1750 |
| 25% | 1,250 | 3,749 | 0.1667 | yes — 321 share u=0.1667 |
| 30% | 1,500 | 3,499 | 0.1583 | yes — 348 share u=0.1583 |
| 35% | 1,750 | 3,249 | 0.1583 | yes — 348 share u=0.1583 |
| 40% | 2,000 | 2,999 | 0.1500 | yes — 322 share u=0.1500 |
| 45% | 2,250 | 2,749 | 0.1417 | yes — 324 share u=0.1417 |
| 50% | 2,500 | 2,499 | 0.1333 | yes — 331 share u=0.1333 |
| 55% | 2,749 | 2,250 | 0.1333 | yes — 331 share u=0.1333 |
| 60% | 2,999 | 2,000 | 0.1250 | yes — 313 share u=0.1250 |
| 65% | 3,249 | 1,750 | 0.1167 | yes — 265 share u=0.1167 |
| 70% | 3,499 | 1,500 | 0.1083 | yes — 185 share u=0.1083 |
| 75% | 3,749 | 1,250 | 0.0917 | yes — 126 share u=0.0917 |
| 80% | 3,999 | 1,000 | 0.0750 | yes — 93 share u=0.0750 |
| 85% | 4,249 | 750 | 0.0583 | yes — 123 share u=0.0583 |
| 90% | 4,499 | 500 | 0.0417 | yes — 112 share u=0.0417 |
| 95% | 4,749 | 250 | 0.0167 | yes — 78 share u=0.0167 |

# sentiment / confidence — rank-based splits (gpt-4o-mini)

4,999 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **61**

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 250 | 4,749 | 0.2250 | yes — 45 share u=0.2250 |
| 10% | 500 | 4,499 | 0.2000 | yes — 59 share u=0.2000 |
| 15% | 750 | 4,249 | 0.1833 | yes — 73 share u=0.1833 |
| 20% | 1,000 | 3,999 | 0.1708 | yes — 68 share u=0.1708 |
| 25% | 1,250 | 3,749 | 0.1542 | yes — 89 share u=0.1542 |
| 30% | 1,500 | 3,499 | 0.1417 | yes — 97 share u=0.1417 |
| 35% | 1,750 | 3,249 | 0.1333 | yes — 125 share u=0.1333 |
| 40% | 2,000 | 2,999 | 0.1250 | yes — 145 share u=0.1250 |
| 45% | 2,250 | 2,749 | 0.1167 | yes — 176 share u=0.1167 |
| 50% | 2,500 | 2,499 | 0.1125 | yes — 180 share u=0.1125 |
| 55% | 2,749 | 2,250 | 0.1042 | yes — 140 share u=0.1042 |
| 60% | 2,999 | 2,000 | 0.1000 | yes — 139 share u=0.1000 |
| 65% | 3,249 | 1,750 | 0.0917 | yes — 153 share u=0.0917 |
| 70% | 3,499 | 1,500 | 0.0833 | yes — 174 share u=0.0833 |
| 75% | 3,749 | 1,250 | 0.0792 | yes — 134 share u=0.0792 |
| 80% | 3,999 | 1,000 | 0.0708 | yes — 167 share u=0.0708 |
| 85% | 4,249 | 750 | 0.0667 | yes — 184 share u=0.0667 |
| 90% | 4,499 | 500 | 0.0583 | yes — 333 share u=0.0583 |
| 95% | 4,749 | 250 | 0.0583 | yes — 333 share u=0.0583 |

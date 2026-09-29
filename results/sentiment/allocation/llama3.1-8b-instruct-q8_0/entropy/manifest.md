# sentiment / entropy — rank-based splits (llama3.1-8b-instruct-q8_0)

4,999 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **7** (heavily tied)

⚠️ **3,498 instances (70.0%) sit at u = 0.** Any cut beyond the 30.0% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 250 | 4,749 | 0.6792 | yes — 159 share u=0.6792 |
| 10% | 500 | 4,499 | 0.5623 | yes — 242 share u=0.5623 |
| 15% | 750 | 4,249 | 0.4506 | yes — 271 share u=0.4506 |
| 20% | 1,000 | 3,999 | 0.2868 | yes — 533 share u=0.2868 |
| 25% | 1,250 | 3,749 | 0.2868 | yes — 533 share u=0.2868 |
| 30% | 1,500 | 3,499 | 0.2868 | yes — 533 share u=0.2868 |
| 35% | 1,750 | 3,249 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 40% | 2,000 | 2,999 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 45% | 2,250 | 2,749 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 50% | 2,500 | 2,499 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 55% | 2,749 | 2,250 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 60% | 2,999 | 2,000 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 65% | 3,249 | 1,750 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 70% | 3,499 | 1,500 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 75% | 3,749 | 1,250 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 80% | 3,999 | 1,000 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 85% | 4,249 | 750 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 90% | 4,499 | 500 | -0.0000 | yes — 3,498 share u=-0.0000 |
| 95% | 4,749 | 250 | -0.0000 | yes — 3,498 share u=-0.0000 |

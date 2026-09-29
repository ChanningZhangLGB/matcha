# conll_ner_5k / entropy — rank-based splits (gpt-4o-mini)

4,994 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **49**

⚠️ **4,275 instances (85.6%) sit at u = 0.** Any cut beyond the 14.4% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 250 | 4,744 | 0.6730 | yes — 29 share u=0.6730 |
| 10% | 499 | 4,495 | 0.5623 | yes — 84 share u=0.5623 |
| 15% | 749 | 4,245 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 20% | 999 | 3,995 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 25% | 1,248 | 3,746 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 30% | 1,498 | 3,496 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 35% | 1,748 | 3,246 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 40% | 1,998 | 2,996 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 45% | 2,247 | 2,747 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 50% | 2,497 | 2,497 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 55% | 2,747 | 2,247 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 60% | 2,996 | 1,998 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 65% | 3,246 | 1,748 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 70% | 3,496 | 1,498 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 75% | 3,746 | 1,248 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 80% | 3,995 | 999 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 85% | 4,245 | 749 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 90% | 4,495 | 499 | -0.0000 | yes — 4,275 share u=-0.0000 |
| 95% | 4,744 | 250 | -0.0000 | yes — 4,275 share u=-0.0000 |

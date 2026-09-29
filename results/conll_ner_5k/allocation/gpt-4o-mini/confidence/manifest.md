# conll_ner_5k / confidence — rank-based splits (gpt-4o-mini)

4,994 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **144**

⚠️ **114 instances (2.3%) sit at u = 0.** Any cut beyond the 97.7% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 250 | 4,744 | 0.1500 | yes — 53 share u=0.1500 |
| 10% | 499 | 4,495 | 0.1167 | yes — 60 share u=0.1167 |
| 15% | 749 | 4,245 | 0.0944 | yes — 28 share u=0.0944 |
| 20% | 999 | 3,995 | 0.0750 | yes — 74 share u=0.0750 |
| 25% | 1,248 | 3,746 | 0.0667 | yes — 1,138 share u=0.0667 |
| 30% | 1,498 | 3,496 | 0.0667 | yes — 1,138 share u=0.0667 |
| 35% | 1,748 | 3,246 | 0.0667 | yes — 1,138 share u=0.0667 |
| 40% | 1,998 | 2,996 | 0.0667 | yes — 1,138 share u=0.0667 |
| 45% | 2,247 | 2,747 | 0.0667 | yes — 1,138 share u=0.0667 |
| 50% | 2,497 | 2,497 | 0.0500 | yes — 975 share u=0.0500 |
| 55% | 2,747 | 2,247 | 0.0500 | yes — 975 share u=0.0500 |
| 60% | 2,996 | 1,998 | 0.0500 | yes — 975 share u=0.0500 |
| 65% | 3,246 | 1,748 | 0.0500 | yes — 975 share u=0.0500 |
| 70% | 3,496 | 1,498 | 0.0429 | yes — 43 share u=0.0429 |
| 75% | 3,746 | 1,248 | 0.0375 | yes — 161 share u=0.0375 |
| 80% | 3,995 | 999 | 0.0333 | yes — 334 share u=0.0333 |
| 85% | 4,245 | 749 | 0.0333 | yes — 334 share u=0.0333 |
| 90% | 4,495 | 499 | 0.0250 | yes — 142 share u=0.0250 |
| 95% | 4,744 | 250 | 0.0167 | yes — 106 share u=0.0167 |

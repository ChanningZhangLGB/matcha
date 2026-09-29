# conll_ner_5k / inter_rater — rank-based splits (gpt-4o-mini)

4,922 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **41**

⚠️ **4,203 instances (85.4%) sit at u = 0.** Any cut beyond the 14.6% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 246 | 4,676 | 0.6667 | yes — 156 share u=0.6667 |
| 10% | 492 | 4,430 | 0.5000 | yes — 103 share u=0.5000 |
| 15% | 738 | 4,184 | 0.0000 | yes — 4,203 share u=0.0000 |
| 20% | 984 | 3,938 | 0.0000 | yes — 4,203 share u=0.0000 |
| 25% | 1,230 | 3,692 | 0.0000 | yes — 4,203 share u=0.0000 |
| 30% | 1,477 | 3,445 | 0.0000 | yes — 4,203 share u=0.0000 |
| 35% | 1,723 | 3,199 | 0.0000 | yes — 4,203 share u=0.0000 |
| 40% | 1,969 | 2,953 | 0.0000 | yes — 4,203 share u=0.0000 |
| 45% | 2,215 | 2,707 | 0.0000 | yes — 4,203 share u=0.0000 |
| 50% | 2,461 | 2,461 | 0.0000 | yes — 4,203 share u=0.0000 |
| 55% | 2,707 | 2,215 | 0.0000 | yes — 4,203 share u=0.0000 |
| 60% | 2,953 | 1,969 | 0.0000 | yes — 4,203 share u=0.0000 |
| 65% | 3,199 | 1,723 | 0.0000 | yes — 4,203 share u=0.0000 |
| 70% | 3,445 | 1,477 | 0.0000 | yes — 4,203 share u=0.0000 |
| 75% | 3,692 | 1,230 | 0.0000 | yes — 4,203 share u=0.0000 |
| 80% | 3,938 | 984 | 0.0000 | yes — 4,203 share u=0.0000 |
| 85% | 4,184 | 738 | 0.0000 | yes — 4,203 share u=0.0000 |
| 90% | 4,430 | 492 | 0.0000 | yes — 4,203 share u=0.0000 |
| 95% | 4,676 | 246 | 0.0000 | yes — 4,203 share u=0.0000 |

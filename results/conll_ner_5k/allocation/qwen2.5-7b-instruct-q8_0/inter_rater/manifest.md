# conll_ner_5k / inter_rater — rank-based splits (qwen2.5-7b-instruct-q8_0)

4,670 instances ranked by `u_agreement`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **39**

⚠️ **3,546 instances (75.9%) sit at u = 0.** Any cut beyond the 24.1% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 234 | 4,436 | 0.7333 | yes — 22 share u=0.7333 |
| 10% | 467 | 4,203 | 0.6667 | yes — 327 share u=0.6667 |
| 15% | 700 | 3,970 | 0.5714 | yes — 40 share u=0.5714 |
| 20% | 934 | 3,736 | 0.4643 | yes — 3 share u=0.4643 |
| 25% | 1,168 | 3,502 | 0.0000 | yes — 3,546 share u=0.0000 |
| 30% | 1,401 | 3,269 | 0.0000 | yes — 3,546 share u=0.0000 |
| 35% | 1,634 | 3,036 | 0.0000 | yes — 3,546 share u=0.0000 |
| 40% | 1,868 | 2,802 | 0.0000 | yes — 3,546 share u=0.0000 |
| 45% | 2,102 | 2,568 | 0.0000 | yes — 3,546 share u=0.0000 |
| 50% | 2,335 | 2,335 | 0.0000 | yes — 3,546 share u=0.0000 |
| 55% | 2,568 | 2,102 | 0.0000 | yes — 3,546 share u=0.0000 |
| 60% | 2,802 | 1,868 | 0.0000 | yes — 3,546 share u=0.0000 |
| 65% | 3,036 | 1,634 | 0.0000 | yes — 3,546 share u=0.0000 |
| 70% | 3,269 | 1,401 | 0.0000 | yes — 3,546 share u=0.0000 |
| 75% | 3,502 | 1,168 | 0.0000 | yes — 3,546 share u=0.0000 |
| 80% | 3,736 | 934 | 0.0000 | yes — 3,546 share u=0.0000 |
| 85% | 3,970 | 700 | 0.0000 | yes — 3,546 share u=0.0000 |
| 90% | 4,203 | 467 | 0.0000 | yes — 3,546 share u=0.0000 |
| 95% | 4,436 | 234 | 0.0000 | yes — 3,546 share u=0.0000 |

# pico_5k / confidence — rank-based splits (llama3.1-8b-instruct-q8_0)

5,034 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **7** (heavily tied)

⚠️ **320 instances (6.4%) sit at u = 0.** Any cut beyond the 93.6% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 252 | 4,782 | 0.0667 | yes — 166 share u=0.0667 |
| 10% | 503 | 4,531 | 0.0444 | yes — 1,620 share u=0.0444 |
| 15% | 755 | 4,279 | 0.0444 | yes — 1,620 share u=0.0444 |
| 20% | 1,007 | 4,027 | 0.0444 | yes — 1,620 share u=0.0444 |
| 25% | 1,258 | 3,776 | 0.0444 | yes — 1,620 share u=0.0444 |
| 30% | 1,510 | 3,524 | 0.0444 | yes — 1,620 share u=0.0444 |
| 35% | 1,762 | 3,272 | 0.0444 | yes — 1,620 share u=0.0444 |
| 40% | 2,014 | 3,020 | 0.0333 | yes — 1,452 share u=0.0333 |
| 45% | 2,265 | 2,769 | 0.0333 | yes — 1,452 share u=0.0333 |
| 50% | 2,517 | 2,517 | 0.0333 | yes — 1,452 share u=0.0333 |
| 55% | 2,769 | 2,265 | 0.0333 | yes — 1,452 share u=0.0333 |
| 60% | 3,020 | 2,014 | 0.0333 | yes — 1,452 share u=0.0333 |
| 65% | 3,272 | 1,762 | 0.0333 | yes — 1,452 share u=0.0333 |
| 70% | 3,524 | 1,510 | 0.0250 | yes — 184 share u=0.0250 |
| 75% | 3,776 | 1,258 | 0.0222 | yes — 1,182 share u=0.0222 |
| 80% | 4,027 | 1,007 | 0.0222 | yes — 1,182 share u=0.0222 |
| 85% | 4,279 | 755 | 0.0222 | yes — 1,182 share u=0.0222 |
| 90% | 4,531 | 503 | 0.0222 | yes — 1,182 share u=0.0222 |
| 95% | 4,782 | 252 | 0.0000 | yes — 320 share u=0.0000 |

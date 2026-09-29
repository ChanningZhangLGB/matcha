# pico_5k / confidence — rank-based splits (qwen2.5-7b-instruct-q8_0)

5,034 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **6** (heavily tied)

⚠️ **1,981 instances (39.4%) sit at u = 0.** Any cut beyond the 60.6% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 252 | 4,782 | 0.0556 | yes — 304 share u=0.0556 |
| 10% | 503 | 4,531 | 0.0333 | yes — 398 share u=0.0333 |
| 15% | 755 | 4,279 | 0.0222 | yes — 441 share u=0.0222 |
| 20% | 1,007 | 4,027 | 0.0222 | yes — 441 share u=0.0222 |
| 25% | 1,258 | 3,776 | 0.0167 | yes — 1,494 share u=0.0167 |
| 30% | 1,510 | 3,524 | 0.0167 | yes — 1,494 share u=0.0167 |
| 35% | 1,762 | 3,272 | 0.0167 | yes — 1,494 share u=0.0167 |
| 40% | 2,014 | 3,020 | 0.0167 | yes — 1,494 share u=0.0167 |
| 45% | 2,265 | 2,769 | 0.0167 | yes — 1,494 share u=0.0167 |
| 50% | 2,517 | 2,517 | 0.0167 | yes — 1,494 share u=0.0167 |
| 55% | 2,769 | 2,265 | 0.0111 | yes — 416 share u=0.0111 |
| 60% | 3,020 | 2,014 | 0.0111 | yes — 416 share u=0.0111 |
| 65% | 3,272 | 1,762 | 0.0000 | yes — 1,981 share u=0.0000 |
| 70% | 3,524 | 1,510 | 0.0000 | yes — 1,981 share u=0.0000 |
| 75% | 3,776 | 1,258 | 0.0000 | yes — 1,981 share u=0.0000 |
| 80% | 4,027 | 1,007 | 0.0000 | yes — 1,981 share u=0.0000 |
| 85% | 4,279 | 755 | 0.0000 | yes — 1,981 share u=0.0000 |
| 90% | 4,531 | 503 | 0.0000 | yes — 1,981 share u=0.0000 |
| 95% | 4,782 | 252 | 0.0000 | yes — 1,981 share u=0.0000 |

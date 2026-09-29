# pico_5k / entropy — rank-based splits (qwen2.5-7b-instruct-q8_0)

5,034 instances ranked by `u_entropy`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **5** (heavily tied)

⚠️ **4,126 instances (82.0%) sit at u = 0.** Any cut beyond the 18.0% mark divides that block arbitrarily.

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 252 | 4,782 | 0.6365 | yes — 188 share u=0.6365 |
| 10% | 503 | 4,531 | 0.5297 | yes — 208 share u=0.5297 |
| 15% | 755 | 4,279 | 0.3488 | yes — 309 share u=0.3488 |
| 20% | 1,007 | 4,027 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 25% | 1,258 | 3,776 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 30% | 1,510 | 3,524 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 35% | 1,762 | 3,272 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 40% | 2,014 | 3,020 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 45% | 2,265 | 2,769 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 50% | 2,517 | 2,517 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 55% | 2,769 | 2,265 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 60% | 3,020 | 2,014 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 65% | 3,272 | 1,762 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 70% | 3,524 | 1,510 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 75% | 3,776 | 1,258 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 80% | 4,027 | 1,007 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 85% | 4,279 | 755 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 90% | 4,531 | 503 | -0.0000 | yes — 4,126 share u=-0.0000 |
| 95% | 4,782 | 252 | -0.0000 | yes — 4,126 share u=-0.0000 |

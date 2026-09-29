# pico_5k / confidence — rank-based splits (gpt-4o-mini)

5,034 instances ranked by `u_confidence`, most uncertain first.
Cut is positional: the **high** batch is the top X% by count.
Distinct uncertainty values: **11** (heavily tied)

| X | high n | low n | u at cut | cut inside a tie group? |
|--:|--:|--:|--:|---|
| 5% | 252 | 4,782 | 0.1056 | yes — 378 share u=0.1056 |
| 10% | 503 | 4,531 | 0.1000 | yes — 556 share u=0.1000 |
| 15% | 755 | 4,279 | 0.1000 | yes — 556 share u=0.1000 |
| 20% | 1,007 | 4,027 | 0.0944 | yes — 394 share u=0.0944 |
| 25% | 1,258 | 3,776 | 0.0944 | yes — 394 share u=0.0944 |
| 30% | 1,510 | 3,524 | 0.0889 | yes — 891 share u=0.0889 |
| 35% | 1,762 | 3,272 | 0.0889 | yes — 891 share u=0.0889 |
| 40% | 2,014 | 3,020 | 0.0889 | yes — 891 share u=0.0889 |
| 45% | 2,265 | 2,769 | 0.0778 | yes — 402 share u=0.0778 |
| 50% | 2,517 | 2,517 | 0.0778 | yes — 402 share u=0.0778 |
| 55% | 2,769 | 2,265 | 0.0722 | yes — 610 share u=0.0722 |
| 60% | 3,020 | 2,014 | 0.0722 | yes — 610 share u=0.0722 |
| 65% | 3,272 | 1,762 | 0.0667 | yes — 772 share u=0.0667 |
| 70% | 3,524 | 1,510 | 0.0667 | yes — 772 share u=0.0667 |
| 75% | 3,776 | 1,258 | 0.0667 | yes — 772 share u=0.0667 |
| 80% | 4,027 | 1,007 | 0.0611 | yes — 125 share u=0.0611 |
| 85% | 4,279 | 755 | 0.0556 | yes — 276 share u=0.0556 |
| 90% | 4,531 | 503 | 0.0500 | yes — 520 share u=0.0500 |
| 95% | 4,782 | 252 | 0.0500 | yes — 520 share u=0.0500 |

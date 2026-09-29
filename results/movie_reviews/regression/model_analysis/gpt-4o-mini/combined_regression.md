# movie_reviews (regression) - Human + gpt-4o-mini

The LLM joins the 135 human raters as **one additional annotator**, its rating being the mean over 6 continuous conditions (`basic` + `control`).  
Ratings per item rise from 4.96 to 5.96.

| Method | pool | MAE | RMSE | R2 | r |
|---|---|--:|--:|--:|--:|
| Mean | human-only | 0.0607 | 0.0755 | 0.8299 | 0.9283 |
| Mean | human+LLM | **0.0540** | 0.0672 | 0.8650 | 0.9455 |
| EMBias | human-only | 0.0492 | 0.0587 | 0.8969 | 0.9672 |
| EMBias | human+LLM | **0.0476** | 0.0571 | 0.9027 | 0.9697 |

| Method | delta MAE | delta R2 |
|---|--:|--:|
| Mean | -0.0066 | +0.0352 |
| EMBias | -0.0016 | +0.0058 |

Lower MAE is better, higher R2 is better, so a NEGATIVE delta MAE means the LLM helped.
`shipped_DS` is a precomputed artefact and cannot be re-run on a combined pool, so it stays a human-only reference.

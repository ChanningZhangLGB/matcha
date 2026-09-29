# movie_reviews (regression) - Human + LLM

The LLM joins the human raters as **one extra annotator**; the aggregators are re-fitted on the combined pool.  
`shipped_DS` is a precomputed artefact and cannot be re-fitted, so it stays human-only.

| model | metric | Mean | EMBias |
|---|---|--:|--:|
| gpt-4o-mini | MAE | 0.0540 | 0.0476 |
| gpt-4o-mini | RMSE | 0.0672 | 0.0571 |
| gpt-4o-mini | R2 | 0.8650 | 0.9027 |
| gpt-4o-mini | r | 0.9455 | 0.9697 |
| llama3.1-8b-instruct-q8_0 | MAE | 0.0536 | 0.0476 |
| llama3.1-8b-instruct-q8_0 | RMSE | 0.0668 | 0.0571 |
| llama3.1-8b-instruct-q8_0 | R2 | 0.8668 | 0.9025 |
| llama3.1-8b-instruct-q8_0 | r | 0.9458 | 0.9695 |
| qwen2.5-7b-instruct-q8_0 | MAE | 0.0573 | 0.0484 |
| qwen2.5-7b-instruct-q8_0 | RMSE | 0.0712 | 0.0578 |
| qwen2.5-7b-instruct-q8_0 | R2 | 0.8483 | 0.9001 |
| qwen2.5-7b-instruct-q8_0 | r | 0.9404 | 0.9687 |

**Human-only reference**

| | Mean | EMBias |
|---|--:|--:|
| MAE | 0.0607 | 0.0492 |
| RMSE | 0.0755 | 0.0587 |
| R2 | 0.8299 | 0.8969 |
| r | 0.9283 | 0.9672 |

Lower MAE/RMSE is better; higher R2/r is better.

# movie_reviews (regression) - summary

Continuous ratings on [0,1]; **not** comparable to the categorical table.  
**Human-only**: aggregation over the human ratings.  
**LLM-only**: mean over that model's continuous conditions (`basic` + `control`; `customized` is a lettered choice and is excluded).

| | **Mean** | **EMBias** | **shipped_DS** | **gpt-4o-mini** | **llama3.1-8b-instruct-q8_0** | **qwen2.5-7b-instruct-q8_0** |
|---|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  | *LLM-only* |  |  |
| **MAE** | 0.0607 | 0.0492 | 0.0436 | 0.0949 | 0.1071 | 0.1150 |
| **RMSE** | 0.0755 | 0.0587 | 0.0535 | 0.1206 | 0.1347 | 0.1490 |
| **R2** | 0.8299 | 0.8969 | 0.9143 | 0.5653 | 0.4580 | 0.3363 |
| **r** | 0.9283 | 0.9672 | 0.9736 | 0.8788 | 0.8707 | 0.8026 |

Lower MAE/RMSE is better; higher R2/r is better.

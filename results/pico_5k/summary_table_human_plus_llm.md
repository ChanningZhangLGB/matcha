# pico_5k - Human + LLM

The LLM joins the human crowd as **one extra annotator**; all 8 aggregators are then re-fitted on the combined pool.  
One row per model per metric; compare against the Human-only row of `summary_table.md`.

| model | metric | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | Acc | 0.9460 | 0.9583 | 0.9577 | 0.9595 | 0.9601 | 0.9573 | 0.9607 | 0.9541 |
| gpt-4o-mini | macro_f1 | 0.8285 | 0.8248 | 0.8167 | 0.8293 | 0.8301 | 0.8224 | 0.8358 | 0.7930 |
| llama3.1-8b-instruct-q8_0 | Acc | 0.9335 | 0.9446 | 0.9583 | 0.9573 | 0.9587 | 0.9551 | 0.9583 | 0.9557 |
| llama3.1-8b-instruct-q8_0 | macro_f1 | 0.8021 | 0.7878 | 0.8233 | 0.8204 | 0.8255 | 0.8163 | 0.8268 | 0.8021 |
| qwen2.5-7b-instruct-q8_0 | Acc | 0.9249 | 0.9456 | 0.9555 | 0.9589 | 0.9573 | 0.9567 | 0.9597 | 0.9559 |
| qwen2.5-7b-instruct-q8_0 | macro_f1 | 0.7856 | 0.7902 | 0.8115 | 0.8265 | 0.8214 | 0.8207 | 0.8319 | 0.8033 |

**Human-only reference**

| | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Acc | 0.9491 | 0.9607 | 0.9587 | 0.9601 | 0.9201 | 0.9567 | 0.9615 | 0.9575 |
| macro_f1 | 0.8323 | 0.8372 | 0.8265 | 0.8340 | 0.7320 | 0.8228 | 0.8414 | 0.8110 |

# crowdtruth_treat - Human + LLM

The LLM joins the human crowd as **one extra annotator**; all 8 aggregators are then re-fitted on the combined pool.  
One row per model per metric; compare against the Human-only row of `summary_table.md`.

| model | metric | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | Acc | 0.8180 | 0.8052 | 0.8341 | 0.8068 | 0.8148 | 0.8196 | 0.8084 | 0.8132 |
| gpt-4o-mini | macro_f1 | 0.8157 | 0.7998 | 0.8309 | 0.8011 | 0.8088 | 0.8151 | 0.8026 | 0.8083 |
| llama3.1-8b-instruct-q8_0 | Acc | 0.8100 | 0.8068 | 0.8261 | 0.8084 | 0.8100 | 0.8180 | 0.8100 | 0.8148 |
| llama3.1-8b-instruct-q8_0 | macro_f1 | 0.8072 | 0.8011 | 0.8221 | 0.8026 | 0.8035 | 0.8132 | 0.8042 | 0.8097 |
| qwen2.5-7b-instruct-q8_0 | Acc | 0.8261 | 0.8084 | 0.8293 | 0.8100 | 0.8100 | 0.8213 | 0.8116 | 0.8164 |
| qwen2.5-7b-instruct-q8_0 | macro_f1 | 0.8237 | 0.8031 | 0.8259 | 0.8044 | 0.8035 | 0.8167 | 0.8059 | 0.8114 |

**Human-only reference**

| | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Acc | 0.8245 | 0.7907 | 0.8293 | 0.7987 | 0.8132 | 0.8180 | 0.8035 | 0.8213 |
| macro_f1 | 0.8219 | 0.7827 | 0.8256 | 0.7917 | 0.8066 | 0.8132 | 0.7971 | 0.8161 |

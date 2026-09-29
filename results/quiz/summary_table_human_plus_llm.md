# quiz - Human + LLM

The LLM joins the human crowd as **one extra annotator**; all 8 aggregators are then re-fitted on the combined pool.  
One row per model per metric; compare against the Human-only row of `summary_table.md`.

| model | metric | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | Acc | 0.6710 | 0.6323 | 0.7032 | 0.6968 | 0.7419 | 0.7613 | 0.7097 | 0.7484 |
| gpt-4o-mini | macro_f1 | 0.6172 | 0.6111 | 0.7123 | 0.6879 | 0.7753 | 0.7868 | 0.7480 | 0.7776 |
| llama3.1-8b-instruct-q8_0 | Acc | 0.6387 | 0.6129 | 0.6903 | 0.6645 | 0.7097 | 0.7355 | 0.6839 | 0.7097 |
| llama3.1-8b-instruct-q8_0 | macro_f1 | 0.5873 | 0.5946 | 0.7010 | 0.6558 | 0.7226 | 0.7683 | 0.7236 | 0.7414 |
| qwen2.5-7b-instruct-q8_0 | Acc | 0.6387 | 0.6387 | 0.6968 | 0.6903 | 0.7097 | 0.7484 | 0.7097 | 0.7419 |
| qwen2.5-7b-instruct-q8_0 | macro_f1 | 0.5741 | 0.6173 | 0.6872 | 0.6830 | 0.6699 | 0.7776 | 0.7480 | 0.7719 |

**Human-only reference**

| | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Acc | 0.6065 | 0.6065 | 0.6387 | 0.6581 | 0.6323 | 0.7226 | 0.6645 | 0.6968 |
| macro_f1 | 0.5542 | 0.5894 | 0.6382 | 0.6525 | 0.6084 | 0.7547 | 0.7078 | 0.7346 |

# conll_ner_5k - Human + LLM

The LLM joins the human crowd as **one extra annotator**; all 8 aggregators are then re-fitted on the combined pool.  
One row per model per metric; compare against the Human-only row of `summary_table.md`.

| model | metric | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | Acc | 0.9498 | 0.9238 | 0.9316 | 0.9308 | 0.9296 | 0.9282 | 0.9310 | 0.9198 |
| gpt-4o-mini | macro_f1 | 0.7666 | 0.6562 | 0.7001 | 0.7020 | 0.6876 | 0.6825 | 0.6950 | 0.6136 |
| llama3.1-8b-instruct-q8_0 | Acc | 0.9412 | 0.9198 | 0.9276 | 0.9280 | 0.9270 | 0.9256 | 0.9272 | 0.9154 |
| llama3.1-8b-instruct-q8_0 | macro_f1 | 0.7549 | 0.6274 | 0.6878 | 0.6915 | 0.6845 | 0.6719 | 0.6863 | 0.6030 |
| qwen2.5-7b-instruct-q8_0 | Acc | 0.9454 | 0.9178 | 0.9298 | 0.9294 | 0.9274 | 0.9276 | 0.9292 | 0.9148 |
| qwen2.5-7b-instruct-q8_0 | macro_f1 | 0.7602 | 0.6191 | 0.6970 | 0.6978 | 0.6813 | 0.6843 | 0.6959 | 0.5971 |

**Human-only reference**

| | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Acc | 0.9418 | 0.9142 | 0.9240 | 0.9234 | 0.9242 | 0.9234 | 0.9248 | 0.9108 |
| macro_f1 | 0.7529 | 0.6253 | 0.6825 | 0.6818 | 0.6794 | 0.6776 | 0.6844 | 0.5889 |

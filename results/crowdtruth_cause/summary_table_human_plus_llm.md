# crowdtruth_cause - Human + LLM

The LLM joins the human crowd as **one extra annotator**; all 8 aggregators are then re-fitted on the combined pool.  
One row per model per metric; compare against the Human-only row of `summary_table.md`.

| model | metric | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | Acc | 0.7579 | 0.7662 | 0.7682 | 0.7662 | 0.7651 | 0.7662 | 0.7662 | 0.7692 |
| gpt-4o-mini | macro_f1 | 0.5997 | 0.5484 | 0.5524 | 0.5509 | 0.5526 | 0.5533 | 0.5509 | 0.5507 |
| llama3.1-8b-instruct-q8_0 | Acc | 0.7559 | 0.7651 | 0.7682 | 0.7662 | 0.7651 | 0.7672 | 0.7662 | 0.7682 |
| llama3.1-8b-instruct-q8_0 | macro_f1 | 0.6047 | 0.5477 | 0.5524 | 0.5509 | 0.5502 | 0.5517 | 0.5509 | 0.5524 |
| qwen2.5-7b-instruct-q8_0 | Acc | 0.7579 | 0.7662 | 0.7682 | 0.7672 | 0.7651 | 0.7682 | 0.7672 | 0.7692 |
| qwen2.5-7b-instruct-q8_0 | macro_f1 | 0.6112 | 0.5484 | 0.5524 | 0.5517 | 0.5526 | 0.5548 | 0.5517 | 0.5507 |

**Human-only reference**

| | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Acc | 0.7600 | 0.7631 | 0.7672 | 0.7631 | 0.7662 | 0.7692 | 0.7631 | 0.7651 |
| macro_f1 | 0.6065 | 0.5462 | 0.5517 | 0.5462 | 0.5533 | 0.5556 | 0.5462 | 0.5401 |

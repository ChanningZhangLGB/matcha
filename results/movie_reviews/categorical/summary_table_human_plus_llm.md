# movie_reviews - Human + LLM

The LLM joins the human crowd as **one extra annotator**; all 8 aggregators are then re-fitted on the combined pool.  
One row per model per metric; compare against the Human-only row of `summary_table.md`.

| model | metric | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | Acc | 0.8131 | 0.8231 | 0.8138 | 0.8191 | 0.7964 | 0.7870 | 0.8164 | 0.7997 |
| gpt-4o-mini | macro_f1 | 0.7918 | 0.8053 | 0.8008 | 0.8052 | 0.7850 | 0.7796 | 0.8032 | 0.7909 |
| llama3.1-8b-instruct-q8_0 | Acc | 0.8184 | 0.8311 | 0.8204 | 0.8238 | 0.7977 | 0.7870 | 0.8211 | 0.8017 |
| llama3.1-8b-instruct-q8_0 | macro_f1 | 0.7969 | 0.8127 | 0.8072 | 0.8089 | 0.7851 | 0.7804 | 0.8077 | 0.7931 |
| qwen2.5-7b-instruct-q8_0 | Acc | 0.7924 | 0.8097 | 0.8011 | 0.7991 | 0.7891 | 0.7737 | 0.7984 | 0.7864 |
| qwen2.5-7b-instruct-q8_0 | macro_f1 | 0.7748 | 0.7921 | 0.7895 | 0.7856 | 0.7769 | 0.7672 | 0.7862 | 0.7787 |

**Human-only reference**

| | DawidSkene | MajorityVote | GLAD | Wawa | MMSR | MACE | ZeroBasedSkill | OneCoinDawidSkene |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Acc | 0.7824 | 0.7710 | 0.7824 | 0.7864 | 0.7417 | 0.7904 | 0.7924 | 0.7824 |
| macro_f1 | 0.7680 | 0.7598 | 0.7730 | 0.7765 | 0.7331 | 0.7815 | 0.7826 | 0.7762 |

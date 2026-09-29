# movie_reviews - Human + llama3.1-8b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::llama3.1-8b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 135 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| MajorityVote | 0.7598 | **0.8127** | +0.0528 |
| Wawa | 0.7765 | **0.8089** | +0.0324 |
| ZeroBasedSkill | 0.7826 | **0.8077** | +0.0252 |
| GLAD | 0.7730 | **0.8072** | +0.0342 |
| DawidSkene | 0.7680 | **0.7969** | +0.0288 |
| OneCoinDawidSkene | 0.7762 | **0.7931** | +0.0169 |
| MMSR | 0.7331 | **0.7851** | +0.0520 |
| MACE | 0.7815 | **0.7804** | -0.0011 |

# movie_reviews - Human + qwen2.5-7b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5-7b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 135 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| MajorityVote | 0.7598 | **0.7921** | +0.0322 |
| GLAD | 0.7730 | **0.7895** | +0.0165 |
| ZeroBasedSkill | 0.7826 | **0.7862** | +0.0037 |
| Wawa | 0.7765 | **0.7856** | +0.0091 |
| OneCoinDawidSkene | 0.7762 | **0.7787** | +0.0025 |
| MMSR | 0.7331 | **0.7769** | +0.0438 |
| DawidSkene | 0.7680 | **0.7748** | +0.0067 |
| MACE | 0.7815 | **0.7672** | -0.0144 |

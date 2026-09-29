# pico_5k - Human + qwen2.5-7b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5-7b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 50 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| ZeroBasedSkill | 0.8414 | **0.8319** | -0.0095 |
| Wawa | 0.8340 | **0.8265** | -0.0075 |
| MMSR | 0.7320 | **0.8214** | +0.0895 |
| MACE | 0.8228 | **0.8207** | -0.0020 |
| GLAD | 0.8265 | **0.8115** | -0.0150 |
| OneCoinDawidSkene | 0.8110 | **0.8033** | -0.0077 |
| MajorityVote | 0.8372 | **0.7902** | -0.0470 |
| DawidSkene | 0.8323 | **0.7856** | -0.0467 |

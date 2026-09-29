# pico_5k - Human + llama3.1-8b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::llama3.1-8b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 50 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| ZeroBasedSkill | 0.8414 | **0.8268** | -0.0146 |
| MMSR | 0.7320 | **0.8255** | +0.0935 |
| GLAD | 0.8265 | **0.8233** | -0.0032 |
| Wawa | 0.8340 | **0.8204** | -0.0136 |
| MACE | 0.8228 | **0.8163** | -0.0065 |
| DawidSkene | 0.8323 | **0.8021** | -0.0302 |
| OneCoinDawidSkene | 0.8110 | **0.8021** | -0.0089 |
| MajorityVote | 0.8372 | **0.7878** | -0.0494 |

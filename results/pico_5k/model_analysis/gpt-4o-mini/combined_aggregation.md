# pico_5k - Human + gpt-4o-mini aggregation

The LLM is appended as **one additional annotator** (LLM::gpt-4o-mini) whose label is its majority vote over the 9 prompt conditions, joining 50 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| ZeroBasedSkill | 0.8414 | **0.8358** | -0.0056 |
| MMSR | 0.7320 | **0.8301** | +0.0981 |
| Wawa | 0.8340 | **0.8293** | -0.0047 |
| DawidSkene | 0.8323 | **0.8285** | -0.0038 |
| MajorityVote | 0.8372 | **0.8248** | -0.0124 |
| MACE | 0.8228 | **0.8224** | -0.0003 |
| GLAD | 0.8265 | **0.8167** | -0.0098 |
| OneCoinDawidSkene | 0.8110 | **0.7930** | -0.0179 |

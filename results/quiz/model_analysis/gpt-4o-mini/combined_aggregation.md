# quiz - Human + gpt-4o-mini aggregation

The LLM is appended as **one additional annotator** (LLM::gpt-4o-mini) whose label is its majority vote over the 9 prompt conditions, joining 360 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| MACE | 0.7547 | **0.7868** | +0.0322 |
| OneCoinDawidSkene | 0.7346 | **0.7776** | +0.0430 |
| MMSR | 0.6084 | **0.7753** | +0.1669 |
| ZeroBasedSkill | 0.7078 | **0.7480** | +0.0402 |
| GLAD | 0.6382 | **0.7123** | +0.0741 |
| Wawa | 0.6525 | **0.6879** | +0.0354 |
| DawidSkene | 0.5542 | **0.6172** | +0.0630 |
| MajorityVote | 0.5894 | **0.6111** | +0.0217 |

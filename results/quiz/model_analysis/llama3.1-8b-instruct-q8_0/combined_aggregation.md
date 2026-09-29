# quiz - Human + llama3.1-8b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::llama3.1-8b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 360 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| MACE | 0.7547 | **0.7683** | +0.0137 |
| OneCoinDawidSkene | 0.7346 | **0.7414** | +0.0068 |
| ZeroBasedSkill | 0.7078 | **0.7236** | +0.0158 |
| MMSR | 0.6084 | **0.7226** | +0.1142 |
| GLAD | 0.6382 | **0.7010** | +0.0628 |
| Wawa | 0.6525 | **0.6558** | +0.0034 |
| MajorityVote | 0.5894 | **0.5946** | +0.0052 |
| DawidSkene | 0.5542 | **0.5873** | +0.0331 |

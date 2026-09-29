# quiz - Human + qwen2.5-7b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5-7b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 360 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| MACE | 0.7547 | **0.7776** | +0.0230 |
| OneCoinDawidSkene | 0.7346 | **0.7719** | +0.0374 |
| ZeroBasedSkill | 0.7078 | **0.7480** | +0.0402 |
| GLAD | 0.6382 | **0.6872** | +0.0489 |
| Wawa | 0.6525 | **0.6830** | +0.0305 |
| MMSR | 0.6084 | **0.6699** | +0.0615 |
| MajorityVote | 0.5894 | **0.6173** | +0.0279 |
| DawidSkene | 0.5542 | **0.5741** | +0.0199 |

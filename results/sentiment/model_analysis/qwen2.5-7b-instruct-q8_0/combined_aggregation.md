# sentiment - Human + qwen2.5-7b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5-7b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 203 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| MACE | 0.9148 | **0.9252** | +0.0104 |
| OneCoinDawidSkene | 0.9166 | **0.9246** | +0.0080 |
| DawidSkene | 0.9152 | **0.9232** | +0.0080 |
| GLAD | 0.9166 | **0.9228** | +0.0062 |
| MMSR | 0.9008 | **0.9188** | +0.0180 |
| ZeroBasedSkill | 0.8945 | **0.9164** | +0.0219 |
| Wawa | 0.8947 | **0.9162** | +0.0215 |
| MajorityVote | 0.8820 | **0.9023** | +0.0203 |

# crowdtruth_treat - Human + qwen2.5-7b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5-7b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 286 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| GLAD | 0.8256 | **0.8259** | +0.0003 |
| DawidSkene | 0.8219 | **0.8237** | +0.0017 |
| MACE | 0.8132 | **0.8167** | +0.0035 |
| OneCoinDawidSkene | 0.8161 | **0.8114** | -0.0047 |
| ZeroBasedSkill | 0.7971 | **0.8059** | +0.0089 |
| Wawa | 0.7917 | **0.8044** | +0.0127 |
| MMSR | 0.8066 | **0.8035** | -0.0031 |
| MajorityVote | 0.7827 | **0.8031** | +0.0204 |

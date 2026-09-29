# crowdtruth_pooled - Human + llama3.1-8b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::llama3.1-8b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 304 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.7495 | **0.7513** | +0.0019 |
| MACE | 0.7259 | **0.7247** | -0.0012 |
| GLAD | 0.7192 | **0.7195** | +0.0003 |
| OneCoinDawidSkene | 0.7100 | **0.7149** | +0.0048 |
| ZeroBasedSkill | 0.6997 | **0.7146** | +0.0149 |
| MMSR | 0.7164 | **0.7129** | -0.0034 |
| Wawa | 0.6997 | **0.7104** | +0.0107 |
| MajorityVote | 0.6997 | **0.6900** | -0.0097 |

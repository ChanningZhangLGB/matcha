# crowdtruth_pooled - Human + qwen2.5-7b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5-7b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 304 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.7495 | **0.7501** | +0.0006 |
| MACE | 0.7259 | **0.7258** | -0.0002 |
| GLAD | 0.7192 | **0.7219** | +0.0027 |
| OneCoinDawidSkene | 0.7100 | **0.7149** | +0.0048 |
| ZeroBasedSkill | 0.6997 | **0.7146** | +0.0149 |
| MMSR | 0.7164 | **0.7134** | -0.0030 |
| Wawa | 0.6997 | **0.7120** | +0.0123 |
| MajorityVote | 0.6997 | **0.6939** | -0.0058 |

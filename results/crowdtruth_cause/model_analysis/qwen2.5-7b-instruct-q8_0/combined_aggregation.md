# crowdtruth_cause - Human + qwen2.5-7b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5-7b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 304 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.6065 | **0.6112** | +0.0047 |
| MACE | 0.5556 | **0.5548** | -0.0008 |
| MMSR | 0.5533 | **0.5526** | -0.0007 |
| GLAD | 0.5517 | **0.5524** | +0.0007 |
| Wawa | 0.5462 | **0.5517** | +0.0054 |
| ZeroBasedSkill | 0.5462 | **0.5517** | +0.0054 |
| OneCoinDawidSkene | 0.5401 | **0.5507** | +0.0106 |
| MajorityVote | 0.5462 | **0.5484** | +0.0022 |

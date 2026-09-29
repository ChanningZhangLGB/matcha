# crowdtruth_cause - Human + llama3.1-8b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::llama3.1-8b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 304 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.6065 | **0.6047** | -0.0018 |
| OneCoinDawidSkene | 0.5401 | **0.5524** | +0.0123 |
| GLAD | 0.5517 | **0.5524** | +0.0007 |
| MACE | 0.5556 | **0.5517** | -0.0040 |
| Wawa | 0.5462 | **0.5509** | +0.0047 |
| ZeroBasedSkill | 0.5462 | **0.5509** | +0.0047 |
| MMSR | 0.5533 | **0.5502** | -0.0032 |
| MajorityVote | 0.5462 | **0.5477** | +0.0015 |

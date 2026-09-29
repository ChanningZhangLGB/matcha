# imagenet16h - Human + qwen2.5vl-7b-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5vl-7b-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 145 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| GLAD | 0.8758 | **0.8763** | +0.0005 |
| ZeroBasedSkill | 0.8755 | **0.8760** | +0.0005 |
| Wawa | 0.8760 | **0.8758** | -0.0002 |
| MMSR | 0.8739 | **0.8757** | +0.0018 |
| OneCoinDawidSkene | 0.8753 | **0.8750** | -0.0003 |
| MACE | 0.8758 | **0.8740** | -0.0017 |
| MajorityVote | 0.8706 | **0.8704** | -0.0002 |
| DawidSkene | 0.8758 | **0.8243** | -0.0515 |

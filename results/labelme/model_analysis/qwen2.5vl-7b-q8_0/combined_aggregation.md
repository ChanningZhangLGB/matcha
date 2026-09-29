# labelme - Human + qwen2.5vl-7b-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5vl-7b-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 59 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.7861 | **0.7969** | +0.0108 |
| ZeroBasedSkill | 0.7739 | **0.7856** | +0.0117 |
| GLAD | 0.7701 | **0.7827** | +0.0125 |
| MMSR | 0.7617 | **0.7817** | +0.0200 |
| MACE | 0.7682 | **0.7814** | +0.0132 |
| OneCoinDawidSkene | 0.7613 | **0.7784** | +0.0171 |
| Wawa | 0.7583 | **0.7778** | +0.0195 |
| MajorityVote | 0.7556 | **0.7729** | +0.0172 |

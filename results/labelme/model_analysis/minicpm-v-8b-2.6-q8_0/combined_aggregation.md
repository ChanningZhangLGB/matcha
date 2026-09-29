# labelme - Human + minicpm-v-8b-2.6-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::minicpm-v-8b-2.6-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 59 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.7861 | **0.7926** | +0.0065 |
| GLAD | 0.7701 | **0.7783** | +0.0082 |
| MMSR | 0.7617 | **0.7765** | +0.0148 |
| MACE | 0.7682 | **0.7761** | +0.0079 |
| OneCoinDawidSkene | 0.7613 | **0.7753** | +0.0140 |
| Wawa | 0.7583 | **0.7739** | +0.0156 |
| ZeroBasedSkill | 0.7739 | **0.7733** | -0.0006 |
| MajorityVote | 0.7556 | **0.7648** | +0.0092 |

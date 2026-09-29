# labelme - Human + gpt-4o-mini aggregation

The LLM is appended as **one additional annotator** (LLM::gpt-4o-mini) whose label is its majority vote over the 9 prompt conditions, joining 59 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.7861 | **0.8209** | +0.0348 |
| MACE | 0.7682 | **0.8142** | +0.0460 |
| ZeroBasedSkill | 0.7739 | **0.8135** | +0.0396 |
| GLAD | 0.7701 | **0.8123** | +0.0422 |
| OneCoinDawidSkene | 0.7613 | **0.8114** | +0.0501 |
| Wawa | 0.7583 | **0.8103** | +0.0520 |
| MMSR | 0.7617 | **0.8041** | +0.0424 |
| MajorityVote | 0.7556 | **0.7944** | +0.0388 |

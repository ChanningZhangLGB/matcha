# sentiment - Human + gpt-4o-mini aggregation

The LLM is appended as **one additional annotator** (LLM::gpt-4o-mini) whose label is its majority vote over the 9 prompt conditions, joining 203 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.9152 | **0.9240** | +0.0088 |
| MACE | 0.9148 | **0.9226** | +0.0078 |
| OneCoinDawidSkene | 0.9166 | **0.9220** | +0.0054 |
| GLAD | 0.9166 | **0.9220** | +0.0054 |
| MMSR | 0.9008 | **0.9186** | +0.0178 |
| Wawa | 0.8947 | **0.9150** | +0.0203 |
| ZeroBasedSkill | 0.8945 | **0.9146** | +0.0201 |
| MajorityVote | 0.8820 | **0.9025** | +0.0206 |

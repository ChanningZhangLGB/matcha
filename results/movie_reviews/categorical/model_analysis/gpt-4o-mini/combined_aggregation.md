# movie_reviews - Human + gpt-4o-mini aggregation

The LLM is appended as **one additional annotator** (LLM::gpt-4o-mini) whose label is its majority vote over the 9 prompt conditions, joining 135 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| MajorityVote | 0.7598 | **0.8053** | +0.0454 |
| Wawa | 0.7765 | **0.8052** | +0.0287 |
| ZeroBasedSkill | 0.7826 | **0.8032** | +0.0206 |
| GLAD | 0.7730 | **0.8008** | +0.0278 |
| DawidSkene | 0.7680 | **0.7918** | +0.0238 |
| OneCoinDawidSkene | 0.7762 | **0.7909** | +0.0147 |
| MMSR | 0.7331 | **0.7850** | +0.0519 |
| MACE | 0.7815 | **0.7796** | -0.0020 |

# imagenet16h - Human + gpt-4o-mini aggregation

The LLM is appended as **one additional annotator** (LLM::gpt-4o-mini) whose label is its majority vote over the 9 prompt conditions, joining 145 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| ZeroBasedSkill | 0.8755 | **0.8812** | +0.0057 |
| Wawa | 0.8760 | **0.8809** | +0.0050 |
| OneCoinDawidSkene | 0.8753 | **0.8805** | +0.0052 |
| MMSR | 0.8739 | **0.8797** | +0.0058 |
| MajorityVote | 0.8706 | **0.8763** | +0.0056 |
| DawidSkene | 0.8758 | **0.8307** | -0.0451 |
| GLAD | 0.8758 | **0.8296** | -0.0461 |
| MACE | 0.8758 | **0.8282** | -0.0475 |

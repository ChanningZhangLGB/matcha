# imagenet16h - Human + minicpm-v-8b-2.6-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::minicpm-v-8b-2.6-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 145 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| GLAD | 0.8758 | **0.8775** | +0.0017 |
| Wawa | 0.8760 | **0.8772** | +0.0013 |
| MMSR | 0.8739 | **0.8768** | +0.0029 |
| ZeroBasedSkill | 0.8755 | **0.8766** | +0.0011 |
| OneCoinDawidSkene | 0.8753 | **0.8764** | +0.0011 |
| MajorityVote | 0.8706 | **0.8731** | +0.0025 |
| DawidSkene | 0.8758 | **0.8326** | -0.0432 |
| MACE | 0.8758 | **0.8275** | -0.0483 |

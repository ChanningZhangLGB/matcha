# sentiment - Human + llama3.1-8b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::llama3.1-8b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 203 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| MACE | 0.9148 | **0.9264** | +0.0116 |
| DawidSkene | 0.9152 | **0.9254** | +0.0102 |
| OneCoinDawidSkene | 0.9166 | **0.9254** | +0.0088 |
| GLAD | 0.9166 | **0.9252** | +0.0086 |
| MMSR | 0.9008 | **0.9202** | +0.0194 |
| ZeroBasedSkill | 0.8945 | **0.9174** | +0.0229 |
| Wawa | 0.8947 | **0.9164** | +0.0217 |
| MajorityVote | 0.8820 | **0.9027** | +0.0207 |

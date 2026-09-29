# crowdtruth_pooled - Human + gpt-4o-mini aggregation

The LLM is appended as **one additional annotator** (LLM::gpt-4o-mini) whose label is its majority vote over the 9 prompt conditions, joining 304 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.7495 | **0.7479** | -0.0015 |
| MACE | 0.7259 | **0.7241** | -0.0018 |
| GLAD | 0.7192 | **0.7200** | +0.0007 |
| ZeroBasedSkill | 0.6997 | **0.7140** | +0.0143 |
| OneCoinDawidSkene | 0.7100 | **0.7137** | +0.0037 |
| MMSR | 0.7164 | **0.7127** | -0.0037 |
| Wawa | 0.6997 | **0.7108** | +0.0112 |
| MajorityVote | 0.6997 | **0.6971** | -0.0025 |

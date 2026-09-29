# crowdtruth_treat - Human + gpt-4o-mini aggregation

The LLM is appended as **one additional annotator** (LLM::gpt-4o-mini) whose label is its majority vote over the 9 prompt conditions, joining 286 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| GLAD | 0.8256 | **0.8309** | +0.0053 |
| DawidSkene | 0.8219 | **0.8157** | -0.0063 |
| MACE | 0.8132 | **0.8151** | +0.0019 |
| MMSR | 0.8066 | **0.8088** | +0.0022 |
| OneCoinDawidSkene | 0.8161 | **0.8083** | -0.0078 |
| ZeroBasedSkill | 0.7971 | **0.8026** | +0.0056 |
| Wawa | 0.7917 | **0.8011** | +0.0094 |
| MajorityVote | 0.7827 | **0.7998** | +0.0171 |

# crowdtruth_treat - Human + llama3.1-8b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::llama3.1-8b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 286 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| GLAD | 0.8256 | **0.8221** | -0.0035 |
| MACE | 0.8132 | **0.8132** | +0.0000 |
| OneCoinDawidSkene | 0.8161 | **0.8097** | -0.0064 |
| DawidSkene | 0.8219 | **0.8072** | -0.0148 |
| ZeroBasedSkill | 0.7971 | **0.8042** | +0.0071 |
| MMSR | 0.8066 | **0.8035** | -0.0031 |
| Wawa | 0.7917 | **0.8026** | +0.0109 |
| MajorityVote | 0.7827 | **0.8011** | +0.0184 |

# conll_ner_5k - Human + qwen2.5-7b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::qwen2.5-7b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 47 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.7529 | **0.7602** | +0.0073 |
| Wawa | 0.6818 | **0.6978** | +0.0160 |
| GLAD | 0.6825 | **0.6970** | +0.0144 |
| ZeroBasedSkill | 0.6844 | **0.6959** | +0.0115 |
| MACE | 0.6776 | **0.6843** | +0.0068 |
| MMSR | 0.6794 | **0.6813** | +0.0019 |
| MajorityVote | 0.6253 | **0.6191** | -0.0062 |
| OneCoinDawidSkene | 0.5889 | **0.5971** | +0.0082 |

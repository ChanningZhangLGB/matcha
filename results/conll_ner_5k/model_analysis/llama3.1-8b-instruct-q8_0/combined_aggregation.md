# conll_ner_5k - Human + llama3.1-8b-instruct-q8_0 aggregation

The LLM is appended as **one additional annotator** (LLM::llama3.1-8b-instruct-q8_0) whose label is its majority vote over the 9 prompt conditions, joining 47 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.7529 | **0.7549** | +0.0019 |
| Wawa | 0.6818 | **0.6915** | +0.0097 |
| GLAD | 0.6825 | **0.6878** | +0.0053 |
| ZeroBasedSkill | 0.6844 | **0.6863** | +0.0018 |
| MMSR | 0.6794 | **0.6845** | +0.0051 |
| MACE | 0.6776 | **0.6719** | -0.0056 |
| MajorityVote | 0.6253 | **0.6274** | +0.0022 |
| OneCoinDawidSkene | 0.5889 | **0.6030** | +0.0141 |

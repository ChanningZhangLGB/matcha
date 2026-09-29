# conll_ner_5k - Human + gpt-4o-mini aggregation

The LLM is appended as **one additional annotator** (LLM::gpt-4o-mini) whose label is its majority vote over the 9 prompt conditions, joining 47 human workers. All 8 aggregators then re-run on the combined pool.

| Method | macro-F1 human-only | macro-F1 human+LLM | delta |
|---|--:|--:|--:|
| DawidSkene | 0.7529 | **0.7666** | +0.0137 |
| Wawa | 0.6818 | **0.7020** | +0.0202 |
| GLAD | 0.6825 | **0.7001** | +0.0175 |
| ZeroBasedSkill | 0.6844 | **0.6950** | +0.0106 |
| MMSR | 0.6794 | **0.6876** | +0.0081 |
| MACE | 0.6776 | **0.6825** | +0.0049 |
| MajorityVote | 0.6253 | **0.6562** | +0.0310 |
| OneCoinDawidSkene | 0.5889 | **0.6136** | +0.0246 |

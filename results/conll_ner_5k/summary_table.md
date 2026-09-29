# conll_ner_5k - summary

**Human-only**: the 8 unsupervised crowd-kit aggregators over the human annotations.  
**LLM-only**: majority vote over that model's protocol x prompt-strategy conditions.

| | **DawidSkene** | **MajorityVote** | **GLAD** | **Wawa** | **MMSR** | **MACE** | **ZeroBasedSkill** | **OneCoinDawidSkene** | **gpt-4o-mini** | **llama3.1-8b-instruct-q8_0** | **qwen2.5-7b-instruct-q8_0** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  |  |  |  |  |  | *LLM-only* |  |  |
| **Acc** | 0.9418 | 0.9142 | 0.9240 | 0.9234 | 0.9242 | 0.9234 | 0.9248 | 0.9108 | 0.9069 | 0.7096 | 0.8377 |
| **macro_f1** | 0.7529 | 0.6253 | 0.6825 | 0.6818 | 0.6794 | 0.6776 | 0.6844 | 0.5889 | 0.5418 | 0.2386 | 0.3785 |

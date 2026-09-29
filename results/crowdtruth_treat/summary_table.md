# crowdtruth_treat - summary

**Human-only**: the 8 unsupervised crowd-kit aggregators over the human annotations.  
**LLM-only**: majority vote over that model's protocol x prompt-strategy conditions.

| | **DawidSkene** | **MajorityVote** | **GLAD** | **Wawa** | **MMSR** | **MACE** | **ZeroBasedSkill** | **OneCoinDawidSkene** | **gpt-4o-mini** | **llama3.1-8b-instruct-q8_0** | **qwen2.5-7b-instruct-q8_0** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  |  |  |  |  |  | *LLM-only* |  |  |
| **Acc** | 0.8245 | 0.7907 | 0.8293 | 0.7987 | 0.8132 | 0.8180 | 0.8035 | 0.8213 | 0.8052 | 0.7810 | 0.8003 |
| **macro_f1** | 0.8219 | 0.7827 | 0.8256 | 0.7917 | 0.8066 | 0.8132 | 0.7971 | 0.8161 | 0.8012 | 0.7726 | 0.7955 |

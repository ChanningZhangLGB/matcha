# sentiment - summary

**Human-only**: the 8 unsupervised crowd-kit aggregators over the human annotations.  
**LLM-only**: majority vote over that model's protocol x prompt-strategy conditions.

| | **DawidSkene** | **MajorityVote** | **GLAD** | **Wawa** | **MMSR** | **MACE** | **ZeroBasedSkill** | **OneCoinDawidSkene** | **gpt-4o-mini** | **llama3.1-8b-instruct-q8_0** | **qwen2.5-7b-instruct-q8_0** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  |  |  |  |  |  | *LLM-only* |  |  |
| **Acc** | 0.9152 | 0.8822 | 0.9166 | 0.8948 | 0.9008 | 0.9148 | 0.8946 | 0.9166 | 0.9012 | 0.9068 | 0.9060 |
| **macro_f1** | 0.9152 | 0.8820 | 0.9166 | 0.8947 | 0.9008 | 0.9148 | 0.8945 | 0.9166 | 0.9007 | 0.9067 | 0.9059 |

# quiz - summary

**Human-only**: the 8 unsupervised crowd-kit aggregators over the human annotations.  
**LLM-only**: majority vote over that model's protocol x prompt-strategy conditions.

| | **DawidSkene** | **MajorityVote** | **GLAD** | **Wawa** | **MMSR** | **MACE** | **ZeroBasedSkill** | **OneCoinDawidSkene** | **gpt-4o-mini** | **llama3.1-8b-instruct-q8_0** | **qwen2.5-7b-instruct-q8_0** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  |  |  |  |  |  | *LLM-only* |  |  |
| **Acc** | 0.6065 | 0.6065 | 0.6387 | 0.6581 | 0.6323 | 0.7226 | 0.6645 | 0.6968 | 0.8387 | 0.6387 | 0.7355 |
| **macro_f1** | 0.5542 | 0.5894 | 0.6382 | 0.6525 | 0.6084 | 0.7547 | 0.7078 | 0.7346 | 0.8651 | 0.5323 | 0.6836 |

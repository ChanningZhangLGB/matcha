# crowdtruth_pooled - summary

**Human-only**: the 8 unsupervised crowd-kit aggregators over the human annotations.  
**LLM-only**: majority vote over that model's protocol x prompt-strategy conditions.

| | **DawidSkene** | **MajorityVote** | **GLAD** | **Wawa** | **MMSR** | **MACE** | **ZeroBasedSkill** | **OneCoinDawidSkene** | **gpt-4o-mini** | **llama3.1-8b-instruct-q8_0** | **qwen2.5-7b-instruct-q8_0** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  |  |  |  |  |  | *LLM-only* |  |  |
| **Acc** | 0.7957 | 0.7738 | 0.7851 | 0.7738 | 0.7845 | 0.7876 | 0.7738 | 0.7807 | 0.7845 | 0.7669 | 0.7813 |
| **macro_f1** | 0.7495 | 0.6997 | 0.7192 | 0.6997 | 0.7164 | 0.7259 | 0.6997 | 0.7100 | 0.7349 | 0.7130 | 0.7309 |

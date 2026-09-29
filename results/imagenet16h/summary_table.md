# imagenet16h - summary

**Human-only**: the 8 unsupervised crowd-kit aggregators over the human annotations.  
**LLM-only**: majority vote over that model's protocol x prompt-strategy conditions.

| | **DawidSkene** | **MajorityVote** | **GLAD** | **Wawa** | **MMSR** | **MACE** | **ZeroBasedSkill** | **OneCoinDawidSkene** | **gpt-4o-mini** | **minicpm-v-8b-2.6-q8_0** | **qwen2.5vl-7b-q8_0** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  |  |  |  |  |  | *LLM-only* |  |  |
| **Acc** | 0.8760 | 0.8715 | 0.8765 | 0.8767 | 0.8746 | 0.8765 | 0.8762 | 0.8760 | 0.7973 | 0.6229 | 0.6523 |
| **macro_f1** | 0.8758 | 0.8706 | 0.8758 | 0.8760 | 0.8739 | 0.8758 | 0.8755 | 0.8753 | 0.7600 | 0.6733 | 0.6247 |

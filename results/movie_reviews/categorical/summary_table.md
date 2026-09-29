# movie_reviews - summary

**Human-only**: the 8 unsupervised crowd-kit aggregators over the human annotations.  
**LLM-only**: majority vote over that model's protocol x prompt-strategy conditions.

| | **DawidSkene** | **MajorityVote** | **GLAD** | **Wawa** | **MMSR** | **MACE** | **ZeroBasedSkill** | **OneCoinDawidSkene** | **gpt-4o-mini** | **llama3.1-8b-instruct-q8_0** | **qwen2.5-7b-instruct-q8_0** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  |  |  |  |  |  | *LLM-only* |  |  |
| **Acc** | 0.7824 | 0.7710 | 0.7824 | 0.7864 | 0.7417 | 0.7904 | 0.7924 | 0.7824 | 0.7483 | 0.7437 | 0.6816 |
| **macro_f1** | 0.7680 | 0.7598 | 0.7730 | 0.7765 | 0.7331 | 0.7815 | 0.7826 | 0.7762 | 0.7242 | 0.7172 | 0.6589 |

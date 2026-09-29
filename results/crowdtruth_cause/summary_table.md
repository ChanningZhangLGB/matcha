# crowdtruth_cause - summary

**Human-only**: the 8 unsupervised crowd-kit aggregators over the human annotations.  
**LLM-only**: majority vote over that model's protocol x prompt-strategy conditions.

| | **DawidSkene** | **MajorityVote** | **GLAD** | **Wawa** | **MMSR** | **MACE** | **ZeroBasedSkill** | **OneCoinDawidSkene** | **gpt-4o-mini** | **llama3.1-8b-instruct-q8_0** | **qwen2.5-7b-instruct-q8_0** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  |  |  |  |  |  | *LLM-only* |  |  |
| **Acc** | 0.7600 | 0.7631 | 0.7672 | 0.7631 | 0.7662 | 0.7692 | 0.7631 | 0.7651 | 0.7713 | 0.7579 | 0.7692 |
| **macro_f1** | 0.6065 | 0.5462 | 0.5517 | 0.5462 | 0.5533 | 0.5556 | 0.5462 | 0.5401 | 0.6304 | 0.6302 | 0.6316 |

# pico_5k - summary

**Human-only**: the 8 unsupervised crowd-kit aggregators over the human annotations.  
**LLM-only**: majority vote over that model's protocol x prompt-strategy conditions.

| | **DawidSkene** | **MajorityVote** | **GLAD** | **Wawa** | **MMSR** | **MACE** | **ZeroBasedSkill** | **OneCoinDawidSkene** | **gpt-4o-mini** | **llama3.1-8b-instruct-q8_0** | **qwen2.5-7b-instruct-q8_0** |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| | *Human-only* |  |  |  |  |  |  |  | *LLM-only* |  |  |
| **Acc** | 0.9491 | 0.9607 | 0.9587 | 0.9601 | 0.9201 | 0.9567 | 0.9615 | 0.9575 | 0.9406 | 0.9118 | 0.8955 |
| **macro_f1** | 0.8323 | 0.8372 | 0.8265 | 0.8340 | 0.7320 | 0.8228 | 0.8414 | 0.8110 | 0.7579 | 0.6992 | 0.6437 |

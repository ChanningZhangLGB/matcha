# MATCHA - best allocation per dataset and model

`best` is a maximum over 2 routes x 3 uncertainty bases x 8 aggregators x 19 budgets = **912 cells** per row. `random` is the control and is excluded from the search.

`gain_vs_random` compares the peak against the random control at the SAME route, aggregator and budget. With 912 cells searched, this column -- not the accuracy -- is what says whether uncertainty ranking did any work.

| Modality | Dataset | model | best | route | uncertainty | method | X | gain vs random |
|---|---|---|--:|---|---|---|--:|--:|
| Text | conll_ner_5k | gpt-4o-mini | **0.9503** | h-human_llm | confidence | DawidSkene | 80 | +0.0131 |
| Text | conll_ner_5k | llama3.1-8b | **0.9393** | h-human | confidence | DawidSkene | 95 | +0.0093 |
| Text | conll_ner_5k | qwen2.5-7b | **0.9425** | h-human_llm | entropy | DawidSkene | 95 | +0.0013 |
| Text | crowdtruth | gpt-4o-mini | **0.7957** | h-human | confidence | DawidSkene | 90 | +0.0025 |
| Text | crowdtruth | llama3.1-8b | **0.8001** | h-human | entropy | MACE | 30 | +0.0269 |
| Text | crowdtruth | qwen2.5-7b | **0.8020** | h-human_llm | confidence | DawidSkene | 70 | +0.0081 |
| Text | movie_reviews | gpt-4o-mini | **0.8304** | h-human_llm | entropy | MajorityVote | 85 | +0.0227 |
| Text | movie_reviews | llama3.1-8b | **0.8304** | h-human_llm | entropy | MajorityVote | 95 | +0.0053 |
| Text | movie_reviews | qwen2.5-7b | **0.8131** | h-human | entropy | MACE | 75 | +0.0621 |
| Text | pico_5k | gpt-4o-mini | **0.9615** | h-human | entropy | ZeroBasedSkill | 95 | +0.0008 |
| Text | pico_5k | llama3.1-8b | **0.9615** | h-human | entropy | ZeroBasedSkill | 95 | +0.0036 |
| Text | pico_5k | qwen2.5-7b | **0.9615** | h-human | entropy | ZeroBasedSkill | 95 | +0.0036 |
| Text | quiz | gpt-4o-mini | **0.8774** | h-human_llm | entropy | OneCoinDawidSkene | 10 | +0.0516 |
| Text | quiz | llama3.1-8b | **0.8000** | h-human | entropy | MACE | 55 | +0.1097 |
| Text | quiz | qwen2.5-7b | **0.8129** | h-human_llm | entropy | MMSR | 45 | +0.0581 |
| Text | sentiment | gpt-4o-mini | **0.9370** | h-human_llm | entropy | OneCoinDawidSkene | 55 | +0.0252 |
| Text | sentiment | llama3.1-8b | **0.9302** | h-human_llm | entropy | OneCoinDawidSkene | 65 | +0.0108 |
| Text | sentiment | qwen2.5-7b | **0.9296** | h-human_llm | entropy | MACE | 20 | +0.0182 |
| Image | imagenet16h | gpt-4o-mini | **0.8840** | h-human_llm | entropy | GLAD | 95 | +0.0075 |
| Image | imagenet16h | minicpm-v-8b | **0.8792** | h-human_llm | entropy | GLAD | 95 | +0.0130 |
| Image | imagenet16h | qwen2.5vl-7b | **0.8771** | h-human_llm | confidence | ZeroBasedSkill | 85 | +0.0329 |
| Image | labelme | gpt-4o-mini | **0.8320** | h-human | entropy | MMSR | 35 |  |
| Image | labelme | minicpm-v-8b | **0.8200** | h-human | confidence | DawidSkene | 70 | +0.0450 |
| Image | labelme | qwen2.5vl-7b | **0.8280** | h-human | entropy | DawidSkene | 70 | +0.0460 |

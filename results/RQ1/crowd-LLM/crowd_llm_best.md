# RQ1 - Crowd-LLM: best per dataset and model

8 crowd-kit aggregators refit on the crowd PLUS the LLM's 9-condition majority-vote label as one additional annotator.

`best` is a max over the 8 methods selected on the scoring gold, so it is an upper bound; `range` is max - min across the 8.

## accuracy

| Modality | Dataset | n | model | best | best method | range across 8 |
|---|---|--:|---|--:|---|--:|
| Text | sentiment | 4,999 | gpt-4o-mini | **0.9240** | DawidSkene | 0.0214 |
| Text | sentiment | 4,999 | llama3.1-8b | **0.9264** | MACE | 0.0236 |
| Text | sentiment | 4,999 | qwen2.5-7b | **0.9252** | MACE | 0.0228 |
| Text | movie_reviews | 1,498 | gpt-4o-mini | **0.8231** | MajorityVote | 0.0361 |
| Text | movie_reviews | 1,498 | llama3.1-8b | **0.8311** | MajorityVote | 0.0441 |
| Text | movie_reviews | 1,498 | qwen2.5-7b | **0.8097** | MajorityVote | 0.0360 |
| Text | crowdtruth | 1,596 | gpt-4o-mini | **0.7945** | DawidSkene | 0.0207 |
| Text | crowdtruth | 1,596 | llama3.1-8b | **0.7970** | DawidSkene | 0.0276 |
| Text | crowdtruth | 1,596 | qwen2.5-7b | **0.7964** | DawidSkene | 0.0245 |
| Text | conll_ner_5k | 5,001 | gpt-4o-mini | **0.9498** | DawidSkene | 0.0300 |
| Text | conll_ner_5k | 5,001 | llama3.1-8b | **0.9412** | DawidSkene | 0.0258 |
| Text | conll_ner_5k | 5,001 | qwen2.5-7b | **0.9454** | DawidSkene | 0.0306 |
| Text | pico_5k | 5,034 | gpt-4o-mini | **0.9607** | ZeroBasedSkill | 0.0147 |
| Text | pico_5k | 5,034 | llama3.1-8b | **0.9587** | MMSR | 0.0252 |
| Text | pico_5k | 5,034 | qwen2.5-7b | **0.9597** | ZeroBasedSkill | 0.0348 |
| Text | quiz | 155 | gpt-4o-mini | **0.7613** | MACE | 0.1290 |
| Text | quiz | 155 | llama3.1-8b | **0.7355** | MACE | 0.1226 |
| Text | quiz | 155 | qwen2.5-7b | **0.7484** | MACE | 0.1097 |
| Image | labelme | 1,000 | gpt-4o-mini | **0.8260** | DawidSkene | 0.0270 |
| Image | labelme | 1,000 | minicpm-v-8b | **0.8030** | DawidSkene | 0.0260 |
| Image | labelme | 1,000 | qwen2.5vl-7b | **0.8050** | DawidSkene | 0.0220 |
| Image | imagenet16h | 4,800 | gpt-4o-mini | **0.8821** | GLAD | 0.0056 |
| Image | imagenet16h | 4,800 | minicpm-v-8b | **0.8781** | GLAD | 0.0085 |
| Image | imagenet16h | 4,800 | qwen2.5vl-7b | **0.8769** | GLAD | 0.0057 |

## macro_f1

| Modality | Dataset | n | model | best | best method | range across 8 |
|---|---|--:|---|--:|---|--:|
| Text | sentiment | 4,999 | gpt-4o-mini | **0.9240** | DawidSkene | 0.0215 |
| Text | sentiment | 4,999 | llama3.1-8b | **0.9264** | MACE | 0.0237 |
| Text | sentiment | 4,999 | qwen2.5-7b | **0.9252** | MACE | 0.0229 |
| Text | movie_reviews | 1,498 | gpt-4o-mini | **0.8053** | MajorityVote | 0.0257 |
| Text | movie_reviews | 1,498 | llama3.1-8b | **0.8127** | MajorityVote | 0.0323 |
| Text | movie_reviews | 1,498 | qwen2.5-7b | **0.7921** | MajorityVote | 0.0249 |
| Text | crowdtruth | 1,596 | gpt-4o-mini | **0.7479** | DawidSkene | 0.0508 |
| Text | crowdtruth | 1,596 | llama3.1-8b | **0.7513** | DawidSkene | 0.0613 |
| Text | crowdtruth | 1,596 | qwen2.5-7b | **0.7501** | DawidSkene | 0.0562 |
| Text | conll_ner_5k | 5,001 | gpt-4o-mini | **0.7666** | DawidSkene | 0.1530 |
| Text | conll_ner_5k | 5,001 | llama3.1-8b | **0.7549** | DawidSkene | 0.1519 |
| Text | conll_ner_5k | 5,001 | qwen2.5-7b | **0.7602** | DawidSkene | 0.1631 |
| Text | pico_5k | 5,034 | gpt-4o-mini | **0.8358** | ZeroBasedSkill | 0.0428 |
| Text | pico_5k | 5,034 | llama3.1-8b | **0.8268** | ZeroBasedSkill | 0.0390 |
| Text | pico_5k | 5,034 | qwen2.5-7b | **0.8319** | ZeroBasedSkill | 0.0463 |
| Text | quiz | 155 | gpt-4o-mini | **0.7868** | MACE | 0.1757 |
| Text | quiz | 155 | llama3.1-8b | **0.7683** | MACE | 0.1810 |
| Text | quiz | 155 | qwen2.5-7b | **0.7776** | MACE | 0.2035 |
| Image | labelme | 1,000 | gpt-4o-mini | **0.8209** | DawidSkene | 0.0265 |
| Image | labelme | 1,000 | minicpm-v-8b | **0.7926** | DawidSkene | 0.0278 |
| Image | labelme | 1,000 | qwen2.5vl-7b | **0.7969** | DawidSkene | 0.0240 |
| Image | imagenet16h | 4,800 | gpt-4o-mini | **0.8812** | ZeroBasedSkill | 0.0530 |
| Image | imagenet16h | 4,800 | minicpm-v-8b | **0.8775** | GLAD | 0.0500 |
| Image | imagenet16h | 4,800 | qwen2.5vl-7b | **0.8763** | GLAD | 0.0520 |


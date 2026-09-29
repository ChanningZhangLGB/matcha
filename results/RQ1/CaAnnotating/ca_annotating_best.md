# CaAnnotating - best allocation per dataset and model

Policy: low-uncertainty (100-X)% keep the LLM label, high-uncertainty X% go to humans. Aggregation is **MajorityVote** for every row (this baseline fixes it); `best` selects over 4 uncertainty bases x 19 budgets.

`gain_vs_random` is the peak minus the random control at the SAME budget -- the test of whether uncertainty ranking selected anything. Non-positive means it did not.

| Modality | Dataset | model | best | uncertainty | X | gain vs random | tied at u=0 |
|---|---|---|--:|---|--:|--:|--:|
| Text | conll_ner_5k | gpt-4o-mini | **0.9362** | inter_rater | 10 | +0.0281 | 85.4% |
| Text | conll_ner_5k | llama3.1-8b | **0.9114** | confidence | 95 | +0.0066 | 29.7% |
| Text | conll_ner_5k | qwen2.5-7b | **0.9116** | entropy | 95 | -0.0001 | 77.3% |
| Text | crowdtruth | gpt-4o-mini | **0.7882** | confidence | 35 | +0.0019 | 0.0% |
| Text | crowdtruth | llama3.1-8b | **0.7907** | entropy | 30 | +0.0194 | 61.2% |
| Text | crowdtruth | qwen2.5-7b | **0.7851** | entropy | 25 | +0.0025 | 71.4% |
| Text | movie_reviews | gpt-4o-mini | **0.7931** | confidence | 80 | +0.0334 | 0.0% |
| Text | movie_reviews | llama3.1-8b | **0.7964** | confidence | 75 | +0.0361 | 0.0% |
| Text | movie_reviews | qwen2.5-7b | **0.7931** | entropy | 70 | +0.0541 | 51.7% |
| Text | pico_5k | gpt-4o-mini | **0.9607** | entropy | 95 | +0.0008 | 89.8% |
| Text | pico_5k | llama3.1-8b | **0.9607** | entropy | 95 | +0.0036 | 70.0% |
| Text | pico_5k | qwen2.5-7b | **0.9607** | entropy | 95 | +0.0036 | 82.0% |
| Text | quiz | gpt-4o-mini | **0.8645** | entropy | 10 | +0.0322 | 77.4% |
| Text | quiz | llama3.1-8b | **0.7355** | entropy | 55 | +0.1032 | 32.9% |
| Text | quiz | qwen2.5-7b | **0.7548** | entropy | 15 | +0.0387 | 38.7% |
| Text | sentiment | gpt-4o-mini | **0.9276** | entropy | 50 | +0.0384 | 86.3% |
| Text | sentiment | llama3.1-8b | **0.9240** | entropy | 10 | +0.0204 | 70.0% |
| Text | sentiment | qwen2.5-7b | **0.9198** | entropy | 15 | +0.0166 | 79.2% |
| Image | imagenet16h | gpt-4o-mini | **0.8733** | confidence | 35 | +0.0489 | 0.0% |
| Image | imagenet16h | minicpm-v-8b | **0.8721** | entropy | 95 | +0.0131 | 54.8% |
| Image | imagenet16h | qwen2.5vl-7b | **0.8715** | confidence | 80 | +0.0428 | 0.0% |
| Image | labelme | gpt-4o-mini | **0.8280** | entropy | 10 | +0.0230 | 76.9% |
| Image | labelme | minicpm-v-8b | **0.8160** | confidence | 75 | +0.0580 | 0.0% |
| Image | labelme | qwen2.5vl-7b | **0.8230** | entropy | 60 | +0.0600 | 74.4% |

# RQ3 — uncertainty basis vs random control: paired significance

Two-sided Wilcoxon signed-rank on paired differences, matched cell by cell (same aggregator, same route, same budget). Holm-Bonferroni across all 72 tests.

**Cells are not independent** (routed sets nest across budgets; aggregators share labels), so p-values are anti-conservative — a screen, not a certificate. `win_rate` and `median_diff` are the effect sizes and are unaffected.

| dataset | model | measure | n | ties | win rate | median Δ | p (Holm) | sig |
|---|---|---|--:|--:|--:|--:|--:|---|
| sentiment | gpt-4o-mini | confidence | 290 | 2 | 0.983 | +0.0100 | 2.26e-47 | yes |
| sentiment | gpt-4o-mini | entropy | 292 | 0 | 1.000 | +0.0170 | 5.54e-48 | yes |
| sentiment | gpt-4o-mini | inter_rater | 292 | 0 | 1.000 | +0.0170 | 5.54e-48 | yes |
| sentiment | llama3.1-8b | confidence | 286 | 5 | 0.839 | +0.0032 | 9.66e-36 | yes |
| sentiment | llama3.1-8b | entropy | 292 | 0 | 0.997 | +0.0088 | 5.54e-48 | yes |
| sentiment | llama3.1-8b | inter_rater | 292 | 0 | 0.997 | +0.0088 | 5.54e-48 | yes |
| sentiment | qwen2.5-7b | confidence | 288 | 4 | 0.910 | +0.0040 | 4.14e-39 | yes |
| sentiment | qwen2.5-7b | entropy | 292 | 0 | 1.000 | +0.0114 | 5.54e-48 | yes |
| sentiment | qwen2.5-7b | inter_rater | 292 | 0 | 1.000 | +0.0114 | 5.54e-48 | yes |
| movie_reviews | gpt-4o-mini | confidence | 304 | 7 | 0.319 | -0.0033 | 0.000554 | WORSE |
| movie_reviews | gpt-4o-mini | entropy | 304 | 0 | 0.895 | +0.0127 | 3.24e-44 | yes |
| movie_reviews | gpt-4o-mini | inter_rater | 304 | 3 | 0.891 | +0.0127 | 3.2e-45 | yes |
| movie_reviews | llama3.1-8b | confidence | 304 | 5 | 0.447 | -0.0020 | 0.0178 | WORSE |
| movie_reviews | llama3.1-8b | entropy | 304 | 2 | 0.967 | +0.0180 | 2.85e-48 | yes |
| movie_reviews | llama3.1-8b | inter_rater | 304 | 1 | 0.977 | +0.0174 | 1.3e-48 | yes |
| movie_reviews | qwen2.5-7b | confidence | 304 | 5 | 0.115 | -0.0107 | 9.42e-42 | WORSE |
| movie_reviews | qwen2.5-7b | entropy | 304 | 0 | 0.997 | +0.0473 | 9.65e-50 | yes |
| movie_reviews | qwen2.5-7b | inter_rater | 304 | 0 | 0.997 | +0.0473 | 9.65e-50 | yes |
| crowdtruth | gpt-4o-mini | confidence | 303 | 25 | 0.248 | -0.0013 | 6.73e-19 | WORSE |
| crowdtruth | gpt-4o-mini | entropy | 303 | 25 | 0.376 | -0.0006 | 0.000127 | WORSE |
| crowdtruth | gpt-4o-mini | inter_rater | 303 | 25 | 0.376 | -0.0006 | 0.000127 | WORSE |
| crowdtruth | llama3.1-8b | confidence | 302 | 3 | 0.950 | +0.0063 | 1.57e-47 | yes |
| crowdtruth | llama3.1-8b | entropy | 304 | 0 | 0.964 | +0.0150 | 2.11e-49 | yes |
| crowdtruth | llama3.1-8b | inter_rater | 304 | 0 | 0.964 | +0.0150 | 2.11e-49 | yes |
| crowdtruth | qwen2.5-7b | confidence | 304 | 14 | 0.562 | +0.0012 | 0.0198 | yes |
| crowdtruth | qwen2.5-7b | entropy | 303 | 22 | 0.442 | +0.0000 | 1 | no |
| crowdtruth | qwen2.5-7b | inter_rater | 303 | 22 | 0.442 | +0.0000 | 1 | no |
| conll_ner_5k | gpt-4o-mini | confidence | 304 | 0 | 1.000 | +0.0089 | 9.65e-50 | yes |
| conll_ner_5k | gpt-4o-mini | entropy | 304 | 0 | 1.000 | +0.0159 | 9.65e-50 | yes |
| conll_ner_5k | gpt-4o-mini | inter_rater | 304 | 0 | 1.000 | +0.0188 | 9.65e-50 | yes |
| conll_ner_5k | llama3.1-8b | confidence | 304 | 0 | 0.789 | +0.0332 | 4.51e-36 | yes |
| conll_ner_5k | llama3.1-8b | entropy | 304 | 0 | 1.000 | +0.0536 | 9.65e-50 | yes |
| conll_ner_5k | llama3.1-8b | inter_rater | 304 | 0 | 0.957 | +0.0542 | 2.03e-49 | yes |
| conll_ner_5k | qwen2.5-7b | confidence | 304 | 0 | 0.891 | +0.0092 | 2.8e-44 | yes |
| conll_ner_5k | qwen2.5-7b | entropy | 304 | 1 | 0.980 | +0.0272 | 1.44e-49 | yes |
| conll_ner_5k | qwen2.5-7b | inter_rater | 304 | 0 | 0.924 | +0.0242 | 5.54e-48 | yes |
| pico_5k | gpt-4o-mini | confidence | 303 | 9 | 0.482 | +0.0000 | 0.856 | no |
| pico_5k | gpt-4o-mini | entropy | 304 | 7 | 0.878 | +0.0066 | 8e-43 | yes |
| pico_5k | gpt-4o-mini | inter_rater | 304 | 7 | 0.878 | +0.0066 | 8e-43 | yes |
| pico_5k | llama3.1-8b | confidence | 303 | 5 | 0.485 | +0.0000 | 0.856 | no |
| pico_5k | llama3.1-8b | entropy | 304 | 0 | 0.990 | +0.0176 | 1.46e-49 | yes |
| pico_5k | llama3.1-8b | inter_rater | 304 | 0 | 0.990 | +0.0176 | 1.46e-49 | yes |
| pico_5k | qwen2.5-7b | confidence | 303 | 2 | 0.277 | -0.0032 | 7.52e-15 | WORSE |
| pico_5k | qwen2.5-7b | entropy | 303 | 0 | 0.970 | +0.0199 | 3.89e-48 | yes |
| pico_5k | qwen2.5-7b | inter_rater | 303 | 0 | 0.970 | +0.0199 | 3.89e-48 | yes |
| quiz | gpt-4o-mini | confidence | 302 | 39 | 0.699 | +0.0129 | 2.21e-24 | yes |
| quiz | gpt-4o-mini | entropy | 304 | 25 | 0.507 | +0.0064 | 0.00207 | yes |
| quiz | gpt-4o-mini | inter_rater | 304 | 25 | 0.507 | +0.0064 | 0.00237 | yes |
| quiz | llama3.1-8b | confidence | 304 | 17 | 0.375 | -0.0129 | 8.78e-05 | WORSE |
| quiz | llama3.1-8b | entropy | 304 | 6 | 0.829 | +0.0580 | 1.68e-41 | yes |
| quiz | llama3.1-8b | inter_rater | 304 | 6 | 0.829 | +0.0516 | 3.01e-41 | yes |
| quiz | qwen2.5-7b | confidence | 303 | 16 | 0.327 | -0.0129 | 7.94e-13 | WORSE |
| quiz | qwen2.5-7b | entropy | 304 | 17 | 0.763 | +0.0258 | 4.13e-20 | yes |
| quiz | qwen2.5-7b | inter_rater | 304 | 16 | 0.766 | +0.0258 | 7.94e-21 | yes |
| labelme | gpt-4o-mini | confidence | 302 | 16 | 0.182 | -0.0040 | 2.39e-25 | WORSE |
| labelme | gpt-4o-mini | entropy | 303 | 4 | 0.868 | +0.0080 | 1.38e-41 | yes |
| labelme | gpt-4o-mini | inter_rater | 303 | 4 | 0.868 | +0.0080 | 1.26e-41 | yes |
| labelme | minicpm-v-8b | confidence | 303 | 4 | 0.941 | +0.0190 | 4.52e-47 | yes |
| labelme | minicpm-v-8b | entropy | 302 | 1 | 0.974 | +0.0230 | 4.1e-49 | yes |
| labelme | minicpm-v-8b | inter_rater | 302 | 1 | 0.974 | +0.0230 | 4.07e-49 | yes |
| labelme | qwen2.5vl-7b | confidence | 303 | 6 | 0.941 | +0.0200 | 2.02e-47 | yes |
| labelme | qwen2.5vl-7b | entropy | 303 | 4 | 0.950 | +0.0230 | 5.54e-48 | yes |
| labelme | qwen2.5vl-7b | inter_rater | 303 | 4 | 0.950 | +0.0230 | 5.54e-48 | yes |
| imagenet16h | gpt-4o-mini | confidence | 304 | 0 | 1.000 | +0.0327 | 9.65e-50 | yes |
| imagenet16h | gpt-4o-mini | entropy | 304 | 0 | 1.000 | +0.0337 | 9.65e-50 | yes |
| imagenet16h | gpt-4o-mini | inter_rater | 304 | 0 | 1.000 | +0.0337 | 9.65e-50 | yes |
| imagenet16h | minicpm-v-8b | confidence | 304 | 0 | 1.000 | +0.0817 | 9.65e-50 | yes |
| imagenet16h | minicpm-v-8b | entropy | 304 | 0 | 1.000 | +0.0803 | 9.65e-50 | yes |
| imagenet16h | minicpm-v-8b | inter_rater | 304 | 0 | 1.000 | +0.0806 | 9.65e-50 | yes |
| imagenet16h | qwen2.5vl-7b | confidence | 304 | 0 | 1.000 | +0.0630 | 9.65e-50 | yes |
| imagenet16h | qwen2.5vl-7b | entropy | 304 | 0 | 1.000 | +0.0604 | 9.65e-50 | yes |
| imagenet16h | qwen2.5vl-7b | inter_rater | 304 | 0 | 1.000 | +0.0617 | 9.65e-50 | yes |

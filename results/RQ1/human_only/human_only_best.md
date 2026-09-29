# RQ1 - Human-only (crowd aggregation): best per dataset

8 crowd-kit aggregators fit on crowd worker labels ONLY -- no LLM in the pool, no gold at fit time (GoldMajorityVote is excluded from the pipeline for that reason). Gold is used only to score.

`best` is a max over the 8 methods selected on the scoring gold, so it is an upper bound; `range` is max - min across the 8.

## accuracy

| Modality | Dataset | n | best | best method | range across 8 |
|---|---|--:|--:|---|--:|
| Text | sentiment | 4,999 | **0.9166** | OneCoinDawidSkene | 0.0344 |
| Text | movie_reviews | 1,498 | **0.7924** | ZeroBasedSkill | 0.0507 |
| Text | crowdtruth | 1,596 | **0.7957** | DawidSkene | 0.0219 |
| Text | conll_ner_5k | 5,001 | **0.9418** | DawidSkene | 0.0310 |
| Text | pico_5k | 5,034 | **0.9615** | ZeroBasedSkill | 0.0413 |
| Text | quiz | 155 | **0.7226** | MACE | 0.1161 |
| Image | labelme | 1,000 | **0.7920** | DawidSkene | 0.0300 |
| Image | imagenet16h | 4,800 | **0.8767** | Wawa | 0.0052 |

## macro_f1

| Modality | Dataset | n | best | best method | range across 8 |
|---|---|--:|--:|---|--:|
| Text | sentiment | 4,999 | **0.9166** | OneCoinDawidSkene | 0.0346 |
| Text | movie_reviews | 1,498 | **0.7826** | ZeroBasedSkill | 0.0494 |
| Text | crowdtruth | 1,596 | **0.7495** | DawidSkene | 0.0498 |
| Text | conll_ner_5k | 5,001 | **0.7529** | DawidSkene | 0.1640 |
| Text | pico_5k | 5,034 | **0.8414** | ZeroBasedSkill | 0.1094 |
| Text | quiz | 155 | **0.7547** | MACE | 0.2005 |
| Image | labelme | 1,000 | **0.7861** | DawidSkene | 0.0305 |
| Image | imagenet16h | 4,800 | **0.8760** | Wawa | 0.0053 |


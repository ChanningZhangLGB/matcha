# Human-only (crowd aggregation), accuracy

8 crowd-kit aggregators fit on crowd worker labels only -- no LLM, no gold at fit time.

**Model-independent**: the same value applies under all three model columns of the submission table.

| Modality | Dataset | n | MajorityVote | Wawa | ZeroBasedSkill | DawidSkene | OneCoinDawidSkene | GLAD | MACE | MMSR | best | best method |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|
| Text | sentiment | 4,999 | 0.8822 | 0.8948 | 0.8946 | 0.9152 | 0.9166 | 0.9166 | 0.9148 | 0.9008 | **0.9166** | OneCoinDawidSkene |
| Text | movie_reviews | 1,498 | 0.7710 | 0.7864 | 0.7924 | 0.7824 | 0.7824 | 0.7824 | 0.7904 | 0.7417 | **0.7924** | ZeroBasedSkill |
| Text | crowdtruth | 1,596 | 0.7738 | 0.7738 | 0.7738 | 0.7957 | 0.7807 | 0.7851 | 0.7876 | 0.7845 | **0.7957** | DawidSkene |
| Text | conll_ner_5k | 5,001 | 0.9142 | 0.9234 | 0.9248 | 0.9418 | 0.9108 | 0.9240 | 0.9234 | 0.9242 | **0.9418** | DawidSkene |
| Text | pico_5k | 5,034 | 0.9607 | 0.9601 | 0.9615 | 0.9491 | 0.9575 | 0.9587 | 0.9567 | 0.9201 | **0.9615** | ZeroBasedSkill |
| Text | quiz | 155 | 0.6065 | 0.6581 | 0.6645 | 0.6065 | 0.6968 | 0.6387 | 0.7226 | 0.6323 | **0.7226** | MACE |
| Image | labelme | 1,000 | 0.7620 | 0.7640 | 0.7780 | 0.7920 | 0.7670 | 0.7750 | 0.7730 | 0.7670 | **0.7920** | DawidSkene |
| Image | imagenet16h | 4,800 | 0.8715 | 0.8767 | 0.8762 | 0.8760 | 0.8760 | 0.8765 | 0.8765 | 0.8746 | **0.8767** | Wawa |

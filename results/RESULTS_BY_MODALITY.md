# Results by modality — text arm vs image arm

Generated from `results/by_modality/` (see `results/utils/build_modality_split.py`).
Per-dataset directories under `results/<dataset>/` are unchanged; only the cross-dataset
roll-ups are split here, because the two arms use **different annotator line-ups** and
cannot be read as a single table.

| | datasets | instances | LLM annotators |
|---|--:|--:|---|
| **text** | 7 | 18,283 | gpt-4o-mini · llama3.1-8b-q8_0 · qwen2.5-7b-q8_0 |
| **image** | 2 | 5,800 | gpt-4o-mini · minicpm-v-2.6-q8_0 · qwen2.5-VL-7b-q8_0 |

**gpt-4o-mini is the only model spanning both arms** (it is multimodal). The other four
appear in exactly one, so it is the sole point of direct cross-modal comparison — the
text/image contrast is otherwise confounded with a change of model.

---

## Human crowd vs LLM (best aggregator vs best model, accuracy)

### Text arm

| dataset | best human | best LLM | gap |
|---|---|---|--:|
| sentiment | GLAD 0.9166 | llama3.1-8b 0.9068 | −0.0098 |
| movie_reviews | ZeroBasedSkill 0.7924 | gpt-4o-mini 0.7483 | −0.0441 |
| crowdtruth_cause | MACE 0.7692 | gpt-4o-mini 0.7713 | **+0.0021** |
| crowdtruth_treat | GLAD 0.8293 | gpt-4o-mini 0.8052 | −0.0241 |
| conll_ner_5k | DawidSkene 0.9418 | gpt-4o-mini 0.9069 | −0.0349 |
| pico_5k | ZeroBasedSkill 0.9615 | gpt-4o-mini 0.9406 | −0.0209 |
| quiz | MACE 0.7226 | gpt-4o-mini 0.8387 | **+0.1161** |

Humans win 5 of 7. The two LLM wins are not equivalent: `crowdtruth_cause` is a tie within
noise, while `quiz`'s +0.1161 reflects an unusually weak crowd (near-chance on knowledge
questions) rather than unusual model strength — see `project_matcha_quiz_caveats`.

### Image arm

| dataset | best human | best LLM | gap |
|---|---|---|--:|
| labelme | DawidSkene 0.7920 | gpt-4o-mini 0.8140 | **+0.0220** |
| imagenet16h | Wawa 0.8767 | gpt-4o-mini 0.7973 | −0.0794 |

The two image datasets land on **opposite sides**, and that contrast is the most useful
result here. It is not "images are hard for models" — it is that **stimulus degradation
specifically** flips the advantage. On clean scene photographs the model substitutes for
the crowd; on phase-noise-degraded images a 6-judgment human crowd holds an 8-point lead
that no VLM closes. The open VLMs are far further behind on imagenet16h (0.6229, 0.6523)
than on labelme (0.7460, 0.7600).

---

## Allocation / routing

| | peak human budget X | cost saved at peak |
|---|---|---|
| **text** (21 rows) | min 10% · median 60% · max 95% | min 5.0% · median 40.0% · max 90.0% |
| **image** (6 rows) | min 35% · median **85%** · max 95% | min 0.7% · median 30.0% · max 57.6% |

The image arm's peak budget sits much higher (median 85% vs 60%). On `imagenet16h` every
model peaks at X=85–95%, i.e. the optimal policy is "route almost everything to humans",
and the accuracy gain over pure human-only is negligible (+0.0004 to +0.0073). Routing has
little to contribute where humans already dominate. `labelme` behaves like the text
datasets — moderate budgets (35–70%) buy a real gain (+0.028 to +0.040) at 30–58% saving.

### Caveat on the image peaks — read before quoting them

`entropy` won **4 of the 6** image peaks, and entropy is tie-degenerate on both image
datasets: only 10–27 distinct values with **55–77% of instances tied at u=0**, and
`build_uncertainty_splits.py` reports **19/19 arbitrary budget cuts**. Checked directly
against the alternatives at the same budget:

| case | entropy | confidence | random |
|---|--:|--:|--:|
| gpt-4o-mini / labelme / X=35% | **0.8320** | 0.8080 | 0.8080 |
| gpt-4o-mini / imagenet16h / X=95% | **0.8840** | 0.8817 | 0.8781 |
| qwen2.5-VL / labelme / X=70% | **0.8280** | 0.7990 | 0.7820 |
| MiniCPM-V / imagenet16h / X=95% | **0.8792** | 0.8783 | 0.8665 |

Entropy does beat both alternatives everywhere, so the wins are not pure tie-breaking
artefacts. But on **imagenet16h the margin over confidence is 0.1–0.2 points** — too thin
to treat as a finding given the tie structure. The labelme margins (2–4 points) are more
solid. `confidence` is the only image-arm measure with genuine ranking power (28–122
distinct values, 0% tied).

---

## Cost

Human annotation cost differs by three orders of magnitude across the arms, which drives
the routing economics:

- text: pico_5k $19,449 · conll_ner_5k $4,381 · crowdtruth_cause $1,927 · sentiment $925
- image: **imagenet16h $442 · labelme $53** — the two cheapest tasks in the project

`imagenet16h` uses **measured** timing (median 3.66s/judgment, from the corpus's own
per-trial `total_time`); `labelme` ships none and uses an assumption of 5.0s anchored to
that measurement. Only gpt-4o-mini incurs LLM cost ($3.94 labelme / $19.02 imagenet16h);
both VLMs run locally and are priced at zero, matching the text-arm convention.

Because human cost is so low on the image arm, the *dollar* saving from routing is small
in absolute terms even at high saving percentages — imagenet16h's peak saves 0.7–15%,
i.e. **$3–$66**.

---

## Files

```
results/by_modality/
  text/   overview_human_vs_llm.csv (7)   overview_human_plus_llm.csv (28)
          allocation_best.csv (21)        budget.csv (21)
  image/  overview_human_vs_llm.csv (2)   overview_human_plus_llm.csv (8)
          allocation_best.csv (6)         budget.csv (6)
```

Verified free of cross-arm contamination: no text dataset or text-only model appears in
`image/`, and vice versa. Columns for models that never ran on an arm are dropped rather
than left blank.

Model-behaviour findings specific to the image arm (refusal rates, confidence coarseness,
top-k `k`-adherence) are in `results/IMAGE_MODEL_BEHAVIOR.md`.

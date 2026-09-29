# Image-arm model behavior — verification findings

Recorded 2026-08-07, after the `_image` payload bug was fixed and all 156,600 records
regenerated clean (see `eval/llm/validate_image_runs.py`, 0 FAIL / 465 benign WARN). These
are decisions about how to *read* the data, not defects in it.

## 1. top-k `k` adherence — accepted as-is, top answer taken regardless

The prompts ask for the 3 best guesses. Not every model returns exactly 3:

| model | records with k≠3 | pattern |
|---|--:|---|
| qwen2.5vl-7b-q8_0 | 1 / 12,600 | effectively perfect |
| gpt-4o-mini | 126 / 12,600 | all k=1, confined to `imagenet16h` |
| minicpm-v-8b-2.6-q8_0 | 1,235 / 12,600 (9.8%) | k up to 28; spikes at k=8 (labelme, all 8 categories) and k=16 (imagenet16h, all 16 categories) — it sometimes ranks the entire category list instead of picking 3 |

**Decision: leave as-is.** `top_answer()` already takes the highest-probability guess
regardless of list length, so every hard-label score in this project (majority vote,
accuracy, aggregation) is unaffected. The only thing this limits is analysis that would
consume the *full ranked list* rather than the top pick — not something currently computed.
MiniCPM-V's list-length quirk should be named if such an analysis is ever added, since its
guess distribution is not shaped like the other two models'.

## 2. Refusals and low/coarse confidence — kept as evidence of model competence, not filtered as noise

Both `imagenet16h` prompts state "none of the above" is *not* an available option. A model
saying it anyway is a real refusal to commit, not a parsing artifact, and is scored as
**incompetence signal**, not discarded as noise.

### Refusal rate (`vanilla`, name-answer groups — `customized` has no refusal option in its letter space)

| model | labelme | imagenet16h basic | imagenet16h control |
|---|--:|--:|--:|
| gpt-4o-mini | 0.0% | 2.3% | 16.8% |
| **minicpm-v-8b-2.6-q8_0** | 0.0% | **31.2%** | **37.2%** |
| qwen2.5vl-7b-q8_0 | 0.0% | 1.5% | 3.9% |

MiniCPM-V refuses roughly **10–20x more often** than the other two on the harder,
noise-degraded dataset. None of the three ever refuses on LabelMe (clean photographs) —
the refusal behavior is specific to genuinely difficult stimuli, which is the intended
reading: it is a response to task difficulty, not a general prompt-following failure.

The **control group amplifies refusal for every model** (basic → control: gpt 2.3%→16.8%,
minicpm 31.2%→37.2%, qwen 1.5%→3.9%) despite control being a pure wording paraphrase with
identical categories, order, and schema. Wording alone shifts willingness to commit by a
large factor. This must be reported alongside any basic-vs-control accuracy comparison
(see `project_matcha_image_arm.md`: gpt's control accuracy is computed on fewer, refused-down
items and is not directly comparable to basic's for that reason).

### Confidence distribution (`vanilla`, `basic_instruction`)

| model | dataset | mean | median | distinct values | most common |
|---|---|--:|--:|--:|---|
| gpt-4o-mini | labelme | 90.0 | 90 | 6 | 90 (39%), 95 (32%), 85 (27%) |
| gpt-4o-mini | imagenet16h | 74.9 | 85 | 13 | 85 (44%) |
| minicpm-v | labelme | 89.4 | 90 | 4 | 90 (82%) |
| **minicpm-v** | **imagenet16h** | **67.3** | 70 | **4** | 80 (38%), 50 (34%), 70 (26%) |
| qwen2.5vl | labelme | 90.1 | 90 | 4 | 90 (86%) |
| qwen2.5vl | imagenet16h | 78.7 | 80 | 6 | 80 (57%) |

All three models are coarse on the clean LabelMe photos (3–6 distinct confidence values,
heavily piled on 90) — this looks like a reporting habit more than genuine calibration.
On the noise-degraded imagenet16h stimuli, confidence drops and spreads out for gpt-4o-mini
(13 distinct values, mean 74.9) but **stays just as coarse for minicpm-v (4 values)**, with
mean confidence dropping to 67.3 and a visible cluster at 50 — the "I don't know" value.
**qwen's confidence barely moves and stays coarse** (6 values, mean 78.7) despite the harder
task, which combined with its near-zero refusal rate suggests qwen is not adjusting its
stated certainty to match actual task difficulty as much as the other two.

### Coverage vs. accuracy-when-answered

This is the number that complicates a pure "MiniCPM-V is worse" reading of its refusal
rate, and is worth carrying into any accuracy table:

| model | dataset | n | answered | coverage | accuracy (of answered) |
|---|---|--:|--:|--:|--:|
| gpt-4o-mini | labelme | 1,000 | 1,000 | 100.0% | 0.7960 |
| gpt-4o-mini | imagenet16h | 4,800 | 4,690 | 97.7% | 0.8060 |
| minicpm-v | labelme | 1,000 | 998 | 99.8% | 0.7515 |
| **minicpm-v** | **imagenet16h** | 4,800 | 3,291 | **68.6%** | **0.8812** |
| qwen2.5vl | labelme | 1,000 | 1,000 | 100.0% | 0.7750 |
| **qwen2.5vl** | **imagenet16h** | 4,800 | 4,718 | 98.3% | **0.6568** |

MiniCPM-V has the **highest** accuracy of the three when it commits to an answer (0.8812),
but only commits 68.6% of the time. Qwen commits almost always (98.3%) and is the **least**
accurate (0.6568). Read together with the refusal and confidence numbers above, MiniCPM-V's
high refusal rate looks less like blanket incompetence and more like a selective-prediction
pattern — it declines on the images it would get wrong. Qwen shows the opposite pattern:
near-total coverage bought at the cost of accuracy, with confidence that does not track
this. Both readings ("high refusal = incompetence" and "high refusal = selective
competence") are defensible from this data; report coverage alongside accuracy rather than
accuracy alone whenever these models are compared.

## Net effect on the pipeline

No FAILs. `map_labelme`/`map_imagenet16h` already drop refusals from the scored set
(`_norm_cat` + the refusal-set check in `score_llm.py`) rather than mis-scoring them, so
`categorical.csv`/`crowd_aggregation.csv` accuracy numbers are already accuracy-of-answered,
not accuracy-of-all. Coverage is the missing column — add it wherever these numbers are
tabled, since it is not derivable from accuracy alone and materially changes which model
looks best.

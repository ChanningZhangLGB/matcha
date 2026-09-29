# eval — two validation tracks

```
eval/
├── convert/build_all.py     datasets_pass/ -> crowd-kit long form
├── common/{paths,metrics}.py
├── data/                    <name>_crowd.csv (task,worker,label) + <name>_gold.csv
├── run_categorical.py       TRACK 1: 8 aggregators x 6 tables
├── run_regression.py        TRACK 2: MovieReviews, continuous
└── results/{categorical,regression}.csv
```

Environment: Python 3.11 with `requirements.txt` (crowd-kit 1.4.2).
**scikit-learn is pinned `<1.6`** — under 1.6+ `Wawa` and `ZeroBasedSkill` die with
`AttributeError: '...' object has no attribute '__sklearn_tags__'`.

```bash
python eval/convert/build_all.py
python eval/run_categorical.py          # or: ... run_categorical.py sentiment pico
python eval/run_regression.py
```

## Track 1 — categorical

Eight aggregators: MajorityVote, DawidSkene, OneCoinDawidSkene, GLAD, MACE, MMSR, Wawa,
ZeroBasedSkill. **GoldMajorityVote is excluded**: it takes `true_labels` at `fit()`, so it would be
scored against gold it had already seen.

Tables actually evaluated (marked ✔), plus the full-size variants kept on disk:

| Table | Tasks | Workers | Judgments | Classes | Recast | |
|---|--:|--:|--:|--:|---|:--:|
| `sentiment` | 4,999 | 203 | 27,746 | 2 | none (native) | ✔ |
| `movie_reviews` | 1,498 | 135 | 7,430 | 3 | **bin** | ✔ |
| `crowdtruth_cause` | 975 | 304 | 14,920 | 2 | none | ✔ |
| `crowdtruth_treat` | 621 | 286 | 9,610 | 2 | none | ✔ |
| `conll_ner_5k` | 5,001 | 47 | 23,366 | 9 | **tok** + subsample | ✔ |
| `pico` | 44,456 | 91 | 272,433 | 2 | **tok** | ✔ |
| `conll_ner` (full) | 79,901 | 47 | 366,370 | 9 | **tok** | |
| `pico_5k` | 5,034 | 50 | 31,119 | 2 | **tok** + subsample | |

### Subsampling (`convert/subsample.py`, seed 42)

CoNLL is subsampled to ~5,000 tasks because its 79,901 tokens × 9 classes dominated runtime.
**Units are drawn whole** — 392 complete sentences of 5,985 (6.5%) — so no token is ever separated
from its sentence. The target is approached from below and overshot by the final unit, giving 5,001.

PICO is **run at full size**. Subsampling it to 5,000 tokens would have cost all but **22 of its 191
documents** and dropped worker coverage from 91 to 50; it is the smallest gold set in the collection
and could not absorb that. `pico_5k` is generated and kept for reference but is not evaluated.

Note the task counts overstate independence for both token-recast tables: PICO's 44,456 tasks come
from 191 documents, and `conll_ner_5k`'s 5,001 from 392 sentences.

Metrics: accuracy, macro-F1, weighted-F1, plus binary F1 on the positive class where one is
meaningful (`pos`, `yes`, `in`).

### Recast details

- **movie_reviews (bin)** — ratings mapped `[0, .35) → poor`, `[.35, .65) → medium`,
  `[.65, 1] → good`. Applied identically to worker answers and to gold.
  Resulting balance: workers 19/49/32%, gold 12/50/38%. Only **19.4%** of items are unanimous
  after binning, so 4 in 5 items carry real disagreement.
  ⚠️ 5 of 7,430 worker ratings are `-0.1` or `1.1`, outside `[0,1]`. `pd.cut(bins=[0,.35,.65,1])`
  would turn these into `NaN` and silently drop them, so `common.paths.bin_rating` uses an explicit
  cascade instead. Separately, `-1` is the missing sentinel while `-0.1` is a **valid rating** —
  never filter with `>= 0`.
- **conll_ner (tok)** — one task per token (`s{sent}_t{tok}`), one worker per annotator column,
  `?` dropped. Sequence structure is discarded by construction.
- **pico (tok)** — one task per whitespace token (`{docid}_{i}`), label `in`/`out` of span.
  Only workers who annotated a given document emit labels for that document's tokens, which is what
  makes the negatives meaningful. Character-level would give 1.87M rows instead of 272k and add
  nothing, since spans are contiguous.
  ⚠️ Positive rate is **10.2%** — read macro-F1 / `f1_in`, not accuracy, since all-`out` scores ~90%.
  Workers per doc: median 6, but **min 1**; single-annotator docs carry no aggregation signal.
- **crowdtruth** — binary per relation, from RelEx `step_1_select_the_valid_relations`
  (`[CAUSES]` / `[TREATS]`). Joined to gold on base SID (`sent_id` up to the first `-`),
  OR-ed across term pairs within a (sentence, worker).

## Track 2 — regression (MovieReviews only)

No binning; operates on the raw continuous ratings.

| Method | What it is |
|---|---|
| **Mean** | per-item average. The **only** aggregation the paper used for MovieReviews (Table 2, `DL (Mean)`). Verified identical to the shipped `ratings_train_mean.txt` to 1.1e-16. |
| **EMBias** | **ours, not theirs.** Adopts the paper's best crowd-layer variant `"B"`, `f_r(mu) = mu + b_r`, fit by EM on the answer matrix alone. |
| *shipped_DS* | reference column only — `ratings_train_DS.txt` corresponds to **no method in the paper**. |

Metrics: MAE, RMSE, R², Pearson r, computed on the 1,498 training items against
`ratings_train.txt`.

### Results

| Method | MAE | RMSE | R² | r |
|---|--:|--:|--:|--:|
| Mean | 0.0607 | 0.0755 | 0.830 | 0.928 |
| EMBias (ours) | 0.0492 | 0.0587 | 0.897 | 0.967 |
| *shipped_DS* | *0.0436* | *0.0535* | *0.914* | *0.974* |

Learned annotator biases `b_r` have sd 0.114 and range `[-0.287, +0.433]` — substantial systematic
bias, consistent with the paper's finding that the bias-only variant beat both scale and scale+bias.

### Provenance cautions

- **EMBias shares the paper's theory, not its procedure.** They trained the `"B"` model end-to-end
  inside a CNN; this fits the same annotator model by EM with no features. Never report it as a
  replication of `DL-Crowds (B)`.
- **These numbers are not comparable to the paper's Table 2.** Table 2 reports a CNN evaluated on
  the 3,506-item *test* set on a 1–10 scale; this evaluates aggregation output on the 1,498 *train*
  items on the [0,1] scale.
- Track 1 and Track 2 both cover MovieReviews under different framings, so the two tracks' numbers
  are not comparable to each other either — but the *ranking* of methods across framings is a fair
  question to ask.

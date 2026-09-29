# Crowd-Kit method compatibility per dataset

Against `crowdkit.aggregation` on `main` (v1.4.2), 22 exported classes.
Legend: **✅ native** = works on a direct `task/worker/label` melt · **⚙️ transform** = works after a
documented recast · **❌** = not applicable.

## Matrix

| Method | Family | sentiment | movie_rev | conll_ner | crowdtruth | pico | quiz | labelme | imagenet16h |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| MajorityVote | classif | ✅ | ⚙️ bin | ✅ tok | ✅ | ⚙️ tok | ✅ | ✅ | ✅ |
| DawidSkene | classif | ✅ | ⚙️ bin | ✅ tok | ✅ | ⚙️ tok | ✅ | ✅ | ✅ |
| OneCoinDawidSkene | classif | ✅ | ⚙️ bin | ✅ tok | ✅ | ⚙️ tok | ✅ | ✅ | ✅ |
| GoldMajorityVote | classif | ✅ | ⚙️ bin | ✅ tok | ✅ | ⚙️ tok | ✅ | ✅ | ✅ |
| GLAD | classif | ✅ | ⚙️ bin | ✅ tok | ✅ | ⚙️ tok | ✅ | ✅ | ✅ |
| **KOS** | classif | ✅ | ⚙️ 2-bin | ❌ **9 tags** | ✅ | ⚙️ tok | ❌ **6 opts** | ❌ **8 cls** | ❌ **16 cls** |
| MACE | classif | ✅ | ⚙️ bin | ✅ tok | ✅ | ⚙️ tok | ✅ | ✅ | ✅ |
| MMSR | classif | ✅ | ⚙️ bin | ✅ tok | ✅ | ⚙️ tok | ✅ | ✅ | ✅ |
| Wawa | classif | ✅ | ⚙️ bin | ✅ tok | ✅ | ⚙️ tok | ✅ | ✅ | ✅ |
| ZeroBasedSkill | classif | ✅ | ⚙️ bin | ✅ tok | ✅ | ⚙️ tok | ✅ | ✅ | ✅ |
| BinaryRelevance | multilabel | ❌ | ❌ | ❌ | ✅ **RelEx** | ❌ | ❌ | ❌ | ❌ |
| ClosestToAverage | embed | ❌ | ✅ | ⚙️ | ⚙️ FactSpan | ⚙️ | ❌ | ❌ | ❌ |
| RASA | embed | ❌ | ⚙️ | ⚙️ | ⚙️ FactSpan | ⚙️ | ❌ | ❌ | ❌ |
| HRRASA | embed | ❌ | ⚙️ | ⚙️ | ⚙️ FactSpan | ⚙️ | ❌ | ❌ | ❌ |
| TextRASA | text | ❌ | ❌ | ⚙️ | ✅ FactSpan | ❌ | ❌ | ❌ | ❌ |
| TextHRRASA | text | ❌ | ❌ | ⚙️ | ✅ FactSpan | ❌ | ❌ | ❌ | ❌ |
| ROVER | text | ❌ | ❌ | ✅ tag seq | ✅ FactSpan | ❌ | ❌ | ❌ | ❌ |
| SegmentationMajorityVote | segm | ❌ | ❌ | ❌ | ⚙️ FactSpan | ✅ **1D ok** | ❌ | ❌ | ❌ |
| SegmentationRASA | segm | ❌ | ❌ | ❌ | ⚙️ | ⚙️ reshape | ❌ | ❌ | ❌ |
| SegmentationEM | segm | ❌ | ❌ | ❌ | ⚙️ | ⚙️ reshape | ❌ | ❌ | ❌ |
| BradleyTerry | pairwise | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| NoisyBradleyTerry | pairwise | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Native totals:** sentiment 10 · movie_reviews 1 · conll_ner 10 · crowdtruth 14 · pico 1 · quiz 9 · labelme 9 · imagenet16h 9.

### quiz_crowd_li — **9 native**
`task=<prefix><n>, worker=<prefix>_workerN, label=A..F` on the pooled 155-item table, already in
long form (`eval/data/quiz_{crowd,gold}.csv`) — no melt needed, and the matrix is 100% dense.
The full categorical family applies **except KOS**, which is binary-only and rejects the 6-option
pool. Workers emit an option letter, not free text, a region, or a vector, so the embedding, text,
segmentation, multilabel, and pairwise families are all out.

⚠️ A–F is **not a shared class space** — "C" is a different option in every question, and option
counts differ across subsets (4/5/6). Methods that estimate a global class prior or a full K×K
confusion matrix (DawidSkene, GLAD, MACE, MMSR) are pooling parameters that have no cross-subset
meaning. They still fit and still beat chance, but read accuracy only; per-class F1 is an artefact.

### labelme_crowd — **9 native**
`task=<image stem>, worker=w00..w76, label=<class name>` from a melt of the 1,000 × 77
`answers.txt` (`-1` = not annotated). All categorical **except KOS** (8 classes, binary-only).
Workers emit a class label, so embedding / text / segmentation / multilabel / pairwise are out.

⚠️ **Drop the 18 all-empty worker columns before fitting.** An annotator with zero observations
contributes no information but still gets a confusion matrix in DawidSkene/GLAD/MACE.
`build_labelme.py` drops them, leaving 59.

⚠️ **Do not report MajorityVote here.** At 2.55 labels/image, 12.9% of tasks have a tied top vote,
and MV moves ~±0.7 pts on tie policy alone (0.7620 / 0.7690 / 0.7760 from three implementations).
DawidSkene (0.7920) is the number to quote; the aggregator spread is 3.0 pts.

### imagenet16h — **9 native**
`task=<image>_n<level>, worker=<worker_id>, label=<category>` — already long form, no melt.
All categorical **except KOS** (16 classes). Same exclusions as labelme for the other families.

⚠️ **The aggregator choice is nearly irrelevant**: all eight land within 0.5 pts (0.8715–0.8767),
and plain **Wawa** nominally wins over GLAD/MACE/DawidSkene. With 6 judgments per task from a
competent crowd there is little annotator unreliability left for the skill-modelling methods to
recover. Contrast `quiz`, where MACE beats MV by 11.6 pts.

⚠️ **MACE costs ~198s on the full table, GLAD ~59s** — the largest table here. Budget accordingly
before any sweep that re-fits per cell.

## Per dataset

### sentiment_polarity_ma_lr — **10 native**
`task=Input.id, worker=WorkerId, label=Answer.sent`. Binary (pos/neg), so the full categorical
family applies **including KOS**. This is the only dataset besides CrowdTruth where KOS runs
without recasting.
Not applicable: workers emit a class label, not free text or a region, so all embedding/text/
segmentation methods are out.

### movie_reviews_crowd — **1 native, 10 after binning**
Continuous target in [0,1], so no categorical aggregator applies directly.
- **ClosestToAverage** ✅ — set `output=rating`, `embedding=np.array([rating])`, `distance=abs`.
  Note this returns a **medoid** (nearest observed rating), not the mean.
- ⚙️ Binning the ratings into k classes unlocks all 10 categorical methods; k=2 also unlocks KOS.
- ⚙️ RASA/HRRASA run on a 1-D embedding but are designed for high-dim response embeddings.
- Melt required: `answers.txt` is 1,498 × 135 wide with `-1` sentinels — drop the -1 cells.

### conll2003_ner_crowd — **10 native**
Two framings, both native:
- **Token level** — `task=(sent_id, tok_idx)`, `label=BIO tag`. All categorical **except KOS**
  (9 distinct tags; KOS raises `ValueError: KOS aggregation method is for binary classification only`).
  9 methods. Discards sequence structure.
- **Sequence level** — **ROVER** ✅ with `text=' '.join(tags)`, `tokenizer=str.split`. Preserves the
  sequence and is the intended use of ROVER's alignment voting.
- ⚙️ TextRASA/TextHRRASA work if you encode tag sequences, but a sentence encoder on BIO strings is
  semantically odd — treat as exploratory only.
- Melt required: 47 annotator columns, `?` = not annotated.

### crowdtruth_medical_re — **14 native, the richest**
Three annotation sub-tasks give three distinct framings:
- **RelEx as binary** — "does this sentence express `cause`/`treat`?" against the expert column.
  All 10 categorical, **KOS included**.
- **RelEx as multi-label** — workers tick multiple relations in
  `step_1_select_the_valid_relations`. **BinaryRelevance** ✅, wrapping any categorical base
  aggregator (e.g. `BinaryRelevance(DawidSkene(n_iter=10))`). This is the only dataset in the set
  with a genuine multi-label signal.
- **FactSpan as text** — workers copy-paste the words expressing the relation
  (`step_2a_...`). **ROVER / TextRASA / TextHRRASA** ✅.
- ⚙️ FactSpan recast as token masks also admits the segmentation family.
- `_worker_id` is the worker key; join to gold on base SID (`sent_id` up to the first `-`).

### pico_data — **1 native, 10 after token melt**
Character spans over abstracts.
- **SegmentationMajorityVote** ✅ — verified dimension-agnostic (it does elementwise
  `segmentation * skill`, sums, thresholds at 0), so 1-D boolean char/token masks work as-is.
- ⚙️ **SegmentationRASA / SegmentationEM** — both hard-code `.sum(axis=(1,2))`, i.e. 2-D masks.
  Reshape each 1-D mask of length N to `(1, N)` and they run correctly.
- ⚙️ **Token/char level binary** — `task=(docid, tok_idx)`, `label ∈ {0,1}` for in-span. Unlocks all
  10 categorical methods including KOS. This is the standard PICO evaluation framing.
- Gold is `MedicalStudent` in `PICO-annos-professional.json`, 191 docs.

## Cross-cutting notes

- **Pairwise (BradleyTerry, NoisyBradleyTerry) applies to nothing here** — no dataset collects
  pairwise preferences. Rules out 2 of 22 outright.
- **GoldMajorityVote needs `true_labels` at fit time** (`fit(data, true_labels)`) to estimate worker
  accuracy. Every dataset here has gold, but fitting on the evaluation gold leaks; hold out a
  disjoint calibration split.
- **RASA/HRRASA vs TextRASA/TextHRRASA** — the former take a precomputed `embedding` column, the
  latter wrap an encoder callable over an `output` column. Same algorithm, different entry point.
- All categorical methods want the long form `task | worker | label`; most datasets need a melt or
  explode first. `quiz` and `imagenet16h` are the exceptions — their converters emit long form
  directly.
- **Annotation depth drives whether the aggregator matters at all.** Ranked by judgments per
  instance: crowdtruth 15.4 · quiz 57.6 · imagenet16h 6.0 · pico 6.1 · sentiment 5.6 ·
  movie_reviews 5.0 · conll_ner 4.7 · labelme 2.55. But depth alone does not predict the spread —
  what matters is how much annotator skill VARIES. quiz (deep, near-chance crowd) shows an 11.6-pt
  gap between MACE and MV; imagenet16h (deep, competent crowd) shows 0.5 pts; labelme (very thin)
  shows 3.0 pts but with tie-unstable MV.
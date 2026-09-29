# datasets_pass — working set

The five TEXT datasets that meet all four criteria (NLP task · public instances · individual
annotator labels · ground truth), plus `quiz_crowd_li` and two IMAGE datasets added later on
request, each carrying the caveats listed below. Built from `../datasets/` by
`../build_datasets_pass.py` — rerun it to regenerate. Full unfiltered copies stay in
`../datasets/`; the audit is in `../datasets/AUDIT.md`.

The image datasets were audited against **three** criteria, not four: the NLP-task criterion
does not apply to them. They exist to extend the human–AI allocation framing beyond text, so
they are annotated by VLMs rather than by the three text models.

| Dataset | Task | Instances | Workers | Judgments | Gold |
|---|---|--:|--:|--:|---|
| `sentiment_polarity_ma_lr` | binary sentiment | 4,999 | 203 | 27,746 (5.6/inst) | all rows |
| `movie_reviews_crowd` | rating regression | 1,498 | 135 | 7,430 (5.0/doc) | all docs |
| `conll2003_ner_crowd` | NER sequence labelling | 5,985 sents / 79,901 tok | 47 | 47 label cols | all sents |
| `crowdtruth_medical_re` | relation extraction | 975 sents | 304 | 15,035 (15.4/sent) | all rows (filtered) |
| `pico_data` | span annotation | 191 docs | 91 | 1,165 (6.1/doc) | all docs (filtered) |
| `quiz_crowd_li` | multiple-choice QA | 155 questions | 360 | 8,930 (57.6/q) | all questions |
| `labelme_crowd` | image scene classification (8-way) | 1,000 images | 59 | 2,547 (2.55/img) | all images (filtered) |
| `imagenet16h` | image classification (16-way) | 4,800 = 1,200 img × 4 noise | 145 | 28,997 (6.04/inst) | all instances (filtered) |

Copied whole: `sentiment_polarity_ma_lr`, `movie_reviews_crowd`, `conll2003_ner_crowd`,
`quiz_crowd_li` — every instance already carries both gold and per-annotator labels.

## Filtered to gold-labelled subsets

### crowdtruth_medical_re
Kept only rows with a non-NA `expert` column, and the `raw/` worker judgments that join to them.

- `ground_truth_cause.csv` — 3,984 → **975** (expert: 247 positive / 728 negative)
- `ground_truth_treat.csv` — 3,984 → **621** (expert: 294 positive / 327 negative)
  Note the 621 treat sentences are a **subset** of the 975 cause sentences, so the union is 975.
- `raw/RelEx/` — 50,962 → **15,035** judgments, 304 workers, all 975 sentences (15.4/sent)
- `raw/RelDir/` — 22,176 → **9,407** judgments, 445 workers, 871 sentences
- `raw/FactSpan/` — 38,001 → **8,400** judgments, 307 workers, 840 sentences

Join key: base SID = `sent_id` truncated at the first `-` (raw ids carry `-FS1`, `-FS1-2` suffixes).
Per-worker fields: `_worker_id`, `_trust`, `_country`, `step_1_select_the_valid_relations`.
The `baseline` column (UMLS distant supervision) is retained but is **not** human gold.

### pico_data
Kept only `acl17-test`, the sole split with professional annotations.

- 191 documents, crowd + professional docids match exactly, all 191 abstracts present in `docs/`.
- Gold `PICO-annos-professional.json` has a single annotator key, `MedicalStudent`.
- ⚠️ Only the **`Participants`** field exists in this release — no Interventions or Outcomes.
- `src/` retains the upstream `pico` loader package.

## Image datasets — the human–AI allocation arm

Both are filtered to **instances that actually carry crowd labels**; everything else stays in
`../datasets/`. Converted by `../eval/convert/build_labelme.py` and `build_imagenet16h.py`,
which assert their joins on every run.

### labelme_crowd
Rodrigues & Pereira, *Deep Learning from Crowds*, AAAI-18 — the same source as
`movie_reviews_crowd`. 8-way scene classification (highway, insidecity, tallbuilding, street,
forest, coast, mountain, opencountry).

- **Train split only.** `answers.txt` is 1,000 × 77; the valid (500) and test (1,188) splits ship
  gold but NO per-annotator labels, so they are dropped.
- **18 of 77 worker columns are entirely empty.** Copied verbatim here, dropped at melt time —
  an annotator with zero observations breaks per-worker estimation in DawidSkene/GLAD/MACE.
  59 workers remain.
- ⚠️ **Annotation depth is 2.55/image, the thinnest in this project.** Vote counts are 42 tasks
  with 1 label, 369 with 2, 589 with 3.
- ⚠️ **Majority vote is NOT a stable baseline here.** 12.9% of tasks have a tied top vote, so MV
  swings ~±0.7 points on tie policy alone: three independent implementations gave 0.7620
  (crowd-kit), 0.7690 (`np.bincount.argmax`) and 0.7760 (`pandas.value_counts.idxmax`).
  Resolving every tie in gold's favour would give 0.8270. **Quote DawidSkene (0.7920), not MV.**
- Task ids are image stems (`street_hexp30`) so each maps to `train/<class>/<stem>.jpg`.
- Aggregator spread is 3.0 pts: DawidSkene 0.7920 → MajorityVote 0.7620.

### imagenet16h
Steyvers, Tejeda, Kerrigan & Smyth, *Bayesian modeling of human–AI complementarity*, PNAS 2022.
16-way object classification over phase-noise-degraded ImageNet photos.

- **The instance unit is (image × noise level), not image** — 1,200 × 4 = 4,800 tasks. Each noise
  variant is a different stimulus with a different difficulty; collapsing across noise would pool
  four difficulty regimes into one instance.
- **The 1,200 `original` (noiseless) images are dropped**: they carry gold but were never shown to
  participants, so they have no crowd labels.
- A **controlled difficulty gradient**, which no other corpus here has — majority-vote accuracy by
  phase-noise level: **0.9600 / 0.9317 / 0.8708 / 0.7325** at 80 / 95 / 110 / 125.
- Per-trial **confidence** (high/medium/low) and response times are in `behavioral/` but are NOT
  carried into the long form, which is strictly task/worker/label. Read them from there if the
  analysis needs *measured* human uncertainty rather than inferred disagreement.
- Gold is `image_category`, verified constant per image; the shipped `correct` flag is asserted
  to equal `participant_classification == image_category` on all 28,997 rows.
- ⚠️ **The aggregator choice barely matters**: all eight land within 0.5 pts (0.8715–0.8767) and
  plain Wawa nominally wins. With 6 judgments from a competent crowd there is little annotator
  unreliability left to model — the opposite of `quiz`, where MACE beats MV by 11.6 pts.
- ⚠️ **Cost warning.** MACE takes ~198s on the full table (GLAD ~59s). A naive routing sweep
  (19 budgets × 2 routes × 4 measures × 3 models, each a re-fit) would run to roughly 25 hours
  for MACE alone. Plan it; do not launch it blind.
- The source paper's CNN predictions and fine-tuned weights (several GB) stay in `../datasets/` —
  we substitute VLM annotators.

## Added on request, with caveats

### quiz_crowd_li
`garfieldpigljy/CrowdLabelwithTextContent` (CC BY 4.0). Six multiple-choice subsets, pooled by
`../eval/convert/build_quiz.py` into a single long table `eval/data/quiz_{crowd,gold}.csv`.

| Subset | Items | Workers | Judgments | Options | Language | MV acc | Mean worker acc |
|---|--:|--:|--:|--:|---|--:|--:|
| CHINESE (`chi`) | 24 | 50 | 1,200 | A–E | zh→ja | 62.5% | 37.4% |
| ENGLISH (`eng`) | 30 | 63 | 1,890 | A–E | en | 46.7% | 25.6% |
| ITMANAGE (`itm`) | 25 | 36 | 900 | A–D | ja | 76.0% | 53.7% |
| MEDICINE (`med`) | 36 | 45 | 1,620 | A–D | ja | 66.7% | 47.5% |
| POKEMON (`pok`) | 20 | 55 | 1,100 | A–F | en→ja | 65.0% | 27.7% |
| SCIENCE (`sci`) | 20 | 111 | 2,220 | A–E | ja | 55.0% | 29.5% |
| **pooled** | **155** | **360** | **8,930** | A–F | | | |

The answer matrix is **100% dense** — every worker answers every question in their subset. No
other corpus here is dense.

**Pooled, not split.** Per subset there are 20–36 items against 36–111 workers, which leaves
DawidSkene / MACE / GLAD badly under-determined (SCIENCE asks for 111 confusion matrices from 20
observations each). Only the pooled 155-item table is worth fitting.

**Worker ids are namespaced** (`chi_worker1`). The subsets came from separate pools of different
sizes, so `worker1` in CHINESE is not `worker1` in SCIENCE; pooling raw would fuse unrelated
annotators into one confusion matrix.

**The label space A–F is not a shared class space.** "C" means a different option in every
question, and option counts differ (4/5/6). Any aggregator estimating a global class prior or a
full K×K confusion matrix sees a prior with no cross-subset meaning. Read per-class F1 here as an
artefact, not a result; accuracy is the only metric that transfers.

**Upstream defect — ENGLISH ids.** `ENGLISH/quiz.csv` retains the original source ids
(1,2,3,4,6,7,8,11,…,59) while its `truth.csv` and `answer.csv` were renumbered 1–30. Joining by
`question_id` silently mismatches 25 of 30 rows (5 agree by coincidence). The join is therefore
**positional** in all six subsets; the other five have contiguous ids and join identically either
way. `build_quiz.py` re-asserts this on every run and aborts if it breaks.

**Not comparable in scale, and shakier on criterion 1.** 155 items against 18,128 elsewhere. Four
of the six subsets are knowledge exams rather than annotation tasks — ITMANAGE is the Japanese IT
Passport exam, MEDICINE a nursing exam, SCIENCE chemistry/physics, POKEMON English→Japanese name
lookup; only ENGLISH (SAT word analogy) and arguably CHINESE (vocabulary gloss) are language tasks.
Published exam banks are plausible pretraining data, so an LLM advantage here may be recall rather
than annotation skill. And the crowd sits near chance (ENGLISH 25.6% against a 20% floor), which is
quiz answer aggregation in the CIKM'17 hyper-questions sense rather than the annotation regime the
other five occupy.

**Do not run the routing sweep on it.** At 155 items each 5% budget step moves ~8 items, and peak
selection over 4 measures × ~6 methods × 19 budgets × 2 routes would be mostly noise. There is also
no timing data in the corpus, so `build_budget.py` has no measured anchor for human cost.

Source papers, to cite if this is used: Jiyi Li, *A Comparative Study on Annotation Quality of
Crowdsourcing and LLM via Label Aggregation*, ICASSP 2024, pp. 6525–6529; and Jiyi Li, Yukino Baba,
Hisashi Kashima, *Hyper Questions: Unsupervised Targeting of a Few Experts in Crowdsourcing*,
CIKM 2017, pp. 1069–1078. The ICASSP paper runs crowd-vs-LLM through label aggregation on exactly
these six subsets, making it our closest related work.

## Caveats carried forward

- Annotation depth is ~5–6 per instance for four of the five (CrowdTruth RelEx is the outlier at
  15.4). Thin for per-annotator parameter estimation.
- `movie_reviews_crowd` is regression, not classification — disagreement is variance, not a
  categorical distribution.
- `sentiment_polarity_ma_lr` ships pre-computed LSA topic features; raw sentences live in
  `mturk_answers.csv` (`Input.original_sentence`) if you want modern encoders.
- Worker identity in `movie_reviews_crowd/answers.txt` and `conll2003_ner_crowd/answers.txt` is
  positional (column index); real MTurk IDs for MovieReviews are in `Batch_results_AMT.csv`.

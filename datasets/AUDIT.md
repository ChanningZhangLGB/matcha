# Dataset eligibility audit

Criteria: **(1)** NLP task · **(2)** publicly available instances · **(3)** individual human annotator
labels per instance · **(4)** ground-truth labels for evaluation.

| Dataset | 1 NLP | 2 Public | 3 Individual labels | 4 Gold | Verdict |
|---|:--:|:--:|:--:|:--:|---|
| sentiment_polarity_ma_lr | ✅ | ✅ | ✅ 203 workers | ✅ all | **PASS** |
| movie_reviews_crowd | ✅ | ✅ | ✅ 135 workers | ✅ all | **PASS** |
| conll2003_ner_crowd | ✅ | ✅ | ✅ 47 workers | ✅ all | **PASS** |
| crowdtruth_medical_re | ✅ | ✅ | ✅ `_worker_id` in `raw/` | ⚠️ 24% / 16% expert | **PASS w/ caveat** |
| pico_data | ✅ | ✅ | ✅ 309 workers | ⚠️ 191 docs only | **PASS w/ caveat** |
| chaosnli | ✅ | ✅ | ❌ counts only, no annotator IDs | ✅ `old_label` | **FAILS (3)** |
| music_genre_crowd | ❌ audio | ✅ | ✅ | ✅ | **FAILS (1)** |

---

## Full pass

### sentiment_polarity_ma_lr — binary sentiment
- `mturk_answers.csv`: **27,746 judgments · 203 workers · 4,999 instances · 5.55 annots/instance**
  (labels: 14,828 pos / 12,918 neg). Worker IDs explicit (`WorkerId`).
- Gold: `Input.true_sent` on every row (Pang & Lee polarity gold). Held-out test: 5,428 instances
  (`polarity_test_lsa_topics.csv`).
- Note: features are pre-computed LSA topics; raw sentences are in `mturk_answers.csv`
  (`Input.original_sentence`) if you need to re-encode with a modern LM.

### movie_reviews_crowd — text regression (rating in [0,1])
- `answers.txt`: **1,498 docs × 135 worker columns · 7,430 judgments · 4.96 annots/doc**, `-1` = no annotation.
  Real worker IDs recoverable from `Batch_results_AMT.csv`.
- Gold: `ratings_train.txt` (1,498) and `ratings_test.txt` (3,508); raw text in `texts_*.txt`.
- Note: continuous target, so "annotator disagreement" is variance, not a categorical distribution.

### conll2003_ner_crowd — sequence labelling (BIO, 4 entity types)
- `answers.txt`: **79,901 tokens · 5,985 sentences · 47 annotator columns** (`?` = not annotated).
- Gold: `ground_truth.txt` (same 5,985 sentences) + `testset.txt` (3,466 sentences, 51,362 tokens).
  `mv.txt` = majority-vote baseline. `trainset.txt` = 6,654 expert-labelled sentences.
- Cleanest of the set for token-level disagreement modelling.

## Pass with caveats

### crowdtruth_medical_re — relation extraction (cause / treat)
- Per-worker judgments in `raw/{RelEx,RelDir,FactSpan}/*_batch_*.csv` with `_worker_id`, `_trust`,
  `sent_id` → joinable to the aggregate files. Aggregates: 3,984 sentences each.
- ⚠️ **Criterion 4 is partial**: `expert` column populated for only **975/3,984 (cause)** and
  **621/3,984 (treat)**; the rest are `NA`. A UMLS `baseline` label exists for all 3,984 but is
  distant supervision, not human gold. `test_partition` splits: cause 239/690/32, treat 291/315.
- → Restrict evaluation to the expert-labelled subset, or accept the UMLS baseline as weak gold.

### pico_data — span annotation on biomedical abstracts
- Per-worker character spans with MTurk IDs: train 3,549 docs / 309 workers / 21,267 worker-doc
  annotations; dev 500/197; test 500/208; acl17-test 191/91.
- ⚠️ **Criterion 4 is partial**: expert (`PICO-annos-professional.json`) exists **only for acl17-test
  (191 docs)**. Train/dev/test have no gold — only `-agg.json` (crowd aggregation, not ground truth).
- ⚠️ Also note: this release contains **only the `Participants` field** — no Interventions or Outcomes,
  despite the PICO name. Verified across every split.
- → Usable, but the evaluation set is 191 documents.

## Fails

### chaosnli — **fails criterion 3**
- Each item has 100 fresh annotations, but the release stores only `label_counter` / `label_count` /
  `label_dist` / `entropy`. **No annotator ID field exists** — verified across all three files.
  You can reconstruct the *multiset* of 100 labels, never who gave which.
- `old_labels` gives the 5 original unattributed annotator labels for SNLI/MNLI (1,514 + 1,599 items)
  but is **absent for alphaNLI** (0/1,532).
- Criterion 4 is fine: `old_label` = original dataset gold; `majority_label` also available.
- → If MATCHA needs per-annotator modelling (annotator embeddings, confusion matrices, worker
  reliability), ChaosNLI **cannot** support it. If it only needs a *label distribution* target, it's
  the strongest resource here (100 annotations/item vs. ~5 elsewhere).

### music_genre_crowd — **fails criterion 1**
- Not an NLP task: audio genre classification over Marsyas acoustic features (`marsyas_features.arff`,
  instances are `.mp3` files). Criteria 2–4 all hold (700 songs, per-worker labels, `Input.true_label`).
- → Came bundled in the 2013 archive; drop unless you want a non-NLP control condition.

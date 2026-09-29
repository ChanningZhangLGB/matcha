# Raw datasets (not redistributed)

Crowdsourced / multi-annotator datasets with **per-annotator labels** (not just aggregated gold).
Source archives kept in `../_archives/`.

| Folder | Dataset | Task | Source |
|---|---|---|---|
| `sentiment_polarity_ma_lr/` | Sentiment Polarity (MTurk) | binary sentiment | Rodrigues et al. 2013, MA-LR — `mturk-datasets.tar.gz` (fprodrigues.com) |
| `music_genre_crowd/` | Music Genre (MTurk) | multi-class | same 2013 archive (bonus, came bundled) |
| `movie_reviews_crowd/` | MovieReviews (MTurk) | text regression (ratings) | Rodrigues & Pereira, *Deep Learning from Crowds*, AAAI-18 |
| `conll2003_ner_crowd/` | CoNLL-2003 NER (MTurk) | sequence labelling | Rodrigues & Pereira, AAAI-18 |
| `crowdtruth_medical_re/` | CrowdTruth Medical Relation Extraction | relation extraction | github.com/CrowdTruth/Medical-Relation-Extraction |
| `chaosnli/` | ChaosNLI v1.0 | NLI label distributions (100 annots/item) | Nie et al. 2020, github.com/easonnie/ChaosNLI |
| `pico_data/` | PICO-data | span annotation (crowd + expert) | github.com/yinfeiy/PICO-data |

## Where the annotator-level labels live

- **sentiment_polarity_ma_lr** — `mturk_answers.csv` (27,746 rows: `WorkerId, Input.id, Input.original_sentence,
  Input.stemmed_sent, Input.true_sent, Answer.sent`). Features: `polarity_{mturk,gold,test}_lsa_topics.csv`.
- **music_genre_crowd** — `mturk_answers.csv`; gold in `music_genre_gold.csv`; features `marsyas_features.arff`.
- **movie_reviews_crowd** — `answers.txt`: one row per document, one column per worker, `-1` = not annotated,
  otherwise the worker's rating in [0,1]. Gold in `ratings_*.txt`, text in `texts_*.txt`, ids in `ids_*.txt`.
  Raw MTurk dump: `Batch_results_AMT.csv`. `scale_data/` = original Pang & Lee scale corpus.
- **conll2003_ner_crowd** — `answers.txt`: CoNLL format, col 1 = token, then one BIO column per worker
  (`?` = not annotated). `ground_truth.txt` = expert labels, `mv.txt` = majority vote,
  `trainset.txt` / `testset.txt` = splits.
- **crowdtruth_medical_re** — `ground_truth_cause.csv` / `ground_truth_treat.csv` (3,984 sentences with
  crowd score vectors); `raw/` has the per-worker judgments for the RelEx / RelDir / FactSpan tasks;
  `train_dev_test/` has the splits.
- **chaosnli** — `chaosNLI_v1.0/chaosNLI_{snli,mnli_m,alphanli}.jsonl`; each line has `label_counter`,
  `label_dist`, `entropy`, `majority_label`, `old_label` over 100 fresh annotations.
- **pico_data** — `annotations/{train,dev,test,acl17-test}/PICO-annos-crowdsourcing.json` (per-worker spans),
  `-agg.json` (aggregated), and `PICO-annos-professional.json` (expert, acl17-test only). Abstracts in `docs/`.

## Provenance notes

- `fprodrigues.com` is behind Cloudflare and blocks scripted downloads; the 2018 tarballs
  (`deep_MovieReviews`, `deep_ner-mturk`) were supplied manually. `mturk-datasets.tar.gz` came from the
  Wayback Machine snapshot.
- ChaosNLI data pulled from the official Dropbox link in `scripts/download_data.sh`; the repo's
  `model_predictions.zip` was **not** downloaded (add it if model-prediction baselines are needed).
- Repo clones (`crowdtruth_medical_re`, `pico_data`) had `.git` stripped; macOS `._*` / `.DS_Store` removed.

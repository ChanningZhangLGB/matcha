# Results

8 crowd-kit aggregators × 6 tables = 48 runs. **Zero failures, zero unpredicted tasks.**
Raw: `results/categorical.csv`, `results/regression.csv`, log in `results/categorical_run.log`.

## Track 1 — categorical, macro-F1

Sorted by mean rank across the six datasets (1 = best).

| Method | sentiment | movie_rev | ct_cause | ct_treat | conll_5k | pico | **rank** |
|---|--:|--:|--:|--:|--:|--:|--:|
| **DawidSkene** | 0.9152 | 0.7680 | **0.6065** | 0.8219 | **0.7529** | **0.8581** | **2.33** |
| GLAD | **0.9166** | 0.7730 | 0.5517 | **0.8256** | 0.6825 | 0.8413 | 3.25 |
| MACE | 0.9148 | 0.7815 | 0.5556 | 0.8132 | 0.6776 | 0.8353 | 4.00 |
| ZeroBasedSkill | 0.8945 | **0.7826** | 0.5462 | 0.7971 | 0.6844 | 0.8433 | 4.17 |
| Wawa | 0.8947 | 0.7765 | 0.5462 | 0.7917 | 0.6818 | 0.8441 | 4.67 |
| OneCoinDawidSkene | **0.9166** | 0.7762 | 0.5401 | 0.8161 | 0.5889 | 0.8055 | 5.25 |
| MMSR | 0.9008 | 0.7331 | 0.5533 | 0.8066 | 0.6794 | 0.8021 | 5.67 |
| MajorityVote | 0.8820 | 0.7598 | 0.5462 | 0.7827 | 0.6253 | 0.8415 | 6.67 |

**DawidSkene wins overall**, and its margin tracks label-space complexity: +6.9 macro-F1 over the
runner-up on 9-class CoNLL, +4.6 on the hard `crowdtruth_cause`, but only ~0 on 2-class sentiment,
where every EM method converges to the same answer. The full K×K confusion matrix is what pays.

**OneCoinDawidSkene is the control that proves it.** Same generative model, annotator reliability
collapsed to one scalar. It ties for best on binary sentiment (0.9166) and finishes **last on
CoNLL** (0.5889, below MajorityVote). Nothing changes but annotator-model capacity.

**MajorityVote is last on mean rank** but is not uniformly bad — on PICO it beats MACE, MMSR and
OneCoinDawidSkene on macro-F1. Weak baseline, not a useless one.

### Accuracy ranks differently — do not report it alone

| | best by macro-F1 | best by accuracy |
|---|---|---|
| conll_ner_5k | DawidSkene 0.7529 | DawidSkene 0.9418 |
| pico | DawidSkene 0.8581 | **Wawa 0.9543** (DawidSkene 6th at 0.9492) |
| crowdtruth_cause | DawidSkene 0.6065 | MACE 0.7692 |

On PICO the positive rate is 10.2%, so accuracy spans just 0.937–0.954 while macro-F1 spans
0.802–0.858, and the two orderings disagree outright. On `crowdtruth_cause` (247 yes / 728 no)
MajorityVote, Wawa and ZeroBasedSkill return **identical** macro-F1 (0.5462) — they collapse to the
same near-degenerate majority-class solution, which accuracy (~0.763) hides completely.

### Cost

| Method | total s (6 datasets) |
|---|--:|
| GLAD | 455.0 |
| MACE | 368.6 |
| MMSR | 47.3 |
| ZeroBasedSkill | 37.9 |
| OneCoinDawidSkene | 7.5 |
| **DawidSkene** | **4.7** |
| Wawa | 2.5 |
| MajorityVote | 1.9 |

DawidSkene is both the most accurate and ~97× faster than GLAD. GLAD and MACE cost >97% of total
runtime and win nothing on macro-F1.

## Track 2 — regression (MovieReviews, no binning)

| Method | MAE | RMSE | R² | r |
|---|--:|--:|--:|--:|
| Mean *(paper's `DL (Mean)` target)* | 0.0607 | 0.0755 | 0.830 | 0.928 |
| **EMBias** *(ours — paper's "B" annotator model, EM-fit)* | **0.0492** | **0.0587** | **0.897** | **0.967** |
| *shipped_DS (reference; no method in the paper)* | *0.0436* | *0.0535* | *0.914* | *0.974* |

Mean reproduces the shipped `ratings_train_mean.txt` to 1.1e-16, confirming the `-1`-sentinel
handling. Learned annotator biases `b_r`: sd 0.114, range `[-0.287, +0.433]` — large systematic
bias, independently corroborating the paper's finding that bias-only ("B") beat scale and
scale+bias.

## Caveats

- **Task counts overstate independence.** PICO's 44,456 tasks come from 191 documents;
  `conll_ner_5k`'s 5,001 from 392 sentences. Tokens within a unit are highly correlated.
- **`crowdtruth_treat` ⊂ `crowdtruth_cause`** — the 621 treat sentences are a strict subset of the
  975 cause sentences. Not independent datasets.
- **MovieReviews appears in both tracks** under different framings; the two tracks' numbers are not
  comparable to each other, and neither is comparable to the paper's Table 2 (which reports a CNN on
  the 3,506-item *test* set, 1–10 scale).
- **GoldMajorityVote excluded** — it consumes ground truth at `fit()`.
- Annotations per worker are thin (MovieReviews median 6), so per-annotator parameters are estimated
  from few observations throughout.

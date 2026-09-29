# RQ3, stage 1: does prompt variation make uncertainty usable?

Artefacts for the prompting ablation. Working detail (per-dataset bins, slopes,
discrimination summaries) stays in `results/calibration_analysis/`; this folder holds
what the paper reports.

## The ladder

Four prompting sources, differing only in how much variation the uncertainty is
measured across. All are scored on the same instances with the same gold labels.

| source | conditions | k |
|---|---|---|
| k0 | basic instruction x vanilla | 1 |
| k1 | basic instruction x {vanilla, cot, topk} | 3 |
| k2 | {basic, control, customized} x vanilla | 3 |
| k3 | 3 prompt groups x 3 protocols | 9 |

k1 and k2 are EQUAL-k by construction, so the contrast between them isolates which axis
of variation matters rather than how many conditions were averaged. Entropy and
inter-rater are undefined at k0: one vote has no spread.

Sentiment Polarity's True/False manipulation queries each sentence twice, counterbalanced
over the asserted polarity. Those two responses are merged into one condition
probabilistically (see `merge_variants` in `build_calibration.py`) so that sentiment
realises k = 1/3/3/9 like every other dataset. Without the merge it reports 1/3/4/12 and
the equal-k property is lost.

## Metrics

- **conf-ECE**, `sum_b (n_b/N)|acc_b - conf_b|` over 15 equal-width confidence bins,
  the definition and bin count of Guo et al. Computed three times, once per uncertainty
  measure, with `conf = 1 - u_norm`.
- **AUROC**, tie-aware, for using low uncertainty to predict a correct label.

## Files

- `ladder_table.{csv,tex}` mean of each metric over the 24 (dataset, model) cells, with
  every source marked for significance against k=9. A blank cell means the test did not
  reach p<0.05, not that no test was run.
- `ladder_table_by_model.{csv,tex}` the same quantities per annotator model. NO
  significance markers: n falls to 8, 6, 6, 2, 2 datasets, and Holm across the 38
  attainable tests suppresses every one, since the smallest two-sided p at n=6 is 0.031.
  Read it for direction and magnitude; take significance from `ladder_table` where n=24.
- `significance.csv` full test table, including the k1-vs-k2 contrast omitted from the
  paper table.
- `figures/<measure>/<dataset>_<model>.{pdf,png}` reliability diagrams across the ladder,
  with the calibration gap hatched by direction.

Tests are two-sided Wilcoxon signed-rank paired on the 24 cells, Holm-corrected within
each table. THE CELLS ARE NOT INDEPENDENT: each dataset appears once per model and each
model once per dataset in its arm, so the p-values speak to the consistency of the
direction across this grid, not to a population of corpora.

## Regenerate

    python results/utils/build_calibration.py <dataset>          # per-dataset summaries
    python results/utils/build_calibration_reliability.py        # figures
    python results/utils/build_calibration_significance.py       # -> significance.csv
    python results/utils/build_calibration_table.py              # -> ladder_table.*

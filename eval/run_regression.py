#!/usr/bin/env python3
"""Track 2 — regression aggregation, MovieReviews only.

Two aggregators, both operating directly on the continuous ratings (no binning):

  Mean       the per-item average of the annotators' ratings. This is the ONLY
             aggregation Rodrigues & Pereira (AAAI-18) used for MovieReviews --
             their Table 2 row "DL (Mean)". Reproduced here exactly; identical to
             the shipped `ratings_train_mean.txt`.

  EMBias     OUR reconstruction, not theirs. It adopts the annotator model of the
             paper's best crowd-layer variant "B", f_r(mu) = mu + b_r, i.e. each
             annotator has an additive bias, and fits it by EM on the answer
             matrix alone. The paper instead trained that model end-to-end inside
             a CNN, so this shares their theory but not their procedure. Do not
             report it as a replication.

`ratings_train_DS.txt` ships with the dataset but corresponds to no method in the
paper (there is no Dawid & Skene row in Table 2 -- DS appears only for the
classification datasets). It is scored here purely as a reference column.

    python eval/run_regression.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.metrics import regression_metrics           # noqa: E402
from common.paths import DATA, MR_MISSING, RESULTS      # noqa: E402

D = DATA / "movie_reviews_crowd"
VAR_FLOOR = 1e-4


def load():
    Y = np.array([[float(x) for x in l.split()] for l in open(D / "answers.txt")])
    M = Y != MR_MISSING          # -0.1 and 1.1 are VALID ratings; only -1 is missing
    gold = np.loadtxt(D / "ratings_train.txt")
    return Y, M, gold


def agg_mean(Y, M):
    return np.where(M, Y, 0.0).sum(1) / M.sum(1)


def agg_em_bias(Y, M, n_iter=500, tol=1e-12):
    """EM for y_ir = z_i + b_r + eps_r,  eps_r ~ N(0, var_r).

    E-step: z_i is the precision-weighted mean of the bias-corrected answers.
    M-step: b_r is the mean residual of annotator r (centred for identifiability),
            var_r is the mean squared residual.
    """
    Yz = np.where(M, Y, 0.0)
    z = agg_mean(Y, M)
    n_per_worker = np.maximum(M.sum(0), 1)
    for _ in range(n_iter):
        b = np.where(M, Yz - z[:, None], 0.0).sum(0) / n_per_worker
        b -= b.mean()                                    # identifiability
        resid = np.where(M, Yz - z[:, None] - b, 0.0)
        var = np.maximum((resid ** 2).sum(0) / n_per_worker, VAR_FLOOR)
        w = M / var
        z_new = (w * (Yz - b)).sum(1) / w.sum(1)
        if np.max(np.abs(z_new - z)) < tol:
            z = z_new
            break
        z = z_new
    return z, b


if __name__ == "__main__":
    RESULTS.mkdir(parents=True, exist_ok=True)
    Y, M, gold = load()
    print(f"MovieReviews: {Y.shape[0]:,} items, {Y.shape[1]} annotators, "
          f"{int(M.sum()):,} ratings")
    print(f"  ratings range [{Y[M].min()}, {Y[M].max()}]  "
          f"(-1 = missing; -0.1 and 1.1 are valid)")
    print(f"  annotations/annotator: min={M.sum(0).min()} "
          f"median={int(np.median(M.sum(0)))} max={M.sum(0).max()}\n")

    mean = agg_mean(Y, M)
    em, bias = agg_em_bias(Y, M)
    shipped_mean = np.loadtxt(D / "ratings_train_mean.txt")
    shipped_ds = np.loadtxt(D / "ratings_train_DS.txt")

    print(f"Mean matches shipped ratings_train_mean.txt: "
          f"{np.allclose(mean, shipped_mean)} "
          f"(max|diff|={np.abs(mean - shipped_mean).max():.2e})")
    print(f"Learned annotator bias b_r: mean={bias.mean():+.4f} "
          f"sd={bias.std():.4f} range [{bias.min():+.3f}, {bias.max():+.3f}]\n")

    rows = []
    for name, est, note in [
        ("Mean", mean, "paper's DL (Mean) target"),
        ("EMBias", em, "ours; paper's 'B' annotator model, fit by EM"),
        ("shipped_DS", shipped_ds, "reference only; not a method in the paper"),
    ]:
        m = regression_metrics(gold, est)
        m.update(method=name, note=note)
        rows.append(m)
        print(f"  {name:11s} MAE={m['MAE']:.4f}  RMSE={m['RMSE']:.4f}  "
              f"R2={m['R2']:.4f}  r={m['pearson_r']:.4f}   ({note})")

    df = pd.DataFrame(rows)[["method", "MAE", "RMSE", "R2", "pearson_r", "note"]]
    out = RESULTS / "regression.csv"
    df.to_csv(out, index=False)
    np.savetxt(RESULTS / "movie_reviews_embias.txt", em, fmt="%.6f")
    print(f"\nwrote {out}")

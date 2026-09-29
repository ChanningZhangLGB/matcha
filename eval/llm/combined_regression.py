#!/usr/bin/env python3
"""Human + LLM regression on MovieReviews: the LLM as one extra rater.

    python eval/llm/combined_regression.py gpt-4o-mini

The continuous analogue of results/build_combined_aggregation.py. The LLM's rating --
the MEAN over its continuous conditions (basic + control; `customized` is a lettered
choice and is excluded) -- is appended to the human answer matrix as one additional
annotator column, then the aggregators re-run on the combined pool.

Aggregators re-run:
  Mean     per-item average over all raters
  EMBias   the paper's "B" annotator model (y = z + b_r), fit by EM

`shipped_DS` is not re-runnable -- it is a precomputed artefact from unpublished code,
so it stays a human-only reference row.

As in the categorical case the LLM contributes ONE vote, not one per condition: the
conditions are the same model under different prompts and their errors are correlated,
so treating them as independent raters would overweight the LLM ~6x.

Writes results/movie_reviews/regression/combined_regression_<model>.{md,csv}
"""
import collections
import csv
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
sys.path.insert(0, str(ROOT / "eval" / "llm"))
from common.metrics import regression_metrics                       # noqa: E402
from common.paths import MR_MISSING                                 # noqa: E402
import score_llm as S                                               # noqa: E402
from regression_llm import CONTINUOUS, GROUPS, PROTOS, stars        # noqa: E402

DATA = ROOT / "datasets_pass" / "movie_reviews_crowd"
RES = ROOT / "results" / "movie_reviews" / "regression"
VAR_FLOOR = 1e-4


def agg_mean(Y, M):
    return np.where(M, Y, 0.0).sum(1) / np.maximum(M.sum(1), 1)


def agg_em_bias(Y, M, n_iter=500, tol=1e-12):
    """EM for y_ir = z_i + b_r + eps_r (the paper's 'B' annotator model)."""
    Yz = np.where(M, Y, 0.0)
    z = agg_mean(Y, M)
    npw = np.maximum(M.sum(0), 1)
    for _ in range(n_iter):
        b = np.where(M, Yz - z[:, None], 0.0).sum(0) / npw
        b -= b.mean()
        resid = np.where(M, Yz - z[:, None] - b, 0.0)
        var = np.maximum((resid ** 2).sum(0) / npw, VAR_FLOOR)
        w = M / var
        z_new = (w * (Yz - b)).sum(1) / w.sum(1)
        if np.max(np.abs(z_new - z)) < tol:
            return z_new, b
        z = z_new
    return z, b


def llm_rating(model):
    """Mean over the continuous conditions -> {task: rating in [0,1]}."""
    acc = collections.defaultdict(list)
    for group, short in GROUPS.items():
        if short not in CONTINUOUS:
            continue
        for proto in PROTOS:
            recs = S.read(model, group, "movie_reviews", proto)
            if not recs:
                continue
            for r in recs:
                v = stars(r, proto, short)
                if v is not None:
                    acc[r["id"]].append(v)
    return {t: float(np.mean(v)) for t, v in acc.items()}, len(CONTINUOUS) * len(PROTOS)


def main(model):
    Y = np.array([[float(x) for x in l.split()] for l in open(DATA / "answers.txt")])
    M = Y != MR_MISSING
    gold = np.loadtxt(DATA / "ratings_train.txt")
    lab, k = llm_rating(model)
    if not lab:
        print("  no continuous LLM output for", model)
        return

    col = np.full((Y.shape[0], 1), MR_MISSING)
    n_llm = 0
    for i in range(Y.shape[0]):
        v = lab.get(f"mr{i}")
        if v is not None:
            col[i, 0] = v
            n_llm += 1
    Yc = np.hstack([Y, col])
    Mc = Yc != MR_MISSING

    print(f"MovieReviews regression: {Y.shape[1]} human raters + 1 LLM "
          f"(mean of {k} continuous conditions)")
    print(f"  LLM rates {n_llm:,}/{Y.shape[0]:,} items; "
          f"ratings/item {M.sum(1).mean():.2f} -> {Mc.sum(1).mean():.2f}")

    rows = []
    for name, fn in [("Mean", agg_mean), ("EMBias", lambda a, b: agg_em_bias(a, b)[0])]:
        for tag, (yy, mm) in [("human-only", (Y, M)), ("human+LLM", (Yc, Mc))]:
            est = fn(yy, mm)
            m = regression_metrics(gold, est)
            m.update(method=name, pool=tag)
            rows.append(m)
            print(f"    {name:8s} {tag:10s} MAE={m['MAE']:.4f} RMSE={m['RMSE']:.4f} "
                  f"R2={m['R2']:.4f} r={m['pearson_r']:.4f}")

    out = RES / "model_analysis" / model; out.mkdir(parents=True, exist_ok=True)
    with open(out / "combined_regression.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["method", "pool", "MAE", "RMSE", "R2", "pearson_r"])
        for r in rows:
            w.writerow([r["method"], r["pool"]] + [f"{r[c]:.4f}" for c in
                                                   ["MAE", "RMSE", "R2", "pearson_r"]])

    by = {(r["method"], r["pool"]): r for r in rows}
    L = [f"# movie_reviews (regression) - Human + {model}", "",
         f"The LLM joins the {Y.shape[1]} human raters as **one additional annotator**, "
         f"its rating being the mean over {k} continuous conditions "
         f"(`basic` + `control`).  ",
         f"Ratings per item rise from {M.sum(1).mean():.2f} to {Mc.sum(1).mean():.2f}.", "",
         "| Method | pool | MAE | RMSE | R2 | r |", "|---|---|--:|--:|--:|--:|"]
    for name in ("Mean", "EMBias"):
        for tag in ("human-only", "human+LLM"):
            r = by[(name, tag)]
            bold = "**" if tag == "human+LLM" else ""
            L.append(f"| {name} | {tag} | {bold}{r['MAE']:.4f}{bold} | {r['RMSE']:.4f} | "
                     f"{r['R2']:.4f} | {r['pearson_r']:.4f} |")
    L += ["", "| Method | delta MAE | delta R2 |", "|---|--:|--:|"]
    for name in ("Mean", "EMBias"):
        a, b = by[(name, "human-only")], by[(name, "human+LLM")]
        L.append(f"| {name} | {b['MAE']-a['MAE']:+.4f} | {b['R2']-a['R2']:+.4f} |")
    L += ["", "Lower MAE is better, higher R2 is better, so a NEGATIVE delta MAE means "
              "the LLM helped.",
          "`shipped_DS` is a precomputed artefact and cannot be re-run on a combined "
          "pool, so it stays a human-only reference."]
    (out / "combined_regression.md").write_text("\n".join(L) + "\n")
    print(f"\n  results/movie_reviews/regression/combined_regression_{model}.{{md,csv}}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

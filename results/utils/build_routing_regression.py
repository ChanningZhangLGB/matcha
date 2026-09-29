#!/usr/bin/env python3
"""Uncertainty-routed annotation for the REGRESSION track (movie_reviews).

    python results/utils/build_routing_regression.py [model] [--random]

The continuous counterpart of build_routing.py. For each measure and each budget X:

  HIGH  top X% by uncertainty rank -> the human answer matrix is RESTRICTED to those
        reviews and Mean / EMBias are RE-FITTED on the subset. Re-fitting matters:
        EMBias estimates a per-annotator bias term, so slicing a full-data fit would
        carry bias estimates learned from reviews no longer in the pool.
  LOW   the rest -> takes the LLM's rating (mean over its 6 continuous conditions).

  human_only      the high batch is aggregated from human ratings alone
  human_plus_llm  the LLM's rating joins that subset as one extra annotator column

Scored with MAE / RMSE / R2 / r against ratings_train.txt, so the numbers sit on the
same scale as regression/summary_table.csv.

Writes results/movie_reviews/regression/allocation/<model>/<measure>/<route>/routing.csv
   and .../splits.csv alongside.
"""
import argparse
import csv
import pathlib
import random
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
sys.path.insert(0, str(ROOT / "eval" / "llm"))
from common.metrics import regression_metrics                      # noqa: E402
from common.paths import MR_MISSING                                # noqa: E402
from combined_regression import agg_em_bias, agg_mean              # noqa: E402

DATA = ROOT / "datasets_pass" / "movie_reviews_crowd"
RES = ROOT / "results" / "movie_reviews" / "regression"
XS = list(range(5, 100, 5))
MEASURES = [("u_confidence", "confidence"), ("u_spread", "spread"),
            ("u_disagreement", "disagreement")]
ROUTES = ["human_only", "human_plus_llm"]


def run(model, with_random):
    src = RES / "model_analysis" / model / "uncertainty_per_instance.csv"
    if not src.exists():
        print(f"  {model}: no regression uncertainty, run uncertainty_regression.py first")
        return
    rows = list(csv.DictReader(open(src)))
    llm = {r["task"]: float(r["llm_rating"]) for r in rows}

    Y = np.array([[float(x) for x in l.split()] for l in open(DATA / "answers.txt")])
    M = Y != MR_MISSING
    gold = np.loadtxt(DATA / "ratings_train.txt")
    idx = {f"mr{i}": i for i in range(len(gold))}

    rankings = []
    for col, name in MEASURES:
        vals = [(r["task"], float(r[col])) for r in rows if r[col] not in ("", None)]
        vals.sort(key=lambda tv: (-tv[1], tv[0]))          # most uncertain first
        rankings.append((name, [t for t, _ in vals], dict(vals)))
    if with_random:
        order = sorted(llm)
        random.Random(42).shuffle(order)
        rankings.append(("random", order, {}))

    for name, order, uval in rankings:
        n = len(order)
        out_m = RES / "allocation" / model / name
        out_m.mkdir(parents=True, exist_ok=True)
        if uval:
            with open(out_m / "splits.csv", "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["task", "u", "rank", "pct_rank"] + [f"x{x:02d}" for x in XS])
                for i, t in enumerate(order):
                    cuts = {x: max(1, min(n - 1, round(n * x / 100))) for x in XS}
                    w.writerow([t, f"{uval[t]:.6f}", i + 1, f"{100*(i+1)/n:.4f}"]
                               + ["high" if i < cuts[x] else "low" for x in XS])

        for route in ROUTES:
            res = []
            for x in XS:
                k = max(1, min(n - 1, round(n * x / 100)))
                high = [t for t in order[:k] if t in idx]
                hi = np.array([idx[t] for t in high])
                sub_Y, sub_M = Y[hi], M[hi]
                if route == "human_plus_llm":
                    col = np.array([[llm.get(t, MR_MISSING)] for t in high])
                    sub_Y = np.hstack([sub_Y, col])
                    sub_M = sub_Y != MR_MISSING
                for meth, fn in [("Mean", agg_mean),
                                 ("EMBias", lambda a, b: agg_em_bias(a, b)[0])]:
                    est_hi = fn(sub_Y, sub_M)
                    full = np.array([llm.get(f"mr{i}", gold.mean())
                                     for i in range(len(gold))])
                    full[hi] = est_hi                     # humans override the high batch
                    m = regression_metrics(gold, full)
                    res.append({"X": x, "route": route, "method": meth,
                                "n_human": len(high), "n_llm": n - len(high),
                                **{k2: round(v, 6) for k2, v in m.items()}})
            out = out_m / route
            out.mkdir(parents=True, exist_ok=True)
            with open(out / "routing.csv", "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(res[0]))
                w.writeheader()
                w.writerows(res)
            best = min(res, key=lambda r: r["MAE"])
            print(f"  {name:12s} {route:15s} best MAE={best['MAE']:.4f} "
                  f"@ X={best['X']}% {best['method']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", default="gpt-4o-mini")
    ap.add_argument("--random", action="store_true")
    a = ap.parse_args()
    print(f"=== {a.model}")
    run(a.model, a.random)

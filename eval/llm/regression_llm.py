#!/usr/bin/env python3
"""MovieReviews as REGRESSION for an LLM, on the same scale as the human baseline.

    python eval/llm/regression_llm.py gpt-4o-mini

The model was asked for a star rating, not a bin -- the categorical track threw that
number away by applying bin_rating(). Here the raw stars are kept, rescaled /10 to
[0,1], and scored against `ratings_train.txt` with MAE / RMSE / R2 / Pearson r, so
the numbers sit directly beside results/movie_reviews/regression_aggregation.csv
(the human Mean / EMBias / shipped_DS row set).

Aggregate across conditions is the MEAN of the per-condition ratings -- the
continuous analogue of majority vote, and the same estimator the paper used on the
human side ("DL (Mean)").

`customized` is reported but EXCLUDED from the headline aggregate: it is a choice
among 11 lettered options rather than a free numeric estimate, and it is known to be
mis-anchored, so averaging it in would corrupt a continuous estimate.

Writes results/movie_reviews/<model>_regression.{md,csv}
"""
import collections
import csv
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
sys.path.insert(0, str(ROOT / "eval" / "llm"))
from common.metrics import regression_metrics                      # noqa: E402
import score_llm as S                                              # noqa: E402

DATA = ROOT / "datasets_pass" / "movie_reviews_crowd"
RES = ROOT / "results" / "movie_reviews" / "regression"
PROTOS = ["vanilla", "cot", "topk"]
GROUPS = {"basic_instruction": "basic", "control": "control", "customized": "customized"}
CONTINUOUS = {"basic", "control"}          # groups that gave a free numeric answer


def stars(rec, proto, group):
    """-> rating in [0,1], or None."""
    a = S.top_answer(rec.get("parsed"), proto)
    if group == "customized":                       # reversed letters, A = 10 stars
        if not isinstance(a, str) or not a.strip():
            return None
        L = a.strip().upper()[0]
        if not ("A" <= L <= "K"):
            return None
        v = 10 - (ord(L) - 65)
    else:
        try:
            v = float(a)
        except (TypeError, ValueError):
            return None
    return v / 10.0 if 0 <= v <= 10 else None


def main(model):
    gold = np.loadtxt(DATA / "ratings_train.txt")
    ids = [f"mr{i}" for i in range(len(gold))]
    gmap = dict(zip(ids, gold))

    conds = {}
    for group, short in GROUPS.items():
        for proto in PROTOS:
            recs = S.read(model, group, "movie_reviews", proto)
            if not recs:
                continue
            d = {}
            for r in recs:
                v = stars(r, proto, short)
                if v is not None:
                    d[r["id"]] = v
            if d:
                conds[f"{short}/{proto}"] = d
    if not conds:
        print("  no movie_reviews output for", model)
        return

    rows = []
    for name, d in sorted(conds.items()):
        k = [i for i in ids if i in d]
        m = regression_metrics([gmap[i] for i in k], [d[i] for i in k])
        m.update(condition=name, coverage=len(k) / len(ids), n=len(k))
        rows.append(m)

    # headline aggregate: mean over the continuous conditions only
    use = {n: d for n, d in conds.items() if n.split("/")[0] in CONTINUOUS}
    acc = collections.defaultdict(list)
    for d in use.values():
        for t, v in d.items():
            acc[t].append(v)
    k = [i for i in ids if i in acc]
    agg = regression_metrics([gmap[i] for i in k], [np.mean(acc[i]) for i in k])
    agg.update(condition=f"MEAN_of_{len(use)}_continuous_conditions",
               coverage=len(k) / len(ids), n=len(k))

    # same, but including customized, for contrast
    acc_all = collections.defaultdict(list)
    for d in conds.values():
        for t, v in d.items():
            acc_all[t].append(v)
    ka = [i for i in ids if i in acc_all]
    agg_all = regression_metrics([gmap[i] for i in ka],
                                 [np.mean(acc_all[i]) for i in ka])
    agg_all.update(condition=f"MEAN_of_all_{len(conds)}_conditions",
                   coverage=len(ka) / len(ids), n=len(ka))

    order = [agg, agg_all] + rows
    cols = ["condition", "MAE", "RMSE", "R2", "pearson_r", "coverage", "n"]
    out = RES / "model_analysis" / model; out.mkdir(parents=True, exist_ok=True)
    with open(out / "regression.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for m in order:
            w.writerow([m["condition"]] + [f"{m[c]:.4f}" for c in
                                           ["MAE", "RMSE", "R2", "pearson_r", "coverage"]]
                       + [m["n"]])

    human = []
    hf = RES / "regression_aggregation.csv"
    if hf.exists():
        human = list(csv.DictReader(open(hf)))

    L = [f"# movie_reviews - {model} as a regressor", "",
         "The model was asked for a star rating (0-10); the raw number is kept and "
         "rescaled to [0,1],",
         "so these sit on the same scale as the human aggregation below.", "",
         "## LLM", "",
         "| condition | MAE | RMSE | R2 | r | coverage |", "|---|--:|--:|--:|--:|--:|"]
    for m in order:
        bold = "**" if m["condition"].startswith("MEAN_of") else ""
        L.append(f"| {bold}{m['condition']}{bold} | {m['MAE']:.4f} | {m['RMSE']:.4f} | "
                 f"{m['R2']:.4f} | {m['pearson_r']:.4f} | {100*m['coverage']:.1f}% |")
    if human:
        L += ["", "## Human crowd (same scale)", "",
              "| method | MAE | RMSE | R2 | r |", "|---|--:|--:|--:|--:|"]
        for r in human:
            L.append(f"| {r['method']} | {float(r['MAE']):.4f} | {float(r['RMSE']):.4f} | "
                     f"{float(r['R2']):.4f} | {float(r['pearson_r']):.4f} |")
    L += ["", "`customized` answers by picking one of 11 lettered options rather than "
              "giving a free number,",
          "so it is listed but kept out of the headline aggregate; the row including it "
          "is shown for contrast."]
    (out / "regression.md").write_text("\n".join(L) + "\n")

    print(f"  results/movie_reviews/{model}_regression.{{md,csv}}")
    for m in (agg, agg_all):
        print(f"    {m['condition']:38s} MAE={m['MAE']:.4f} RMSE={m['RMSE']:.4f} "
              f"R2={m['R2']:.4f} r={m['pearson_r']:.4f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

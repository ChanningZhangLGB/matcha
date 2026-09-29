#!/usr/bin/env python3
"""Best routed allocation vs the fixed baselines -- REGRESSION track (movie_reviews).

    python results/utils/build_allocation_best_regression.py [model]

The continuous counterpart of build_allocation_best.py. MAE is the headline (lower is
better), with RMSE / R2 / r carried alongside.

    llm_only        mean over the model's 6 continuous conditions
    human_only      best of Mean / EMBias on the human ratings alone
    human_plus_llm  best of the two with the LLM added as one extra rater
    peak_*          the single best cell over the routing sweep, and the condition
                    that produced it (budget, method, uncertainty, route)

`shipped_DS` is excluded throughout: it is a precomputed artefact, so it cannot be
re-fitted on a routed subset or a combined pool.

Cost columns use the same model as the categorical side -- the LLM must rate ALL
instances to rank them, so its cost lands whatever X is:
    judgments_at_peak = distinct (task, worker) pairs among the routed instances

Writes results/movie_reviews/regression/allocation/<model>/best_allocation.csv
   and upserts the model's row into results/allocation_best_regression.csv
   (one combined table, one row per model)
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
REG = RES / "movie_reviews" / "regression"
MEASURES = ["confidence", "spread", "disagreement", "random"]
ROUTES = ["human_only", "human_plus_llm"]
AGG = ["Mean", "EMBias"]
HEADER = ["model", "dataset", "metric", "llm_only", "human_only", "human_only_method",
          "human_plus_llm", "human_plus_llm_method",
          "peak_routed", "peak_budget_X", "peak_method", "peak_uncertainty",
          "peak_route",
          # Human effort in JUDGMENTS, not money -- see build_budget.py for why the
          # dollar model was dropped (non-uniform annotator expertise, assumed timings).
          "human_judgments_full", "judgments_at_peak", "judgments_saved",
          "judgments_saved_pct", "mae_vs_human_only"]


def main(model):
    st = list(csv.DictReader(open(REG / "summary_table.csv")))
    hp = list(csv.DictReader(open(REG / "summary_table_human_plus_llm.csv")))
    mae = next(r for r in st if r["metric"] == "MAE")

    llm_only = mae.get(f"llm-only: {model}", "")
    h = {a: float(mae[f"human-only: {a}"]) for a in AGG if f"human-only: {a}" in mae}
    h_m = min(h, key=h.get)
    hp_row = next((r for r in hp if r["annotator_pool"] == f"{model} + human"
                   and r["metric"] == "MAE"), None)
    hpv = {a: float(hp_row[a]) for a in AGG if hp_row and hp_row.get(a)}
    hp_m = min(hpv, key=hpv.get) if hpv else ""

    peak = None
    for meas in MEASURES:
        for rt in ROUTES:
            f = REG / "allocation" / model / meas / rt / "routing.csv"
            if not f.exists():
                continue
            for r in csv.DictReader(open(f)):
                v = float(r["MAE"])
                if peak is None or v < peak[0]:
                    peak = (v, r["X"], r["method"], meas, rt)
    if peak is None:
        print(f"  {model}: no regression routing yet")
        return
    pv, px, pm, pmeas, prt = peak

    # Exact routed-judgment count from the splits file that produced the ranking.
    sp = REG / "allocation" / model / pmeas / "splits.csv"
    cf = ROOT / "eval" / "data" / "movie_reviews_crowd.csv"
    eff = [""] * 4
    if sp.exists() and cf.exists():
        col = f"x{int(px):02d}"
        srows = list(csv.DictReader(open(sp)))
        if col in srows[0]:
            high = {r["task"] for r in srows if r[col] == "high"}
            full, routed = set(), set()
            for r in csv.DictReader(open(cf)):
                pair = (r["task"], r["worker"])
                full.add(pair)
                if r["task"] in high:
                    routed.add(pair)
            jf, jp = len(full), len(routed)
            eff = [f"{jf}", f"{jp}", f"{jf - jp}", f"{100 * (jf - jp) / jf:.1f}%"]
    cost = eff

    row = [model, "movie_reviews (regression)", "MAE", llm_only,
           f"{h[h_m]:.4f}", h_m, f"{hpv[hp_m]:.4f}" if hpv else "", hp_m,
           f"{pv:.4f}", px, pm, pmeas, prt] + cost + [f"{pv - h[h_m]:+.4f}"]

    # per-model copy stays beside its own allocation folder
    out = REG / "allocation" / model / "best_allocation.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerow(row)

    # one combined table at the results root: upsert this model's row
    comb = RES / "allocation_best_regression.csv"
    rows = {}
    if comb.exists():
        for r in csv.DictReader(open(comb)):
            rows[r["model"]] = [r.get(c, "") for c in HEADER]
    rows[model] = row
    with open(comb, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        for m in ("gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"):
            if m in rows:
                w.writerow(rows[m])
    print(f"  {model}: llm {llm_only} | human {h[h_m]:.4f} ({h_m}) | "
          f"human+llm {hpv[hp_m]:.4f} ({hp_m}) | peak {pv:.4f} @ X={px}% "
          f"{pm}/{pmeas}/{prt} | {cost[2] or '?'} judgments saved ({cost[3] or 'n/a'})")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

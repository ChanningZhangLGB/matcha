#!/usr/bin/env python3
"""Pivot a routing.csv into methods x allocation-budget.

    python results/utils/pivot_routing.py <routing.csv> [--metric accuracy]
    python results/utils/pivot_routing.py --all [--metric accuracy]

routing.csv is long form (one row per X per method). This writes the wide view a
reader actually wants: one ROW per aggregation method, one COLUMN per allocation
budget X (the share of instances routed to humans; the rest take the LLM label).

Two reference rows are appended:
    LLM-only (X=0)    every instance takes the LLM label - the left endpoint
    human-only (X=100) the full human crowd - the right endpoint
so the sweep can be read against both extremes without opening another file.

Writes routing_pivot_<metric>.csv beside the input.
"""
import argparse
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
ORDER = ["DawidSkene", "MajorityVote", "GLAD", "Wawa", "MMSR", "MACE",
         "ZeroBasedSkill", "OneCoinDawidSkene"]


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def pivot(path, metric="accuracy"):
    path = pathlib.Path(path)
    rows = list(csv.DictReader(open(path)))
    if not rows:
        return None
    # --all sweeps every routing.csv under results/, which includes the REGRESSION track
    # (movie_reviews/regression). Those carry MAE/RMSE/R2/r and have no `accuracy` column,
    # so asking for a categorical metric there raised KeyError and aborted the whole run
    # before it reached the datasets that come later alphabetically. Skip, don't crash.
    if metric not in rows[0]:
        return None
    xs = sorted({int(r["X"]) for r in rows})
    got = {(r["method"], int(r["X"])): r[metric] for r in rows}
    methods = [m for m in ORDER if any((m, x) in got for x in xs)]
    methods += sorted({r["method"] for r in rows} - set(methods))

    # endpoints: model dir is .../allocation/<model>/<measure>/<route>/routing.csv
    model = path.parents[2].name
    ds_dir = path.parents[4]
    ref = {}
    st = ds_dir / "summary_table.csv"
    if st.exists():
        acc = next((r for r in csv.DictReader(open(st))
                    if r["metric"].lower() in ("acc", "accuracy")), None)
        f1 = next((r for r in csv.DictReader(open(st))
                   if r["metric"].lower() == "macro_f1"), None)
        src = acc if metric == "accuracy" else f1
        if src:
            ref["llm"] = src.get(f"llm-only: {model}", "")
            ref["human"] = {m: src.get(f"human-only: {m}", "") for m in methods}

    out = path.with_name(f"routing_pivot_{metric}.csv")
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        # X=0 and X=100 are the endpoints of the same sweep, so they belong in the
        # row -- not in a footer that could only ever show one method's value.
        w.writerow(["method", "X=0% (LLM-only)"] + [f"X={x}%" for x in xs]
                   + ["X=100% (human-only)"])
        for m in methods:
            w.writerow([m, ref.get("llm", "")]
                       + [got.get((m, x), "") for x in xs]
                       + [ref.get("human", {}).get(m, "")])
    return out, len(methods), len(xs) + 2


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?")
    ap.add_argument("--metric", default="accuracy")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    targets = ([a.path] if a.path else
               sorted(str(p) for p in RES.glob("*/**/routing.csv")) if a.all else [])
    for t in targets:
        r = pivot(t, a.metric)
        if r:
            out, nm, nx = r
            try:
                shown = out.resolve().relative_to(ROOT)
            except ValueError:
                shown = out
            print(f"  {shown}  ({nm} methods x {nx} budgets)")

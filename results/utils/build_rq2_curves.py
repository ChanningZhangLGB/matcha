#!/usr/bin/env python3
"""RQ2: accuracy vs human allocation ratio -- MATCHA against the allocation baselines.

    python results/utils/build_rq2_curves.py <dataset> <measure> [model ...]
    e.g. python results/utils/build_rq2_curves.py sentiment confidence

THE QUESTION. Every strategy here spends the same thing -- X% of instances annotated by
humans -- so the curves are directly comparable at each budget. What differs is how much
machinery each one is allowed to use on top of that spend.

THREE LINES:

    CoAnnotating   the uncertainty measure, route h-human, MajorityVote ONLY. The
                   published-style baseline: routed instances take the crowd's majority
                   label, the rest keep the LLM's.
    random         the CONTROL. Same selection rule as MATCHA -- best aggregator, best
                   route at each X -- but instances are ranked by a seeded shuffle
                   instead of by uncertainty. It isolates what the uncertainty signal
                   contributes: everything MATCHA gains over this line comes from
                   ranking, and everything below it comes merely from buying human
                   labels.
    MATCHA         the uncertainty measure, BEST AGGREGATOR AND BEST ROUTE at each X --
                   the max ranges over h-human_llm too, where the LLM stays in the pool
                   as an extra annotator rather than being discarded on routed instances.

MATCHA and random are matched on selection width, so their gap is attributable to the
uncertainty ranking rather than to multiplicity. MATCHA vs CoAnnotating is NOT matched:
MATCHA maximises over routes and aggregators while CoAnnotating is fixed to one of each,
so that gap mixes signal with selection and should be read as an upper bound.

The maxima are taken on the same gold the curves are scored against; `n_methods_*` in
the CSV records how wide each max was at every budget.

ENDPOINTS. X=0 is LLM-only and X=100 is the crowd alone; both come from the pivot files'
explicit endpoint columns rather than being extrapolated. At X=0 all three lines
coincide by definition.

Writes results/RQ2/<dataset>/<measure>/curve_<model>.png and curve_data.csv
"""
import collections
import csv
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ2"

ROUTES = {"h-human": "human_only", "h-human_llm": "human_plus_llm"}
TEXT_MODELS = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
IMAGE_MODELS = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]
IMAGE_DATASETS = {"labelme", "imagenet16h"}
SHORT = {"gpt-4o-mini": "gpt-4o-mini", "llama3.1-8b-instruct-q8_0": "llama3.1-8b",
         "qwen2.5-7b-instruct-q8_0": "qwen2.5-7b",
         "minicpm-v-8b-2.6-q8_0": "minicpm-v-8b", "qwen2.5vl-7b-q8_0": "qwen2.5vl-7b"}

SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#dcdbd6"
STYLE = {"MATCHA": ("#2a78d6", 2.2, "-"),
         "CoAnnotating": ("#e08214", 1.8, "-"),
         "random": ("#7a7a7a", 1.6, "--")}


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def load(ds, model, measure):
    """-> {route: {X: {method: acc}}} plus endpoints keyed PER METHOD.

    The X=100 endpoint is stored per aggregator, not pre-maximised. Each line has to
    take the endpoint consistent with its own selection rule: CoAnnotating is
    MajorityVote at every budget, so its X=100 must be MajorityVote's crowd score --
    handing it the best-of-N endpoint would make the baseline jump to a value its own
    policy never produces.
    """
    out, ends = {}, {}
    for folder, route in ROUTES.items():
        f = ddir(ds) / "allocation" / model / measure / route / "routing.csv"
        if not f.exists():
            continue
        d = collections.defaultdict(dict)
        for r in csv.DictReader(open(f)):
            d[int(r["X"])][r["method"]] = float(r["accuracy"])
        out[folder] = d
        p = f.with_name("routing_pivot_accuracy.csv")
        if p.exists():
            rows = list(csv.DictReader(open(p)))
            ends.setdefault("llm_only", float(rows[0]["X=0% (LLM-only)"]))
            ends[folder] = {r["method"]: float(r["X=100% (human-only)"]) for r in rows}
    return out, ends


def curves(ds, model, measure):
    data, ends = load(ds, model, measure)
    rdata, rends = load(ds, model, "random")
    if "h-human" not in data:
        return None
    xs = sorted(data["h-human"])
    series, widths = {k: {} for k in STYLE}, {}
    for x in xs:
        hh = data["h-human"].get(x, {})
        hl = data.get("h-human_llm", {}).get(x, {})
        if "MajorityVote" in hh:
            series["CoAnnotating"][x] = hh["MajorityVote"]
        pool = list(hh.values()) + list(hl.values())
        if pool:
            series["MATCHA"][x] = max(pool)
        # control: same best-aggregator-best-route rule, shuffled ranking
        rh = rdata.get("h-human", {}).get(x, {})
        rl = rdata.get("h-human_llm", {}).get(x, {})
        rpool = list(rh.values()) + list(rl.values())
        if rpool:
            series["random"][x] = max(rpool)
        widths[x] = (len(hh), len(hh) + len(hl))
    # Endpoints, each taken under the SAME rule as its line.
    if "llm_only" in ends:
        for k in series:
            series[k][0] = ends["llm_only"]          # X=0 is LLM-only for all three
    hh_end = ends.get("h-human", {})
    hl_end = ends.get("h-human_llm", {})
    if "MajorityVote" in hh_end:
        series["CoAnnotating"][100] = hh_end["MajorityVote"]
    if hh_end:
        series["MATCHA"][100] = max(list(hh_end.values()) + list(hl_end.values()))
    rh_end = rends.get("h-human", {})
    rl_end = rends.get("h-human_llm", {})
    if rh_end:
        series["random"][100] = max(list(rh_end.values()) + list(rl_end.values()))
    return series, widths


def main(ds, measure, models):
    d = OUT / ds / measure
    d.mkdir(parents=True, exist_ok=True)
    rows = [["dataset", "measure", "model", "X", "CoAnnotating", "random",
             "MATCHA", "n_methods_h-human", "n_methods_both"]]
    n_meth = set()

    for model in models:
        got = curves(ds, model, measure)
        if not got:
            print(f"  {model}: no sweep, skipped")
            continue
        series, widths = got
        xs = sorted(series["MATCHA"])
        for x in xs:
            a, b = widths.get(x, ("", ""))
            if a:
                n_meth.add(a)
            rows.append([ds, measure, SHORT[model], x,
                         series["CoAnnotating"].get(x, ""),
                         series["random"].get(x, ""),
                         series["MATCHA"].get(x, ""), a, b])

        fig, ax = plt.subplots(figsize=(6.4, 4.4))
        fig.patch.set_facecolor(SURFACE)
        ax.set_facecolor(SURFACE)
        ax.grid(True, color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)
        for s in ax.spines:
            ax.spines[s].set_color(GRID)
        ax.tick_params(colors=INK_2, labelsize=9, length=0)
        for name, (col, lw, ls) in STYLE.items():
            pts = sorted(series[name].items())
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col,
                    linewidth=lw, linestyle=ls, marker="o", markersize=3,
                    label=name, zorder=3 if name == "MATCHA" else 2)
        ax.set_xlim(0, 100)
        ax.set_xlabel("human allocation ratio X  (% of instances annotated by humans)",
                      color=INK_2, fontsize=9)
        ax.set_ylabel("accuracy", color=INK_2, fontsize=9)
        ax.set_title(f"{ds} · {SHORT[model]} · {measure}", color=INK,
                     fontsize=11.5, fontweight="bold", loc="left")
        leg = ax.legend(fontsize=8.5, frameon=True, facecolor=SURFACE,
                        edgecolor=GRID, loc="lower left", framealpha=0.95)
        for t in leg.get_texts():
            t.set_color(INK_2)
        fig.tight_layout()
        fig.savefig(d / f"curve_{SHORT[model]}.png", dpi=200, facecolor=SURFACE)
        plt.close(fig)
        print(f"  {(d / f'curve_{SHORT[model]}.png').relative_to(ROOT)}")

    with open(d / "curve_data.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    print(f"  {(d / 'curve_data.csv').relative_to(ROOT)}  ({len(rows)-1} rows)")
    if n_meth:
        print(f"  aggregators available per X on this dataset: {sorted(n_meth)}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    ds, measure = a[0], a[1]
    ms = a[2:] or (IMAGE_MODELS if ds in IMAGE_DATASETS else TEXT_MODELS)
    main(ds, measure, ms)

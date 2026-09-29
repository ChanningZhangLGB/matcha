#!/usr/bin/env python3
"""RQ2 detail: every aggregator's own allocation curve, against the CoAnnotating baseline.

    python results/utils/build_rq2_per_method.py <dataset> <measure> [model ...]

Where build_rq2_curves.py collapses the aggregators into a single best-of line, this
keeps them separate. One line per aggregation method, each taking ITS OWN best route at
each budget -- max(h-human, h-human_llm) for that method -- plus the CoAnnotating
baseline drawn on top.

WHY BEST-OF-ROUTE PER METHOD. The two routes are different policies (h-human discards
the LLM label on routed instances, h-human_llm keeps the LLM in the pool), and which one
suits a method depends on the method: confusion-matrix aggregators can exploit the LLM
as a high-reliability annotator, plain vote-counters cannot. Fixing one route for all
would penalise whichever family it disagrees with, so each method is shown at its best.

MAJORITYVOTE APPEARS TWICE, deliberately:
    MajorityVote          best of the two routes
    CoAnnotating (base)   h-human ONLY, MajorityVote -- the published-style baseline
The vertical gap between them is exactly what route selection buys for the simplest
aggregator, with everything else held fixed. If the two coincide, h-human was already
MajorityVote's better route at that budget.

ENDPOINTS. X=0 is LLM-only (identical for every line). X=100 is that method's crowd-only
score, taken under its own rule -- best-of-route for the method lines, MajorityVote's
h-human value for the baseline.

Writes results/RQ2/<dataset>/<measure>/per_method_<model>.png (+ per_method_data.csv)
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
ORDER = ["MajorityVote", "Wawa", "ZeroBasedSkill", "DawidSkene",
         "OneCoinDawidSkene", "GLAD", "MACE", "MMSR"]
# Palette chosen by OPTIMISATION, not by eye. Candidate colours were simulated under
# protanopia, deuteranopia and tritanopia (Vienot LMS transform), converted to CIE Lab,
# and an 8-subset was searched to maximise the MINIMUM pairwise dE across normal vision
# and all three deficiencies simultaneously. Measured result:
#
#     min dE among the 8 aggregators        28.5
#     min dE to the bronze reference lines  18.7
#     min dE to the black CoAnnotating line 18.7
#     L* ladder  21 29 32 48 52 58 59 69    (capped at 70 so thin lines stay
#                                            visible against white)
#
# For comparison the previous Tol-muted set measured 13.0 -- these are roughly twice as
# separable under colour-vision deficiency. Marker shape remains the redundant channel
# for greyscale print.
STYLES = {
    "MajorityVote":      ("#470788", "o"),   # deep violet
    "Wawa":              ("#880747", "s"),   # dark maroon
    "ZeroBasedSkill":    ("#1616F3", "^"),   # blue
    "DawidSkene":        ("#993DF5", "D"),   # light violet
    "OneCoinDawidSkene": ("#F3163B", "v"),   # red
    "GLAD":              ("#E052C9", "P"),   # magenta
    "MACE":              ("#719C1C", "X"),   # olive green
    "MMSR":              ("#22BF8A", "*"),   # jade
}
# The baseline must not read as a ninth aggregator, so it stays achromatic.
BASELINE = "#111111"

# ---------------------------------------------------------------------------
# Placement of the three reference-level labels. EDIT THESE, not the plotting
# code -- x is in data units (0-100, the budget axis), dy is a vertical nudge in
# points. Defaults put all three at the left edge just above their line; move one
# right if a curve happens to run through it on a particular dataset.
# ---------------------------------------------------------------------------
REF_LABEL_POS = {
    "LLM-only":          {"x": 1.0, "dy": 1.4},
    "Human-only (best)": {"x": 1.0, "dy": 1.4},
    "Crowd-LLM (best)":  {"x": 1.0, "dy": 1.4},
}
TEXT_MODELS = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
IMAGE_MODELS = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]
IMAGE_DATASETS = {"labelme", "imagenet16h"}
SHORT = {"gpt-4o-mini": "gpt-4o-mini", "llama3.1-8b-instruct-q8_0": "llama3.1-8b",
         "qwen2.5-7b-instruct-q8_0": "qwen2.5-7b",
         "minicpm-v-8b-2.6-q8_0": "minicpm-v-8b", "qwen2.5vl-7b-q8_0": "qwen2.5vl-7b"}
SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#dcdbd6"


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def load(ds, model, measure):
    out, ends, llm = {}, {}, None
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
            llm = float(rows[0]["X=0% (LLM-only)"])
            ends[folder] = {r["method"]: float(r["X=100% (human-only)"]) for r in rows}
    return out, ends, llm


def build(ds, model, measure):
    data, ends, llm = load(ds, model, measure)
    if "h-human" not in data:
        return None
    xs = sorted(data["h-human"])
    methods = [m for m in ORDER
               if any(m in data[f].get(x, {}) for f in data for x in xs)]
    series = {m: {} for m in methods}
    which = {}
    for x in xs:
        for m in methods:
            vals = {f: data[f][x][m] for f in data if m in data[f].get(x, {})}
            if not vals:
                continue
            bf = max(vals, key=vals.get)
            series[m][x] = vals[bf]
            which[(m, x)] = bf
    base = {x: data["h-human"][x]["MajorityVote"]
            for x in xs if "MajorityVote" in data["h-human"].get(x, {})}
    if llm is not None:
        for m in methods:
            series[m][0] = llm
        base[0] = llm
    for m in methods:
        e = [ends[f][m] for f in ends if m in ends[f]]
        if e:
            series[m][100] = max(e)
    if "h-human" in ends and "MajorityVote" in ends["h-human"]:
        base[100] = ends["h-human"]["MajorityVote"]
    # Reference levels. human_best is the best aggregator on the crowd ALONE, taken
    # from the h-human X=100 endpoint -- the h-human_llm endpoint still contains the
    # LLM as an annotator and so is not a human-only quantity.
    human_best = max(ends["h-human"].values()) if "h-human" in ends else None
    # Crowd-LLM: the crowd PLUS the LLM as one extra annotator, aggregated with NO
    # routing at all. It does not vary with X, so it is a horizontal reference like the
    # other two -- and it is the strictest of the three, being the best any pool can do
    # when every instance is annotated by both parties.
    cl = ddir(ds) / "model_analysis" / model / "combined_aggregation.csv"
    crowd_llm = None
    if cl.exists():
        vals = [float(r["accuracy"]) for r in csv.DictReader(open(cl))]
        crowd_llm = max(vals) if vals else None
    return series, base, which, methods, llm, human_best, crowd_llm


def main(ds, measure, models):
    d = OUT / ds / measure
    d.mkdir(parents=True, exist_ok=True)
    rows = [["dataset", "measure", "model", "method", "X", "accuracy", "best_route"]]

    for model in models:
        got = build(ds, model, measure)
        if not got:
            print(f"  {model}: no sweep, skipped")
            continue
        series, base, which, methods, llm_lvl, human_lvl, cllm_lvl = got
        for m in methods:
            for x in sorted(series[m]):
                rows.append([ds, measure, SHORT[model], m, x, series[m][x],
                             which.get((m, x), "")])
        for x in sorted(base):
            rows.append([ds, measure, SHORT[model], "CoAnnotating (baseline)", x,
                         base[x], "h-human"])

        # COMPACT single-column format: ~3.4in wide, boxed frame, dotted grid on both
        # axes, legend inside. Sized to sit at 1:1 in a WSDM column so nothing is
        # rescaled by \includegraphics and the 5-6pt type lands at its true size.
        fig, ax = plt.subplots(figsize=(3.4, 1.75))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        ax.grid(True, color="#c8c8c8", linewidth=0.4, linestyle=(0, (1, 1.6)),
                zorder=0)
        ax.set_axisbelow(True)
        for sp in ax.spines.values():           # full box, as in the reference
            sp.set_visible(True)
            sp.set_color("#111111")
            sp.set_linewidth(0.6)
        ax.tick_params(colors="#111111", labelsize=5.2, length=1.8, width=0.5,
                       pad=1.5)

        xs_all = sorted({x for m in methods for x in series[m]})
        mark_at = set(xs_all[::2]) | {0, 100}

        for m in methods:
            col, mk = STYLES.get(m, ("#777777", "o"))
            pts = sorted(series[m].items())
            ax.plot([q[0] for q in pts], [q[1] for q in pts], color=col,
                    linewidth=0.85, zorder=3, solid_capstyle="round")
            mx = [x for x in series[m] if x in mark_at]
            ax.plot(mx, [series[m][x] for x in mx], linestyle="none", marker=mk,
                    markersize=2.3, color=col, markeredgewidth=0, zorder=4,
                    label=m)

        pts = sorted(base.items())
        ax.plot([q[0] for q in pts], [q[1] for q in pts], color=BASELINE,
                linewidth=1.3, linestyle=(0, (3, 1.4)), zorder=6,
                solid_capstyle="round")
        mbx = [x for x in base if x in mark_at]
        ax.plot(mbx, [base[x] for x in mbx], linestyle="none", marker="s",
                markersize=2.6, color=BASELINE, markeredgewidth=0, zorder=7,
                label="CoAnnotating")

        # ---- reference thresholds -------------------------------------------
        # LLM-only is where every curve starts (X=0); human-only best is the crowd
        # alone. Together they bracket what allocation has to beat to be worth doing:
        # a curve below both is worse than either pure strategy at that budget.
        for lvl, lab, col, dash in (
                (llm_lvl, "LLM-only", "#8C4A00", (0, (2, 2))),
                (human_lvl, "Human-only (best)", "#8C4A00", (0, (5, 1.6, 1, 1.6))),
                (cllm_lvl, "Crowd-LLM (best)", "#8C4A00", (0, (1, 1.5)))):
            if lvl is None:
                continue
            ax.axhline(lvl, color=col, linewidth=0.65, linestyle=dash, zorder=2)
            # white backing: these sit at the left edge where the curves are still
            # climbing, so without it the text prints over three or four lines
            pos = REF_LABEL_POS.get(lab, {"x": 1.0, "dy": 1.4})
            ax.annotate(lab, xy=(pos["x"], lvl), xytext=(0, pos["dy"]), fontsize=3.9,
                        textcoords="offset points", color=col, va="bottom",
                        ha="left", zorder=9,
                        bbox=dict(facecolor="white", edgecolor="none",
                                  boxstyle="square,pad=0.12", alpha=0.9))

        # ---- gold star on the single best point across every curve -----------
        star = max(((series[m][x], x, m) for m in methods for x in series[m]),
                   default=None)
        if star is not None:
            ax.plot([star[1]], [star[0]], marker="*", markersize=6.0,
                    color="#FFC300", markeredgecolor="#7a5c00",
                    markeredgewidth=0.4, linestyle="none", zorder=10)

        lo_y = min(min(min(series[m].values()) for m in methods), min(base.values()))
        if llm_lvl is not None:
            lo_y = min(lo_y, llm_lvl)
        for lv in (human_lvl, cllm_lvl):
            if lv is not None:
                lo_y = min(lo_y, lv)
        hi_y = max(max(series[m].values()) for m in methods)
        for lv in (human_lvl, cllm_lvl):
            if lv is not None:
                hi_y = max(hi_y, lv)
        rng = hi_y - lo_y
        # generous headroom: the legend sits INSIDE the axes in this format, so the
        # data has to be pushed clear of it rather than overlapping
        ax.set_ylim(lo_y - rng * 0.08, hi_y + rng * 0.62)
        ax.set_xlim(-2, 102)
        ax.set_xticks([0, 20, 40, 60, 80, 100])
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda v, _: f"{v*100:.0f}"))
        ax.set_xlabel("Human allocation ratio $X$ (%)", color="#111111",
                      fontsize=6, labelpad=1.5)
        ax.set_ylabel("Accuracy (%)", color="#111111", fontsize=6, labelpad=1.5)

        # FIXED legend order, identical in every figure. It was previously sorted by
        # each line's finishing value, which meant the legend re-ordered itself from
        # panel to panel -- fine in isolation, but it makes a multi-figure sheet
        # unreadable because the same method sits in a different slot each time.
        h, l = ax.get_legend_handles_labels()
        rank = {m: i for i, m in enumerate(ORDER)}
        rank["CoAnnotating"] = len(ORDER)          # baseline always last
        idx = sorted(range(len(l)), key=lambda i: rank.get(l[i], 99))
        leg = ax.legend([h[i] for i in idx], [l[i] for i in idx],
                        fontsize=4.4, frameon=False, ncol=2, loc="upper center",
                        handlelength=1.5, labelspacing=0.18, columnspacing=0.7,
                        handletextpad=0.35, borderpad=0.1)
        for t in leg.get_texts():
            t.set_color("#111111")

        for ext in ("pdf", "png"):
            fig.savefig(d / f"per_method_{SHORT[model]}.{ext}", dpi=600,
                        facecolor="white", bbox_inches="tight", pad_inches=0.015)
        plt.close(fig)
        print(f"  {(d / f'per_method_{SHORT[model]}.png').relative_to(ROOT)}"
              f"  ({len(methods)} aggregators)")

    with open(d / "per_method_data.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    print(f"  {(d / 'per_method_data.csv').relative_to(ROOT)}  ({len(rows)-1} rows)")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    ds, measure = a[0], a[1]
    ms = a[2:] or (IMAGE_MODELS if ds in IMAGE_DATASETS else TEXT_MODELS)
    main(ds, measure, ms)

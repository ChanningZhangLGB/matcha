#!/usr/bin/env python3
"""RQ2: per-aggregator allocation curves with the ROUTE HELD FIXED.

    python results/RQ2/allocation_vs_acc/labelme/build_allocation_vs_acc.py

Identical in construction to build_rq2_per_method.py, with one difference. There, each
aggregator takes ITS OWN better route at every budget, so a line can silently switch
policy from one X to the next. Here the allocation strategy is PINNED for the whole
panel, which is what a practitioner actually deploys: one route is chosen up front and
held for the entire corpus.

The route pinned to each dataset is fixed for presentation, not selected by
consensus: the models do not all prefer the same route on QUIZ, nor on LabelMe under the
entropy basis used here.

    Sentiment Polarity   LLM-led    (human_plus_llm)
    QUIZ                 LLM-led    (human_plus_llm)
    LabelMe              Human-led  (human_only)

CoAnnotating stays on h-human with MajorityVote in every panel, since that is its
definition and not a route choice. The Human-only reference likewise comes from the
h-human X=100 endpoint, the only one that contains no LLM annotator.

Writes per_method_<model>.{pdf,png} and per_method_data.csv beside this script.
"""
import collections
import csv
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[4]
RES = ROOT / "results"
OUT = RES / "RQ2" / "allocation_vs_acc"

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
# Placement of the three reference-level labels. EDIT THIS, not the plotting code.
#   x  = position along the budget axis, in data units (0-100)
#   dy = vertical nudge in points, positive moves the label up off its line
#   ha = "left" or "right"; use "right" when x is near 100 so the text stays inside
#
# REF_LABEL_POS["default"] applies everywhere. Add a dataset key to override just
# that panel, e.g. REF_LABEL_POS["labelme"]["Crowd-LLM (best)"] = {"x": 55, "dy": 2}.
# Only the entries you list are overridden; the rest fall back to default.
# ---------------------------------------------------------------------------
REF_LABEL_POS = {
    "default": {
        "LLM-only":          {"x": 1.0, "dy": 1.4, "ha": "left"},
        "Human-only (best)": {"x": 1.0, "dy": 1.4, "ha": "left"},
        "Crowd-LLM (best)":  {"x": 1.0, "dy": 1.4, "ha": "left"},
    },
    "labelme": {},
}


def ref_pos(ds, label):
    d = dict(REF_LABEL_POS["default"].get(label, {"x": 1.0, "dy": 1.4, "ha": "left"}))
    d.update(REF_LABEL_POS.get(ds, {}).get(label, {}))
    return d


PANELS = [("labelme",   "h-human",     "Human-led")]
MEASURE = "entropy"
DISPLAY = {"sentiment": "Sentiment Polarity", "quiz": "QUIZ", "labelme": "LabelMe"}
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


def build(ds, model, measure, route):
    """route is the FIXED folder key, 'h-human' or 'h-human_llm'."""
    data, ends, llm = load(ds, model, measure)
    if route not in data or "h-human" not in data:
        return None
    xs = sorted(data[route])
    methods = [m for m in ORDER if any(m in data[route].get(x, {}) for x in xs)]
    series = {m: {} for m in methods}
    for x in xs:
        for m in methods:
            if m in data[route].get(x, {}):
                series[m][x] = data[route][x][m]
    # CoAnnotating is h-human + MajorityVote by definition, not a route choice.
    base = {x: data["h-human"][x]["MajorityVote"]
            for x in sorted(data["h-human"])
            if "MajorityVote" in data["h-human"].get(x, {})}
    if llm is not None:
        for m in methods:
            series[m][0] = llm
        base[0] = llm
    for m in methods:
        if route in ends and m in ends[route]:
            series[m][100] = ends[route][m]
    if "h-human" in ends and "MajorityVote" in ends["h-human"]:
        base[100] = ends["h-human"]["MajorityVote"]
    human_best = max(ends["h-human"].values()) if "h-human" in ends else None
    cl = ddir(ds) / "model_analysis" / model / "combined_aggregation.csv"
    crowd_llm = None
    if cl.exists():
        vals = [float(r["accuracy"]) for r in csv.DictReader(open(cl))]
        crowd_llm = max(vals) if vals else None
    return series, base, {}, methods, llm, human_best, crowd_llm


def main(ds, measure, models, route, rlabel):
    d = OUT / ds
    d.mkdir(parents=True, exist_ok=True)
    rows = [["dataset", "strategy", "model", "method", "X", "accuracy"]]

    for model in models:
        got = build(ds, model, measure, route)
        if not got:
            print(f"  {model}: no sweep, skipped")
            continue
        series, base, _which, methods, llm_lvl, human_lvl, cllm_lvl = got
        for m in methods:
            for x in sorted(series[m]):
                rows.append([ds, rlabel, SHORT[model], m, x, series[m][x]])
        for x in sorted(base):
            rows.append([ds, rlabel, SHORT[model], "CoAnnotating (baseline)", x,
                         base[x]])

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
                (llm_lvl, "LLM-only", "#610E03", (0, (2, 2))),
                (human_lvl, "Human-only (best)", "#610E03", (0, (5, 1.6, 1, 1.6))),
                (cllm_lvl, "Crowd-LLM (best)", "#610E03", (0, (1, 1.5)))):
            if lvl is None:
                continue
            ax.axhline(lvl, color=col, linewidth=0.65, linestyle=dash, zorder=2)
            # white backing: these sit at the left edge where the curves are still
            # climbing, so without it the text prints over three or four lines
            pos = ref_pos(ds, lab)
            ax.annotate(lab, xy=(pos["x"], lvl), xytext=(0, pos["dy"]), fontsize=3.9,
                        textcoords="offset points", color=col, va="bottom",
                        ha=pos.get("ha", "left"), zorder=9,
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
    for _ds, _route, _label in PANELS:
        _models = IMAGE_MODELS if _ds in IMAGE_DATASETS else TEXT_MODELS
        print(f"== {_ds}  [{_label}]")
        main(_ds, MEASURE, _models, _route, _label)

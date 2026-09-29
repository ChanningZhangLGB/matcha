#!/usr/bin/env python3
"""RQ3 (b): how much does the AGGREGATION METHOD contribute?

    python results/utils/build_rq3_aggregation.py

One radar PER DATASET. The spokes are AGGREGATION METHODS; each polygon is a MODEL.
A vertex is that (model, aggregator) pair's PEAK MATCHA accuracy on the dataset --
maximised over uncertainty basis (random excluded) x budget x route -- so uncertainty
and routing are held at their best and only the aggregator varies around the rim.

TWO THINGS ARE READABLE AT ONCE, which is the reason for this orientation:
    polygon SIZE   how good the model is on this dataset overall
    polygon SHAPE  which aggregators that model depends on -- a round polygon means the
                   aggregator hardly matters, a spiky one means it does

RADIUS IS TRUE ACCURACY, not a per-axis rank. Within one dataset every spoke is the
same metric on the same items, so a shared radial scale is meaningful and the polygons
nest by model quality as they should. The scale is set per dataset to the observed
min-max across all (model, aggregator) cells, padded -- a common scale across datasets
would flatten every polygon to a circle, since dataset difficulty dominates aggregator
choice by an order of magnitude.

    The radial tick labels carry the real percentages. ALWAYS read them: a dataset whose
    aggregators span 0.4 points is drawn as large as one spanning 2.9 points. `spread`
    in the CSV is the number that says whether a shape is worth interpreting.

AGGREGATOR SPOKES are the INTERSECTION of what ran for every model on that dataset --
6 on the text corpora where GLAD and MACE were never swept, 8 elsewhere. A polygon with
a missing vertex would read as a low score rather than as absent data.

Writes results/RQ3/aggregation/radar_<dataset>.{pdf,png}, a combined all_datasets
figure, and aggregation_peaks.csv
"""
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402
import numpy as np                                                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ3" / "aggregation"

ORDER = ["MajorityVote", "Wawa", "ZeroBasedSkill", "DawidSkene",
         "OneCoinDawidSkene", "GLAD", "MACE", "MMSR"]
ABBR = {"MajorityVote": "MV", "Wawa": "Wawa", "ZeroBasedSkill": "ZBS",
        "DawidSkene": "DS", "OneCoinDawidSkene": "1C-DS", "GLAD": "GLAD",
        "MACE": "MACE", "MMSR": "MMSR"}
MEASURES = ["confidence", "entropy", "inter_rater"]      # random is the control
ROUTES = {"h-human": "human_only", "h-human_llm": "human_plus_llm"}

MODEL_STYLE = {
    "gpt-4o-mini":               ("#0072B2", "-",  "o"),
    "llama3.1-8b-instruct-q8_0": ("#D55E00", "--", "s"),
    "qwen2.5-7b-instruct-q8_0":  ("#009E73", "-.", "^"),
    "minicpm-v-8b-2.6-q8_0":     ("#CC79A7", "--", "v"),
    "qwen2.5vl-7b-q8_0":         ("#7B3294", "-.", "D"),
}
# Display names as they appear in the model-profile table and every other figure.
SHORT = {"gpt-4o-mini": "GPT-4o-mini", "llama3.1-8b-instruct-q8_0": "Llama3.1-8B",
         "qwen2.5-7b-instruct-q8_0": "Qwen2.5-7B",
         "minicpm-v-8b-2.6-q8_0": "MiniCPM-V-8B", "qwen2.5vl-7b-q8_0": "Qwen2.5VL-7B"}
TEXT_MODELS = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
IMAGE_MODELS = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]

# Titles on the combined sheet use the official corpus names of the dataset table, so
# the two are read together without a mental mapping. Per-dataset radars stay untitled:
# there the name belongs in the subcaption.
OFFICIAL = {"sentiment": "Sentiment Polarity", "movie_reviews": "MovieReviews",
            "crowdtruth": "CrowdTruth RelEx", "conll_ner_5k": "CoNLL-NER",
            "pico_5k": "PICO", "quiz": "QUIZ", "labelme": "LabelMe",
            "imagenet16h": "ImageNet-16H"}
DATASETS = [("sentiment", "sentiment", "text"),
            ("movie_reviews", "movie_reviews", "text"),
            ("crowdtruth", "crowdtruth_pooled", "text"),
            ("conll_ner_5k", "conll_ner_5k", "text"),
            ("pico_5k", "pico_5k", "text"),
            ("quiz", "quiz", "text"),
            ("labelme", "labelme", "image"),
            ("imagenet16h", "imagenet16h", "image")]


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def peaks(table, model):
    best = {}
    for me in MEASURES:
        for folder, route in ROUTES.items():
            f = ddir(table) / "allocation" / model / me / route / "routing.csv"
            if not f.exists():
                continue
            for r in csv.DictReader(open(f)):
                v = float(r["accuracy"])
                k = r["method"]
                if k not in best or v > best[k][0]:
                    best[k] = (v, me, folder, r["X"])
    return best


def gather(table, arm):
    models = IMAGE_MODELS if arm == "image" else TEXT_MODELS
    data = {m: peaks(table, m) for m in models}
    data = {m: v for m, v in data.items() if v}
    if not data:
        return None, None
    spokes = [a for a in ORDER if all(a in v for v in data.values())]
    return data, spokes


def draw(ax, disp, data, spokes, label_size=6.5, title_size=7.5,
         tick_size=5.6):
    n = len(spokes)
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    ang += ang[:1]
    allv = [data[m][a][0] for m in data for a in spokes]
    lo, hi = min(allv), max(allv)
    pad = (hi - lo) * 0.28 or 0.005
    r0, r1 = lo - pad, hi + pad * 0.55

    for m in data:
        col, ls, mk = MODEL_STYLE[m]
        rs = [data[m][a][0] for a in spokes]
        rs += rs[:1]
        ax.plot(ang, rs, color=col, linestyle=ls, linewidth=1.0, marker=mk,
                markersize=2.4, markeredgewidth=0, label=SHORT[m], zorder=3)
        ax.fill(ang, rs, color=col, alpha=0.055, zorder=2)
        # Highlight this MODEL's best aggregator. Filled star in the model's own colour
        # with a dark rim, so the mark is attributable to a polygon -- a single neutral
        # highlight colour would be ambiguous where two polygons peak on the same spoke.
        bi = int(np.argmax(rs[:-1]))
        ax.plot([ang[bi]], [rs[bi]], marker="*", markersize=6.4, color=col,
                markeredgecolor="#111111", markeredgewidth=0.45, linestyle="none",
                zorder=7)

    ax.set_xticks(ang[:-1])
    ax.set_xticklabels([ABBR[a] for a in spokes], fontsize=label_size, color="#111111")
    ax.set_ylim(r0, r1)
    # Two radial ticks only, and placed MIDWAY BETWEEN spokes: at rlabel_position=0 the
    # numbers land on a spoke and are overprinted by the polygons crossing it.
    # Only the OUTER ring is labelled. The inner label sits close to the pole, where on
    # an 8-spoke panel it collided with the axes clip and rendered as "8.5" instead of
    # "78.5". The full range lives in the title instead, which is unambiguous.
    ticks = [lo, hi]
    ax.set_yticks(ticks)
    ax.set_yticklabels(["", f"{hi*100:.1f}"], fontsize=tick_size, color="#5a5a5a")
    ax.set_rlabel_position(180.0 / n)
    for lbl in ax.get_yticklabels():
        lbl.set_bbox(dict(facecolor="white", edgecolor="none", pad=0.6, alpha=0.85))
        # the inner tick sits near the pole where the axes clip path cuts the text --
        # "78.5" was rendering as "8.5" before this
        lbl.set_clip_on(False)
        lbl.set_zorder(9)
    ax.tick_params(pad=1.2)
    ax.grid(color="#cccccc", linewidth=0.4)
    ax.spines["polar"].set_color("#8a8a8a")
    ax.spines["polar"].set_linewidth(0.6)
    # No title: the dataset name and its accuracy range are carried by the subcaption
    # in the manuscript. The range still reaches the reader through the radial tick
    # labels, which are drawn in true accuracy units rather than in scaled radius.
    _ = (disp, lo, hi, title_size)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [["arm", "dataset", "model", "aggregator", "peak_accuracy", "uncertainty",
             "route", "X", "rank_for_model", "dataset_spread"]]
    store = {}

    for disp, table, arm in DATASETS:
        data, spokes = gather(table, arm)
        if not data:
            print(f"  {disp}: no data")
            continue
        store[disp] = (data, spokes, arm)

        fig = plt.figure(figsize=(3.3, 2.9))
        ax = fig.add_subplot(111, projection="polar")
        draw(ax, disp, data, spokes)
        leg = ax.legend(fontsize=6.2, frameon=False, ncol=3,
                        loc="lower center", bbox_to_anchor=(0.5, -0.20),
                        handlelength=1.7, labelspacing=0.3, columnspacing=1.1,
                        handletextpad=0.4)
        for t in leg.get_texts():
            t.set_color("#111111")
        for ext in ("pdf", "png"):
            fig.savefig(OUT / f"radar_{disp}.{ext}", dpi=600, facecolor="white",
                        bbox_inches="tight", pad_inches=0.03)
        plt.close(fig)

        allv = [data[m][a][0] for m in data for a in spokes]
        spread = max(allv) - min(allv)
        for m in data:
            order = sorted(((data[m][a][0], a) for a in spokes), reverse=True)
            rank = {a: i + 1 for i, (_, a) in enumerate(order)}
            for a in spokes:
                v, me, rt, X = data[m][a]
                rows.append([arm, disp, SHORT[m], a, f"{v:.4f}", me, rt, X,
                             rank[a], f"{spread:.4f}"])

    # combined 2 x 4 sheet
    fig = plt.figure(figsize=(7.0, 3.75))
    for i, (disp, table, arm) in enumerate(DATASETS):
        if disp not in store:
            continue
        data, spokes, _ = store[disp]
        ax = fig.add_subplot(2, 4, i + 1, projection="polar")
        draw(ax, disp, data, spokes, label_size=5.4, title_size=6.6,
             tick_size=4.6)
        ax.set_title(OFFICIAL.get(disp, disp), fontsize=6.4, fontweight="bold",
                     pad=4, color="#111111")
    handles = [plt.Line2D([], [], color=MODEL_STYLE[m][0],
                          linestyle=MODEL_STYLE[m][1], marker=MODEL_STYLE[m][2],
                          markersize=3, linewidth=1.1, label=SHORT[m])
               for m in MODEL_STYLE]
    leg = fig.legend(handles=handles, fontsize=6.0, frameon=False, ncol=5,
                     loc="lower center", bbox_to_anchor=(0.5, -0.012),
                     handlelength=1.8, columnspacing=1.5, handletextpad=0.45)
    for t in leg.get_texts():
        t.set_color("#111111")
    # No footnote: the eight aggregators and their abbreviations are defined in the
    # experimental setup, and the star and radius conventions belong in the caption.
    fig.tight_layout(h_pad=0.35, w_pad=0.55)
    fig.subplots_adjust(top=0.93, bottom=0.075)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"radar_all_datasets.{ext}", dpi=600, facecolor="white",
                    bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)

    with open(OUT / "aggregation_peaks.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)

    print(f"  {len(store)} per-dataset radars + radar_all_datasets  "
          f"({len(rows)-1} rows)")
    print(f"  {'dataset':16s} {'spokes':>6s} {'spread':>8s}   best (model / aggregator)")
    for disp, (data, spokes, arm) in store.items():
        allv = [(data[m][a][0], SHORT[m], a) for m in data for a in spokes]
        b = max(allv)
        print(f"  {disp:16s} {len(spokes):6d} {max(v[0] for v in allv) - min(v[0] for v in allv):8.4f}"
              f"   {b[1]} / {b[2]}  {b[0]:.4f}")


if __name__ == "__main__":
    main()

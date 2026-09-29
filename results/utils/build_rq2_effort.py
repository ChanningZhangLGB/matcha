#!/usr/bin/env python3
"""RQ2: how much HUMAN EFFORT does MATCHA save against Crowd-LLM at its best accuracy?

    python results/utils/build_rq2_effort.py

Crowd-LLM annotates EVERY instance with the crowd and adds the LLM as one extra
annotator, so its human cost is the full judgment count of the dataset -- and it is
model-agnostic, because the crowd does the same work whichever LLM joins the pool.
MATCHA routes only the X% most-uncertain instances to humans, so its human cost is the
judgments on that subset alone, and it differs per model because each model peaks at a
different budget.

EFFORT IS COUNTED IN JUDGMENTS, and only over the instances actually experimented on --
the eval tables in eval/data/, not the upstream corpora. A judgment is one DISTINCT
(effort, worker) pair:

  * crowdtruth_pooled namespaces one sentence as c<id>/t<id>, but a single CrowdFlower
    HIT answered both relation questions, so those two rows are ONE human act. Counting
    rows would overstate its effort by 64% (24,530 vs 14,920).
  * imagenet16h contains 6 rows where one worker labelled the same image twice.

The routed subset is read from the peak measure's splits.csv, so the count is the exact
set of instances MATCHA sent to humans -- not n_judgments x X/100, which would be wrong
wherever routing selects instances with unusual annotator counts (crowdtruth ranges
15-30 judgments per sentence, conll_ner 1-8 per token).

BARS ARE NORMALISED to Crowd-LLM = 100%. Absolute judgment counts differ by an order of
magnitude across datasets (2,547 on LabelMe vs 31,119 on PICO), so a shared linear axis
would render the small datasets invisible. The true counts are printed on each bar and
carried in the CSV.

Writes results/RQ2/compare_aggregation/effort_vs_crowdllm.{pdf,png,csv}
"""
import collections
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402
import numpy as np                                                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ2" / "compare_aggregation"
MEAS = ["confidence", "entropy", "inter_rater"]
ROUTES = ["human_only", "human_plus_llm"]
DATASETS = [("Sentiment Polarity", "sentiment", "text"),
            ("MovieReviews", "movie_reviews", "text"),
            ("CrowdTruth RelEx", "crowdtruth_pooled", "text"),
            ("CoNLL-2003 NER", "conll_ner_5k", "text"),
            ("PICO", "pico_5k", "text"), ("QUIZ", "quiz", "text"),
            ("LabelMe", "labelme", "image"), ("ImageNet-16H", "imagenet16h", "image")]
TEXT = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
IMAGE = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]
SHORT = {"gpt-4o-mini": "GPT-4o-mini", "llama3.1-8b-instruct-q8_0": "Llama3.1-8B",
         "qwen2.5-7b-instruct-q8_0": "Qwen2.5-7B",
         "minicpm-v-8b-2.6-q8_0": "MiniCPM-V-8B", "qwen2.5vl-7b-q8_0": "Qwen2.5VL-7B"}
# Pale fills with BLACK hatching and black outlines -- the same convention as the RQ3
# ablation bars, so the two figures read as one family. Texture, not hue, carries the
# identity: printed in greyscale the four fills collapse to near-identical light greys
# and the hatch is all that survives. Crowd-LLM keeps the neutral grey + dots used for
# reference series elsewhere, so the baseline stays visually subordinate to the three
# MATCHA bars it is being compared against.
CROWD_LLM_COL, CROWD_LLM_HATCH = "#BDBDBD", "..."
# Keyed by MODEL, not by slot, and identical to MODEL_STYLE in
# build_rq3_aggregation.py -- a model keeps one colour across every figure in the
# paper, so a reader who has learned "blue = GPT-4o-mini" on the radars carries that
# here. Slot-keyed colour would have made the same hue mean Llama in one panel and
# MiniCPM in the other.
# Standard primary-family colours -- blue / red / yellow / green / purple. Plain,
# conventional, and immediately readable; hatch patterns carry the identity redundantly
# for greyscale print.
# Dark fills chosen so the white bold in-bar counts stay legible. Contrast ratios for
# white text: royal blue 4.85:1, red 3.36:1, purple 7.70:1, green 2.18:1,
# pink 5.87:1.
MODEL_COL = {
    "gpt-4o-mini":               "#4169E1",   # royal blue
    "llama3.1-8b-instruct-q8_0": "#E8483F",   # red
    "qwen2.5-7b-instruct-q8_0":  "#7B3294",   # dark purple
    "minicpm-v-8b-2.6-q8_0":     "#6FC276",   # green
    "qwen2.5vl-7b-q8_0":         "#C2185B",   # dark pink
}
# Pale fills with BLACK hatching and black outlines -- the same convention as the RQ3
# ablation bars, so the two figures read as one family. Texture, not hue, carries the
# identity: printed in greyscale the four fills collapse to near-identical light greys
# and the hatch is all that survives. Crowd-LLM keeps the neutral grey + dots used for
# reference series elsewhere, so the baseline stays visually subordinate to the three
# MATCHA bars it is being compared against.
CROWD_LLM_COL, CROWD_LLM_HATCH = "#BDBDBD", "..."
# Keyed by MODEL, not by slot, and identical to MODEL_STYLE in
# build_rq3_aggregation.py -- a model keeps one colour across every figure in the
# paper, so a reader who has learned "blue = GPT-4o-mini" on the radars carries that
# here. Slot-keyed colour would have made the same hue mean Llama in one panel and
# MiniCPM in the other.


def ink_on(hexcol):
    """Readable text colour for a fill: relative luminance decides black vs white."""
    r, g, b = (int(hexcol[i:i+2], 16) / 255 for i in (1, 3, 5))
    lin = [(c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4) for c in (r, g, b)]
    return "#111111" if 0.2126*lin[0] + 0.7152*lin[1] + 0.0722*lin[2] > 0.42 else "white"
# Keyed by MODEL, like the colours. Slot-keyed hatching gave only three patterns
# cycling, so Llama and MiniCPM shared one and Qwen2.5-7B and Qwen2.5VL shared another
# -- fine within a panel, but the legend showed the same texture twice for different
# models. Five distinct patterns remove that ambiguity and make the bars separable in
# greyscale without relying on fill colour at all.
MODEL_HATCH = {"gpt-4o-mini": "///", "llama3.1-8b-instruct-q8_0": "xxx",
               "qwen2.5-7b-instruct-q8_0": "\\\\\\",
               "minicpm-v-8b-2.6-q8_0": "...", "qwen2.5vl-7b-q8_0": "++"}


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def effort_key(table, task):
    return task[1:] if table == "crowdtruth_pooled" else task


def judgments(table, high=None):
    """Distinct (effort, worker) pairs; restricted to `high` when given."""
    f = ROOT / "eval" / "data" / f"{table}_crowd.csv"
    out = set()
    for r in csv.DictReader(open(f)):
        if high is not None and r["task"] not in high:
            continue
        out.add((effort_key(table, r["task"]), r["worker"]))
    return len(out)


def peak(table, model):
    best = None
    for me in MEAS:
        for rt in ROUTES:
            f = ddir(table) / "allocation" / model / me / rt / "routing.csv"
            if not f.exists():
                continue
            for r in csv.DictReader(open(f)):
                v = float(r["accuracy"])
                if best is None or v > best[0]:
                    best = (v, me, rt, r["method"], int(r["X"]))
    return best


def routed(table, model, measure, X):
    f = ddir(table) / "allocation" / model / measure / "splits.csv"
    col = f"x{X:02d}"
    rows = list(csv.DictReader(open(f)))
    return {r["task"] for r in rows if r[col] == "high"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [["modality", "dataset", "model", "crowd_llm_judgments",
             "matcha_judgments", "judgments_saved", "effort_saved_pct",
             "matcha_pct_of_crowdllm", "peak_accuracy", "uncertainty", "route",
             "aggregator", "X"]]
    data = {}
    for disp, table, arm in DATASETS:
        full = judgments(table)
        for m in (IMAGE if arm == "image" else TEXT):
            p = peak(table, m)
            if not p:
                continue
            acc, me, rt, agg, X = p
            j = judgments(table, routed(table, m, me, X))
            data[(disp, m)] = (full, j)
            rows.append([arm, disp, SHORT[m], full, j, full - j,
                         f"{100*(full-j)/full:.1f}%", f"{100*j/full:.1f}%",
                         f"{acc:.4f}", me, rt, agg, X])
    with open(OUT / "effort_vs_crowdllm.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)

    plt.rcParams["hatch.linewidth"] = 0.45
    TEXT_DS = [d for d in DATASETS if d[2] == "text"]
    IMG_DS = [d for d in DATASETS if d[2] == "image"]
    fig, axes = plt.subplots(
        1, 2, figsize=(7.0, 2.35), sharey=True,
        gridspec_kw={"width_ratios": [len(TEXT_DS), len(IMG_DS)], "wspace": 0.05})

    for ax, block, models, title in (
            (axes[0], TEXT_DS, TEXT, "Text"),
            (axes[1], IMG_DS, IMAGE, "Image")):
        ax.set_facecolor("white")
        ax.grid(True, axis="y", color="#d8d8d8", linewidth=0.35,
                linestyle=(0, (1, 1.8)), zorder=0)
        ax.set_axisbelow(True)
        for sp in ax.spines.values():
            sp.set_color("#111111"); sp.set_linewidth(0.55)
        ax.tick_params(colors="#111111", labelsize=6.4, length=2.0, width=0.5, pad=1.8)
        # Crowd-LLM is the BASELINE, not a fourth series: the y-axis is already
        # expressed as a percentage of it, so it is the 100% line by definition.
        # Drawing it as a bar made the legend mix one METHOD with three MODELS, which
        # is a category error -- the bars answer "which model", the line answers
        # "compared to what".
        # Short names + horizontal text so each label centres under its own block.
        # Rotated labels with ha="right" anchor at the label's end, which visually
        # shifts them off-centre from the bars they describe.
        SHORTEN = {"Sentiment Polarity": "Sentiment", "MovieReviews": "MovieRev.",
                   "CrowdTruth RelEx": "CrowdTruth", "CoNLL-2003 NER": "CoNLL-03",
                   "ImageNet-16H": "ImageNet-16H"}
        labels = [f"{SHORTEN.get(d, d)}\n({judgments(t):,})" for d, t, _ in block]
        xs = np.arange(len(labels)); w = 0.26
        ax.axhline(100, color="#111111", linewidth=0.9, linestyle=(0, (4, 2)),
                   zorder=6)
        for k, mdl in enumerate(models):
            vals, cnt = [], []
            for disp, table, _ in block:
                full, j = data.get((disp, mdl), (None, None))
                vals.append(100*j/full if full else np.nan); cnt.append(j)
            ax.bar(xs + (k - 1)*w, vals, width=w, color=MODEL_COL[mdl],
                   hatch=MODEL_HATCH[mdl], edgecolor="#111111", linewidth=0.45,
                   zorder=3, label=SHORT[mdl])
            # Counts sit INSIDE the bar, just under its top edge. Printed above, the
            # labels on tall bars (>90%) collided with the Crowd-LLM baseline line and
            # were clipped -- and raising the axis limit only pushed the collision up
            # with them, since the line is at a fixed 100%.
            for xi, (v, jj) in enumerate(zip(vals, cnt)):
                if v != v:
                    continue
                # Inside the bar when it is tall enough to hold the rotated text,
                # otherwise above it. A fixed inside-placement pushed the label off
                # the bottom of short bars (QUIZ/GPT-4o-mini sits at 12%).
                if v >= 26:
                    ax.annotate(f"{jj:,}", xy=(xs[xi] + (k-1)*w, v), xytext=(0, -2.4),
                                textcoords="offset points", ha="center", va="top",
                                fontsize=4.8, rotation=90, color="white",
                                fontweight="bold", zorder=8)
                else:
                    ax.annotate(f"{jj:,}", xy=(xs[xi] + (k-1)*w, v), xytext=(0, 2.0),
                                textcoords="offset points", ha="center", va="bottom",
                                fontsize=4.8, rotation=90, color="#111111",
                                fontweight="bold", zorder=8)
        ax.set_xticks(xs)
        ax.set_xticklabels(labels, fontsize=6.2, rotation=0, ha="center")
        ax.set_xlim(-0.6, len(labels) - 0.4)
        # Title sits just ABOVE its own axes, tight to the frame -- attached to the
        # panel it names, and clear of the shared legend that sits higher up.
        ax.set_title(title, fontsize=7.4, fontweight="bold", color="#111111", pad=3)

    # ONE shared legend. Crowd-LLM and GPT-4o-mini appear in both panels, so per-panel
    # legends listed them twice; de-duplicate by label while preserving first-seen order.
    handles, labs = [], []
    for ax in axes:
        for h, l in zip(*ax.get_legend_handles_labels()):
            if l not in labs:
                handles.append(h); labs.append(l)
    leg = fig.legend(handles, labs, fontsize=6.4, frameon=False, ncol=len(labs),
                     loc="upper center", bbox_to_anchor=(0.5, 1.08),
                     handlelength=1.3, columnspacing=1.1, handletextpad=0.35)
    for t in leg.get_texts():
        t.set_color("#111111")

    axes[0].annotate("Crowd-LLM baseline (100%)", xy=(-0.46, 100), xytext=(0, 2.4),
                     textcoords="offset points", fontsize=6.0, color="#111111",
                     ha="left", va="bottom",
                     bbox=dict(facecolor="white", edgecolor="none", pad=0.6, alpha=0.9))
    axes[0].set_ylim(0, 122)
    axes[0].set_ylabel("Human effort (% of Crowd-LLM)", fontsize=7.0, labelpad=3)
    axes[1].tick_params(axis="y", left=False)
    fig.patch.set_facecolor("white")
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"effort_vs_crowdllm.{ext}", dpi=600, facecolor="white",
                    bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(f"  {(OUT/'effort_vs_crowdllm.csv').relative_to(ROOT)}  ({len(rows)-1} rows)")
    for r in rows[1:]:
        print(f"   {r[1]:20s} {r[2]:13s} {r[4]:>7,} / {r[3]:>7,}  saved {r[6]:>6s}")


if __name__ == "__main__":
    main()

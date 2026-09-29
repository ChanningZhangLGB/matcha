#!/usr/bin/env python3
"""RQ3: the shape of the uncertainty distribution, per dataset and annotator model.

    python results/utils/build_rq3_uncertainty_distribution.py

Two properties govern how much a ranking can actually do, and neither is visible in an
accuracy curve.

TIED MASS. Entropy and inter-rater agreement are exactly 0 whenever all m conditions
return the same label, and on these corpora that is the common case. Every instance in
that block is indistinguishable to the ranker, so once the budget exceeds the untied
fraction, which instances get routed is arbitrary. Any gain past that point comes from
buying more human labels, not from ranking them, which is precisely what the random
control in build_rq3_uncertainty.py isolates.

GRANULARITY. A measure over m=9 conditions can take only a handful of distinct values.
With 19 budgets in the sweep and often fewer than a dozen levels, most budget cuts fall
inside a tie block rather than between two levels. Stated confidence is far finer, having
a continuous scale, which is a practical argument for it that its AUROC does not make.

Left panel is the tied fraction, right is the number of distinct levels, both for the
inter-rater measure, whose values coincide with entropy's on most cells.

Writes results/RQ3/uncertainty_distribution.{pdf,png}
"""
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402
import numpy as np                                                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ3"
MEASURE = "inter_rater"
DISP = {"sentiment": "Sentiment", "movie_reviews": "MovieRev.",
        "crowdtruth_pooled": "CrowdTruth", "conll_ner_5k": "CoNLL-03",
        "pico_5k": "PICO", "quiz": "QUIZ", "labelme": "LabelMe",
        "imagenet16h": "ImageNet-16H"}
ORDER = ["sentiment", "movie_reviews", "crowdtruth_pooled", "conll_ner_5k",
         "pico_5k", "quiz", "labelme", "imagenet16h"]
MODEL_COL = {"GPT-4o-mini": "#4169E1", "Llama3.1-8B": "#E8483F",
             "Qwen2.5-7B": "#7B3294", "MiniCPM-V-8B": "#6FC276",
             "Qwen2.5VL-7B": "#C2185B"}
HATCH = {"GPT-4o-mini": "///", "Llama3.1-8B": "xxx", "Qwen2.5-7B": "\\\\\\",
         "MiniCPM-V-8B": "...", "Qwen2.5VL-7B": "++"}
INK, GRID = "#111111", "#d8d8d8"


def main():
    rows = [r for r in csv.DictReader(open(OUT / "uncertainty_distribution.csv"))
            if r["measure"] == MEASURE]
    by = {}
    for r in rows:
        by.setdefault(r["dataset"], []).append(r)
    plt.rcParams.update({"font.size": 6.6, "hatch.linewidth": 0.45})
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.1))
    fig.patch.set_facecolor("white")
    xs = np.arange(len(ORDER))
    for ax, key, lab in ((axes[0], "pct_zero", "Instances with $u=0$ (%)"),
                         (axes[1], "n_distinct", "Distinct uncertainty levels")):
        ax.set_facecolor("white")
        ax.grid(True, axis="y", color=GRID, linewidth=0.4, linestyle=(0, (1, 2)),
                zorder=0)
        ax.set_axisbelow(True)
        for sp in ax.spines.values():
            sp.set_color(INK); sp.set_linewidth(0.55)
        ax.tick_params(colors=INK, labelsize=5.6, length=1.8, width=0.5, pad=1.4)
        w = 0.26
        for i, ds in enumerate(ORDER):
            for j, r in enumerate(sorted(by.get(ds, []), key=lambda x: x["model"])):
                ax.bar(i + (j - 1) * w, float(r[key]), width=w,
                       color=MODEL_COL[r["model"]], hatch=HATCH[r["model"]],
                       edgecolor=INK, linewidth=0.4, zorder=3,
                       label=r["model"] if i == 0 or r["model"] not in
                       [x["model"] for d in ORDER[:i] for x in by.get(d, [])] else None)
        ax.set_xticks(xs)
        ax.set_xticklabels([DISP[d] for d in ORDER], fontsize=5.4, rotation=30,
                           ha="right")
        ax.set_ylabel(lab, fontsize=6.3, color=INK, labelpad=2)
    axes[0].axhline(100, color=INK, linewidth=0.5, linestyle=(0, (3, 2)), zorder=4)
    h, l = [], []
    for ax in axes:
        for hh, ll in zip(*ax.get_legend_handles_labels()):
            if ll not in l:
                h.append(hh); l.append(ll)
    leg = fig.legend(h, l, fontsize=5.6, frameon=False, ncol=5, loc="upper center",
                     bbox_to_anchor=(0.5, 1.07), handlelength=1.5, columnspacing=1.4,
                     handletextpad=0.4)
    for t in leg.get_texts():
        t.set_color(INK)
    fig.subplots_adjust(wspace=0.26)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"uncertainty_distribution.{ext}", dpi=600,
                    facecolor="white", bbox_inches="tight", pad_inches=0.03)
    print(f"  {(OUT / 'uncertainty_distribution.png').relative_to(ROOT)}")


if __name__ == "__main__":
    main()

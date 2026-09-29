#!/usr/bin/env python3
"""Reliability diagrams across the prompt-variation ladder k0..k3.

    python results/utils/build_calibration_reliability.py [dataset ...]

One row of four panels per (dataset, model, measure): the four uncertainty sources of
build_calibration.py, in increasing order of how much prompt variation the uncertainty
is measured across.

    k0  basic x vanilla                 k=1   no variation, the model's self-report
    k1  basic x {vanilla, cot, topk}    k=3   vary the elicitation protocol
    k2  {basic, control, customized} x vanilla   k=3   vary the prompt wording
    k3  3 groups x 3 protocols          k=9   the full grid used by the pipeline

Bars are accuracy within each confidence bin; the diagonal is perfect calibration. The
shaded wedge between bar and diagonal is the calibration gap, hatched one way where the
bin is OVERCONFIDENT (accuracy below stated confidence) and the other where it is
UNDERCONFIDENT. ECE is the population-weighted area of those wedges, so the figure and
the number in the panel title measure the same thing.

BINS. 15 equal-width bins on [0,1], the number used by Guo et al. Empty bins contribute
nothing, which matters here because 60-80% of instances sit at the top of the scale.

Writes results/calibration_analysis/<ds>_calibration/<measure>/gap_<model>.{pdf,png}
"""
import collections
import csv
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402
from matplotlib.patches import Patch                                 # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_calibration as C                                        # noqa: E402

NBINS = 15
BAR = "#8FD3C7"          # accuracy bars
OVER = "#D9D9D9"         # overconfident wedge
UNDER = "#F2F2F2"        # underconfident wedge
INK = "#111111"


def curve(pairs, ceil, nbins=NBINS):
    """-> [(bin_centre, mean_conf, acc, n)] over equal-width bins OF CONFIDENCE.

    Bins are formed on confidence = 1 - u_norm, not on u, so that a bar sits at the
    confidence it describes. Binning on u gives the same partition and therefore the
    same ECE, but mirrors the x-axis.
    """
    cc = [(1.0 - (u / ceil if ceil else 0.0), c) for u, c in pairs]
    out = []
    for b in range(nbins):
        lo, hi = b / nbins, (b + 1) / nbins
        sel = [(f, c) for f, c in cc
               if (lo <= f < hi) or (b == nbins - 1 and f >= hi)]
        if not sel:
            continue
        conf = sum(f for f, _ in sel) / len(sel)
        acc = sum(c for _, c in sel) / len(sel)
        out.append(((lo + hi) / 2, conf, acc, len(sel)))
    return out


def panel(ax, pts, w):
    for centre, conf, acc, _ in pts:
        lo = centre - w / 2
        ax.bar(centre, acc, width=w, color=BAR, edgecolor=INK, linewidth=0.5,
               zorder=3)
        # wedge between the bar and the diagonal, drawn at the bin's own confidence
        if abs(acc - conf) > 1e-9:
            lo_y, hi_y = min(acc, conf), max(acc, conf)
            ax.bar(centre, hi_y - lo_y, bottom=lo_y, width=w,
                   color=OVER if acc < conf else UNDER,
                   edgecolor=INK, linewidth=0.5, zorder=2,
                   hatch="///" if acc < conf else "---")
    ax.plot([0, 1], [0, 1], color=INK, linewidth=0.8, linestyle=(0, (4, 2)), zorder=5)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])


def main(datasets):
    plt.rcParams.update({"font.size": 6.6, "hatch.linewidth": 0.5})
    for ds in datasets:
        gold = {r["task"]: r["true_label"]
                for r in csv.DictReader(open(C.LONG / f"{ds}_gold.csv"))}
        for model in C.models_for(ds):
            conds_all = C.merge_variants(C.U.conditions(model, ds))
            if not conds_all:
                continue
            data = {}
            for skey, _lab, pred in C.SOURCES:
                conds = {c: v for c, v in conds_all.items()
                         if pred(*C.parse_cond(c))}
                if not conds:
                    continue
                pi = C.per_instance(conds, gold)
                k = len(conds)
                n_classes = len({lab for lab, _, _, _ in pi.values()})
                data[skey] = (pi, k, n_classes)
            for meas in C.MEASURES:
                fig, axes = plt.subplots(1, 4, figsize=(7.0, 1.95), sharey=True)
                fig.patch.set_facecolor("white")
                drew = False
                for ax, (skey, _l, _p) in zip(axes, C.SOURCES):
                    ax.set_facecolor("white")
                    for sp in ax.spines.values():
                        sp.set_color(INK); sp.set_linewidth(0.6)
                    ax.tick_params(colors=INK, labelsize=5.6, length=1.8, width=0.5,
                                   pad=1.4)
                    if skey not in data:
                        ax.set_axis_off(); continue
                    pi, k, n_classes = data[skey]
                    pairs = [(u[meas], corr) for _, corr, u, _ in pi.values()
                             if u[meas] is not None]
                    if not pairs:
                        ax.text(0.5, 0.5, f"undefined at $k$={k}", ha="center",
                                va="center", fontsize=5.4, color="#666666")
                        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
                        ax.set_title(f"$k$={k}", fontsize=6.4, color=INK, pad=2.5)
                        continue
                    ceil = C.ceiling(meas, k, n_classes)
                    pts = curve(pairs, ceil)
                    panel(ax, pts, 1.0 / NBINS)
                    e = C.ece(pairs, ceil, NBINS); a = C.auroc(pairs)
                    ax.set_title(f"$k$={k}   ECE {e:.3f}   AUROC {a:.3f}",
                                 fontsize=6.0, color=INK, pad=2.5)
                    ax.set_xlabel("Confidence", fontsize=6.2, color=INK, labelpad=1.5)
                    drew = True
                if not drew:
                    plt.close(fig); continue
                axes[0].set_ylabel("Accuracy", fontsize=6.4, color=INK, labelpad=2)
                axes[0].legend(handles=[
                    Patch(facecolor=UNDER, edgecolor=INK, hatch="---",
                          linewidth=0.5, label="Underconf."),
                    Patch(facecolor=OVER, edgecolor=INK, hatch="///",
                          linewidth=0.5, label="Overconf.")],
                    fontsize=5.0, frameon=True, loc="upper left", handlelength=1.5,
                    borderpad=0.28, labelspacing=0.22, handletextpad=0.4)
                d = C.outdir(ds) / meas
                d.mkdir(parents=True, exist_ok=True)
                for ext in ("pdf", "png"):
                    fig.savefig(d / f"gap_{model}.{ext}", dpi=600, facecolor="white",
                                bbox_inches="tight", pad_inches=0.02)
                plt.close(fig)
            print(f"  {ds} / {model}: gap_*.png for {len(C.MEASURES)} measures")


if __name__ == "__main__":
    main(sys.argv[1:] or ["sentiment", "movie_reviews", "crowdtruth_pooled",
                          "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"])

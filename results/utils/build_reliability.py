#!/usr/bin/env python3
"""Confidence histogram + reliability diagram, one column per uncertainty source.

    python results/utils/build_reliability.py [dataset] [model ...]

For each dataset x model x MEASURE a single 2x4 figure:

    row 1  EMPIRICAL DISTRIBUTION  stacked count of instances by confidence, split
           correct (blue) / wrong (red). Shows WHERE the mass sits and how much of
           it is wrong.
    row 2  RELIABILITY DIAGRAM     accuracy within each confidence bin against the
           bin's mean confidence, with the y=x diagonal. Bars below the diagonal are
           OVERCONFIDENT.

    columns  k0 / k1 / k2 / k3, the four uncertainty sources of build_calibration.py

WHAT "CONFIDENCE" MEANS PER MEASURE -- read this before comparing the three folders.

    confidence   1 - u_confidence. The model's OWN stated probability. This is the
                 only one where the reliability diagram carries its textbook meaning:
                 "when it says 80%, is it right 80% of the time?"
    entropy      1 - u_entropy / ln(min(k, n_classes))
    inter_rater  1 - u_agreement

The latter two are CONSISTENCY scores rescaled to [0,1], not probabilities the model
asserted. A bar below the diagonal there does not mean "overconfident" -- it means the
agreement rate among k conditions runs higher than the accuracy it implies, which is a
statement about redundancy between conditions, not about self-knowledge. Their ECE is
therefore a scale-mismatch measure, not a calibration error. Use the discrimination
figures (build_discrimination.py) to compare the three measures on equal footing.

k0 DEGENERACY: entropy is identically 0 (one vote has no spread) and inter_rater is
undefined (divides by k(k-1)=0). Those panels are drawn with an explicit note rather
than silently omitted.

BINS. 10 equal-width bins on [0,1], the convention for reliability diagrams and ECE.
This differs from the 5 bins in build_calibration.py, so the header ECE is ECE_10 and
will NOT equal that file's ECE column. Both are kept in the summary.

Writes results/calibration_analysis/<ds>_calibration/<measure>/reliability_<model>.png
   and adds ECE_10 to that folder's calibration_summary.csv
"""
import csv
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402
import numpy as np                                                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
sys.path.insert(0, str(ROOT / "eval" / "llm"))
sys.path.insert(0, str(ROOT / "results" / "utils"))
import uncertainty as U                                              # noqa: E402
from build_calibration import (DATASETS, MEASURES, SOURCES, auroc,   # noqa: E402
                               ceiling, models_for, outdir, parse_cond,
                               per_instance)

LONG = ROOT / "eval" / "data"
NBINS = 10

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#dcdbd6"
CORRECT = "#2a78d6"
WRONG = "#d1495b"

# What the x-axis actually holds, per measure. All three panels say "Confidence"
# because all three plot 1 - normalised u on [0,1], but only the first is a
# probability the model asserted -- the parenthetical keeps that distinction on the
# figure itself rather than only in this docstring.
AXIS_NOTE = {
    "confidence": "stated by the model",
    "entropy": "1 - normalised entropy",
    "inter_rater": "mean pairwise agreement",
}


def ece10(pairs, nbins=NBINS):
    """ECE over `nbins` equal-width confidence bins. pairs = [(confidence, correct)]."""
    if not pairs:
        return None
    N = len(pairs)
    tot = 0.0
    for b in range(nbins):
        lo, hi = b / nbins, (b + 1) / nbins
        sel = [(f, c) for f, c in pairs
               if (lo <= f < hi) or (b == nbins - 1 and f >= hi)]
        if not sel:
            continue
        acc = sum(c for _, c in sel) / len(sel)
        conf = sum(f for f, _ in sel) / len(sel)
        tot += len(sel) / N * abs(acc - conf)
    return tot


def collect(ds, model, gold, measure):
    """-> {skey: (slabel, k, [(confidence, correct)], note)} for every source.

    `confidence` is 1 - u normalised by that measure's ceiling, so all three measures
    land on a common [0,1] axis. note is non-empty when the source cannot support the
    measure at all.
    """
    conds_all = U.conditions(model, ds)
    out = {}
    for skey, slabel, pred in SOURCES:
        conds = {c: v for c, v in conds_all.items() if pred(*parse_cond(c))}
        if not conds:
            continue
        pi = per_instance(conds, gold)
        k = len(conds)
        n_classes = len({lab for lab, _, _, _ in pi.values()})
        ceil = ceiling(measure, k, n_classes)
        vals = [(u[measure], corr) for _, corr, u, _ in pi.values()
                if u[measure] is not None]
        if not vals:
            out[skey] = (slabel, k, [], "undefined at k=1\n(divides by k(k-1)=0)")
            continue
        if ceil == 0:
            out[skey] = (slabel, k, [], "identically 0 at k=1\n(one vote has no spread)")
            continue
        out[skey] = (slabel, k, [(1.0 - u / ceil, c) for u, c in vals], "")
    return out


def plot(ds, model, measure, data, out):
    keys = [k for k, _, _ in SOURCES if k in data]
    fig, axes = plt.subplots(2, len(keys), figsize=(3.5 * len(keys), 6.4))
    fig.patch.set_facecolor(SURFACE)
    if len(keys) == 1:
        axes = axes.reshape(2, 1)
    edges = np.linspace(0, 1, NBINS + 1)
    centers = (edges[:-1] + edges[1:]) / 2
    stats = {}

    for j, skey in enumerate(keys):
        slabel, k, pairs, note = data[skey]
        ax_top, ax_bot = axes[0, j], axes[1, j]

        if note:
            for ax in (ax_top, ax_bot):
                ax.text(0.5, 0.5, note, ha="center", va="center",
                        transform=ax.transAxes, color=INK_2, fontsize=8.5)
            ax_top.set_title(f"{skey}  (k={k})\nDEGENERATE", color=INK_2,
                             fontsize=9.5, fontweight="bold")
            continue

        conf = np.array([f for f, _ in pairs])
        corr = np.array([c for _, c in pairs])
        acc = corr.mean()
        a = auroc([(1.0 - f, c) for f, c in pairs])      # auroc() expects uncertainty
        e = ece10(pairs)
        stats[skey] = (acc, a, e)

        ax_top.hist([conf[corr == 0] * 100, conf[corr == 1] * 100],
                    bins=edges * 100, stacked=True, color=[WRONG, CORRECT],
                    label=["wrong answer", "correct answer"], edgecolor=SURFACE,
                    linewidth=0.4)
        ax_top.set_title(
            f"{skey}  (k={k})\nACC {acc:.2f} / AUROC {a:.2f} / ECE {e:.2f}",
            color=INK, fontsize=9.5, fontweight="bold")
        ax_top.set_xlabel(f"Confidence % ({AXIS_NOTE[measure]})", color=INK_2,
                          fontsize=8.5)
        ax_top.set_xlim(0, 100)
        if j == 0:
            ax_top.set_ylabel("Count", color=INK_2, fontsize=9)
            ax_top.legend(fontsize=7.5, frameon=True, facecolor=SURFACE,
                          edgecolor=GRID)

        idx = np.clip(np.digitize(conf, edges) - 1, 0, NBINS - 1)
        bar_acc = [corr[idx == b].mean() if (idx == b).any() else 0.0
                   for b in range(NBINS)]
        ax_bot.bar(centers, bar_acc, width=1.0 / NBINS * 0.92, color=CORRECT,
                   edgecolor=SURFACE, linewidth=0.5)
        ax_bot.plot([0, 1], [0, 1], color=INK, linestyle="--", linewidth=1.0)
        ax_bot.set_xlabel(f"Confidence ({AXIS_NOTE[measure]})", color=INK_2,
                          fontsize=8.5)
        ax_bot.set_xlim(0, 1)
        ax_bot.set_ylim(0, 1)
        if j == 0:
            ax_bot.set_ylabel("Accuracy Within Bin", color=INK_2, fontsize=9)

    for ax in axes.ravel():
        ax.set_facecolor(SURFACE)
        ax.grid(True, color=GRID, linewidth=0.5, alpha=0.7)
        ax.set_axisbelow(True)
        for s in ax.spines:
            ax.spines[s].set_color(GRID)
        ax.tick_params(colors=INK_2, labelsize=8, length=0)

    kind = ("stated confidence" if measure == "confidence"
            else f"1 - normalised {measure} (consistency, NOT an asserted probability)")
    fig.suptitle(f"{ds} · {model} · {measure} — distribution and reliability\n{kind}",
                 color=INK, fontsize=11.5, fontweight="bold", x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return stats


def main(ds, models):
    gold = {r["task"]: r["true_label"]
            for r in csv.DictReader(open(LONG / f"{ds}_gold.csv"))}
    got = {}
    for measure in MEASURES:
        d = outdir(ds) / measure
        d.mkdir(parents=True, exist_ok=True)
        for model in models:
            data = collect(ds, model, gold, measure)
            if not data:
                print(f"  {model}: no conditions, skipped")
                continue
            stats = plot(ds, model, measure, data, d / f"reliability_{model}.png")
            for skey, (acc, a, e) in stats.items():
                got[(model, skey, measure)] = e
            done = " ".join(f"{s}:ECE10={v[2]:.3f}" for s, v in stats.items())
            print(f"    {measure:12s} {model:26s} {done}")

    f = outdir(ds) / "calibration_summary.csv"
    if f.exists() and got:
        rows = list(csv.DictReader(open(f)))
        cols = list(rows[0])
        if "ECE_10" not in cols:
            cols.insert(cols.index("ECE") + 1, "ECE_10")
        for r in rows:
            e = got.get((r["model"], r["source"], r["measure"]))
            r["ECE_10"] = f"{e:.4f}" if e is not None else ""
        with open(f, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(f"  -> {f.relative_to(ROOT)}  (ECE_10 for all three measures)")


if __name__ == "__main__":
    a = sys.argv[1:]
    todo = [a[0]] if a else DATASETS
    for _ds in todo:
        print(f"\n########## {_ds} ##########")
        main(_ds, a[1:] or models_for(_ds))

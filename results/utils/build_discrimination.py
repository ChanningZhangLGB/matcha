#!/usr/bin/env python3
"""Discrimination: can this uncertainty measure SEPARATE correct from wrong answers?

    python results/utils/build_discrimination.py [dataset] [model ...]

The companion to build_reliability.py, and the fair way to compare the three measures.
A reliability diagram asks whether a number is on the right SCALE, which only makes
sense for a probability the model asserted. This asks only whether the number ORDERS
instances correctly -- scale-free, so stated confidence, entropy and inter-rater
agreement are judged on equal terms.

Per dataset x model x measure, a 2x4 figure (columns = sources k0..k3):

    row 1  ROC CURVE            using LOW uncertainty to predict CORRECT. The
                                diagonal is chance. Ties are plotted as the sloped
                                segments they are, rather than being broken
                                arbitrarily -- 60-80% of instances share u=0 on some
                                datasets, and a tie-breaking implementation would draw
                                a curve far above the honest one.
    row 2  RISK-COVERAGE CURVE  keep the c% LEAST uncertain instances, plot accuracy
                                on that retained subset. This IS the routing question:
                                at coverage c the model annotates c% and the remaining
                                (100-c)% go to humans, so the curve reads directly as
                                "how good is what the model keeps". The dashed line is
                                full-coverage accuracy; a measure with no signal is
                                flat along it.

AURC (area under the risk-coverage curve, on accuracy) is reported alongside AUROC.
AUROC judges ranking over the whole range; AURC weights the high-confidence head,
which is where routing actually operates, so the two can disagree and both are given.

Writes results/calibration_analysis/<ds>_calibration/<measure>/discrimination_<model>.png
   and a per-dataset discrimination_summary.csv
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
                               models_for, outdir, parse_cond, per_instance)

LONG = ROOT / "eval" / "data"

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#dcdbd6"
LINE = "#2a78d6"
REF = "#d1495b"


def roc_points(pairs):
    """-> (fpr, tpr) walking thresholds over -u. pairs = [(u, correct)].

    Instances tied at the same u are consumed in ONE step, which is what produces the
    straight diagonal segments across a tied block. Splitting them would imply an
    ordering the measure does not provide.
    """
    P = sum(c for _, c in pairs)
    N = len(pairs) - P
    if P == 0 or N == 0:
        return None, None
    order = sorted(pairs, key=lambda uc: uc[0])          # least uncertain first
    fpr, tpr = [0.0], [0.0]
    tp = fp = 0
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and order[j + 1][0] == order[i][0]:
            j += 1
        block = order[i:j + 1]
        tp += sum(c for _, c in block)
        fp += sum(1 - c for _, c in block)
        fpr.append(fp / N)
        tpr.append(tp / P)
        i = j + 1
    return np.array(fpr), np.array(tpr)


def risk_coverage(pairs):
    """-> (coverage, accuracy_on_retained). Keeps the least-uncertain first.

    Ties are consumed as whole blocks for the same reason as roc_points: within a tied
    block the measure expresses no preference, so no intermediate coverage is defined.
    """
    order = sorted(pairs, key=lambda uc: uc[0])
    n = len(order)
    cov, acc = [], []
    correct = 0
    i = 0
    while i < n:
        j = i
        while j + 1 < n and order[j + 1][0] == order[i][0]:
            j += 1
        correct += sum(c for _, c in order[i:j + 1])
        cov.append((j + 1) / n)
        acc.append(correct / (j + 1))
        i = j + 1
    return np.array(cov), np.array(acc)


def aurc(cov, acc):
    """Area under the risk-coverage curve, trapezoid over coverage in [0,1]."""
    if len(cov) < 2:
        return float(acc[0]) if len(acc) else float("nan")
    c = np.concatenate([[0.0], cov])
    a = np.concatenate([[acc[0]], acc])
    return float(np.trapezoid(a, c)) if hasattr(np, "trapezoid") else float(np.trapz(a, c))


def collect(ds, model, gold, measure):
    conds_all = U.conditions(model, ds)
    out = {}
    for skey, slabel, pred in SOURCES:
        conds = {c: v for c, v in conds_all.items() if pred(*parse_cond(c))}
        if not conds:
            continue
        pi = per_instance(conds, gold)
        vals = [(u[measure], corr) for _, corr, u, _ in pi.values()
                if u[measure] is not None]
        note = ""
        if not vals:
            note = "undefined at k=1\n(divides by k(k-1)=0)"
        elif len({v for v, _ in vals}) == 1:
            note = "no discrimination\n(every instance tied)"
        out[skey] = (slabel, len(conds), vals, note)
    return out


def plot(ds, model, measure, data, out):
    keys = [k for k, _, _ in SOURCES if k in data]
    fig, axes = plt.subplots(2, len(keys), figsize=(3.5 * len(keys), 6.4))
    fig.patch.set_facecolor(SURFACE)
    stats = {}

    for j, skey in enumerate(keys):
        slabel, k, pairs, note = data[skey]
        ax_top, ax_bot = axes[0, j], axes[1, j]
        ax_top.plot([0, 1], [0, 1], color=INK, linestyle="--", linewidth=1.0)

        if note:
            for ax in (ax_top, ax_bot):
                ax.text(0.5, 0.5, note, ha="center", va="center",
                        transform=ax.transAxes, color=INK_2, fontsize=8.5)
            ax_top.set_title(f"{skey}  (k={k})", color=INK_2, fontsize=9.5,
                             fontweight="bold")
        else:
            a = auroc(pairs)
            fpr, tpr = roc_points(pairs)
            cov, acc = risk_coverage(pairs)
            r = aurc(cov, acc)
            full = float(np.mean([c for _, c in pairs]))
            stats[skey] = (a, r, full)

            # markers matter here: a coarse measure yields only 3-4 tied blocks, and
            # an unmarked line through them reads as a smooth curve rather than as
            # the handful of discrete steps it actually is
            mk = dict(marker="o", markersize=3.2) if len(fpr) <= 25 else {}
            ax_top.plot(fpr, tpr, color=LINE, linewidth=1.8, **mk)
            ax_top.fill_between(fpr, tpr, alpha=0.12, color=LINE)
            ax_top.set_title(f"{skey}  (k={k})\nAUROC {a:.3f} / AURC {r:.3f}",
                             color=INK, fontsize=9.5, fontweight="bold")
            ax_top.set_xlabel("false positive rate", color=INK_2, fontsize=8.5)

            mk2 = dict(marker="o", markersize=3.6) if len(cov) <= 25 else {}
            ax_bot.plot(cov * 100, acc, color=LINE, linewidth=1.8, **mk2)
            ax_bot.axhline(full, color=REF, linestyle="--", linewidth=1.2)
            ax_bot.text(2, full, f" full coverage {full:.3f}", color=REF, fontsize=7.5,
                        va="bottom")
            ax_bot.set_xlabel(f"coverage % (kept by the model)   ·   {len(cov)} step(s)",
                              color=INK_2, fontsize=8.5)
            ax_bot.set_xlim(0, 100)

        ax_top.set_xlim(0, 1)
        ax_top.set_ylim(0, 1)
        if j == 0:
            ax_top.set_ylabel("true positive rate", color=INK_2, fontsize=9)
            ax_bot.set_ylabel("accuracy on retained", color=INK_2, fontsize=9)

    for ax in axes.ravel():
        ax.set_facecolor(SURFACE)
        ax.grid(True, color=GRID, linewidth=0.5, alpha=0.7)
        ax.set_axisbelow(True)
        for s in ax.spines:
            ax.spines[s].set_color(GRID)
        ax.tick_params(colors=INK_2, labelsize=8, length=0)

    fig.suptitle(f"{ds} · {model} · {measure} — discrimination\n"
                 "ROC (top) and risk-coverage (bottom); scale-free, so the three "
                 "measures are directly comparable",
                 color=INK, fontsize=11.5, fontweight="bold", x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return stats


def main(ds, models):
    gold = {r["task"]: r["true_label"]
            for r in csv.DictReader(open(LONG / f"{ds}_gold.csv"))}
    rows = []
    for measure in MEASURES:
        d = outdir(ds) / measure
        d.mkdir(parents=True, exist_ok=True)
        for model in models:
            data = collect(ds, model, gold, measure)
            if not data:
                continue
            stats = plot(ds, model, measure, data,
                         d / f"discrimination_{model}.png")
            for skey, (a, r, full) in stats.items():
                rows.append({"dataset": ds, "model": model, "measure": measure,
                             "source": skey, "AUROC": f"{a:.4f}",
                             "AURC": f"{r:.4f}", "full_coverage_acc": f"{full:.4f}",
                             "AURC_gain": f"{r - full:+.4f}"})
            done = " ".join(f"{s}:{v[0]:.3f}/{v[1]:.3f}" for s, v in stats.items())
            print(f"    {measure:12s} {model:26s} {done}")

    if rows:
        f = outdir(ds) / "discrimination_summary.csv"
        with open(f, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"  -> {f.relative_to(ROOT)}  ({len(rows)} rows)")


if __name__ == "__main__":
    a = sys.argv[1:]
    todo = [a[0]] if a else DATASETS
    for _ds in todo:
        print(f"\n########## {_ds} ##########")
        main(_ds, a[1:] or models_for(_ds))

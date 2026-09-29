#!/usr/bin/env python3
"""CDF of the three uncertainty measures, one figure per dataset.

    python results/plot_uncertainty_cdf.py gpt-4o-mini

Reads results/<dataset>/<model>_uncertainty_per_instance.csv and writes
results/<dataset>/<model>_uncertainty_cdf.png -- three subplots, one per measure.

A CDF is the right form here: the question is "what share of instances sit below
uncertainty u", which is a distribution-shape question, not a magnitude comparison.
Reading it: a curve that shoots up at the left = most instances are certain; a long
right tail = a meaningful minority the model is unsure about; a step is the discrete
lattice these measures live on (k conditions give only k+1 distinct agreement values).
"""
import csv
import math
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
DATASETS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
            "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"]

# reference palette, light mode
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
SERIES = "#2a78d6"          # categorical slot 1
GRID = "#dcdbd6"

def ddir(ds):
    """Output dir for a dataset. movie_reviews is scored under TWO framings, so its
    categorical artefacts live in movie_reviews/categorical/ and the continuous ones
    in movie_reviews/regression/."""
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def mdir(ds, model, base=None):
    """Per-model output dir: <dataset>/model_analysis/<model>/ (created on demand)."""
    d = (base or ddir(ds)) / "model_analysis" / model
    d.mkdir(parents=True, exist_ok=True)
    return d



MEASURES = [
    ("u_confidence", "1. Confidence",
     r"$u_i = 1 - \frac{1}{k}\sum_j P(a_{ij}|p_{ij})$"),
    ("u_entropy", "2. Entropy",
     r"$u_i = -\sum_l f_l \ln f_l$"),
    ("u_agreement", "3. Inter-rater",
     r"$u_i = 1 - \mathrm{pairwise\ agreement}$"),
]


def cdf(vals):
    v = np.sort(np.asarray(vals, dtype=float))
    y = np.arange(1, len(v) + 1) / len(v)
    return v, y


def main(model):
    for ds in DATASETS:
        f = ddir(ds) / "model_analysis" / model / "uncertainty_per_instance.csv"
        if not f.exists():
            continue
        rows = list(csv.DictReader(open(f)))
        ks = [int(r["k_conditions"]) for r in rows]
        kmin, kmax = min(ks), max(ks)
        # k varies per instance when some conditions failed on that instance
        # (conll_ner especially); reporting rows[0] alone would be misleading
        kdesc = (f"{kmax} prompt conditions" if kmin == kmax else
                 f"up to {kmax} prompt conditions (median "
                 f"{sorted(ks)[len(ks)//2]}, min {kmin})")

        fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.4))
        fig.patch.set_facecolor(SURFACE)

        for ax, (col, title, formula) in zip(axes, MEASURES):
            vals = [float(r[col]) for r in rows if r[col] not in ("", None)]
            ax.set_facecolor(SURFACE)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
            for s in ("left", "bottom"):
                ax.spines[s].set_color(GRID)
            ax.grid(True, color=GRID, linewidth=0.6, alpha=0.9)
            ax.set_axisbelow(True)
            ax.tick_params(colors=INK_2, labelsize=9, length=0)

            if not vals:
                ax.text(0.5, 0.5, "no data", ha="center", va="center",
                        color=INK_2, transform=ax.transAxes)
                ax.set_title(title, color=INK, fontsize=11, fontweight="bold",
                             loc="left", pad=8)
                continue

            x, y = cdf(vals)
            ax.step(x, y, where="post", color=SERIES, linewidth=2.0,
                    solid_capstyle="round")
            ax.fill_between(x, y, step="post", color=SERIES, alpha=0.10, linewidth=0)

            med = float(np.median(vals))
            mean = float(np.mean(vals))
            ax.axvline(med, color=INK_2, linewidth=1.0, linestyle=(0, (4, 3)), alpha=0.8)
            ax.annotate(f"median {med:.3f}\nmean {mean:.3f}",
                        xy=(med, 0.5), xytext=(6, -34), textcoords="offset points",
                        color=INK_2, fontsize=8.5, va="center")

            hi = max(x.max(), 1e-6)
            ax.set_xlim(-0.02 * hi, hi * 1.06)
            ax.set_ylim(0, 1.02)
            ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
            ax.set_title(title, color=INK, fontsize=11, fontweight="bold", loc="left",
                         pad=8)
            # formula goes under the axis: putting it above collided with the title
            ax.set_xlabel(f"uncertainty $u_i$\n{formula}", color=INK_2, fontsize=9,
                          linespacing=1.9)

        axes[0].set_ylabel("cumulative share of instances", color=INK_2, fontsize=9.5)
        fig.suptitle(f"{ds} — {model}: uncertainty across {kdesc} "
                     f"({len(rows):,} instances)",
                     color=INK, fontsize=12.5, fontweight="bold", x=0.008, ha="left",
                     y=0.985)
        fig.tight_layout(rect=(0, 0, 1, 0.94))
        out = mdir(ds, model) / "uncertainty_cdf.png"
        fig.savefig(out, dpi=200, facecolor=SURFACE)
        plt.close(fig)
        print(f"  {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

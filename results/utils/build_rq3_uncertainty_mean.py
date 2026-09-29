#!/usr/bin/env python3
"""RQ3: mean uncertainty per dataset under each measure, one figure per model.

    python results/utils/build_rq3_uncertainty_mean.py

Five figures, one per annotator model, each showing the mean of the three uncertainty
measures across that model's datasets.

ENTROPY IS NORMALISED. Confidence and inter-rater agreement are already on [0,1], but
Shannon entropy over m conditions runs to ln(min(m, |Y|)), which is 2.20 at m=9 and
varies with the label space. Plotting it raw would make entropy look larger than the
other two for reasons of scale rather than of substance, so it is divided by its own
ceiling, the same normalisation build_calibration.py uses when binning.

Writes results/RQ3/uncertainty_mean/<model>.{pdf,png} and uncertainty_mean.csv
"""
import csv
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402
import numpy as np                                                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ3" / "uncertainty_mean"

TEXT = ["sentiment", "movie_reviews", "crowdtruth_pooled", "conll_ner_5k",
        "pico_5k", "quiz"]
IMAGE = ["labelme", "imagenet16h"]
DISP = {"sentiment": "Sentiment", "movie_reviews": "MovieRev.",
        "crowdtruth_pooled": "CrowdTruth", "conll_ner_5k": "CoNLL-03",
        "pico_5k": "PICO", "quiz": "QUIZ", "labelme": "LabelMe",
        "imagenet16h": "ImageNet-16H"}
MODELS = [("gpt-4o-mini", "GPT-4o-mini", TEXT + IMAGE),
          ("llama3.1-8b-instruct-q8_0", "Llama3.1-8B", TEXT),
          ("qwen2.5-7b-instruct-q8_0", "Qwen2.5-7B", TEXT),
          ("minicpm-v-8b-2.6-q8_0", "MiniCPM-V-8B", IMAGE),
          ("qwen2.5vl-7b-q8_0", "Qwen2.5VL-7B", IMAGE)]
# same palette as the RQ3 ablation bars, so the two figures read as one family
MEAS = [("u_confidence", "Self-Evaluation", "#BBD9EC", "\\\\\\"),
        ("u_entropy", "Entropy", "#FBD9A9", "xxx"),
        ("u_agreement", "Inter-rater agr.", "#BEE3D3", "///")]
INK, GRID = "#111111", "#d8d8d8"


def ddir(ds):
    return RES / ds / "categorical" if ds == "movie_reviews" else RES / ds


def means(ds, model):
    f = ddir(ds) / "model_analysis" / model / "uncertainty_per_instance.csv"
    if not f.exists():
        return None
    rows = list(csv.DictReader(open(f)))
    k = max(int(r["k_conditions"]) for r in rows if r.get("k_conditions"))
    n_cls = len({r["llm_label"] for r in rows if r["llm_label"]})
    ceil = math.log(min(k, n_cls)) if min(k, n_cls) > 1 else 1.0
    out = {}
    for col, _lab, _c, _h in MEAS:
        v = [float(r[col]) for r in rows if r.get(col) not in (None, "")]
        if not v:
            continue
        out[col] = (sum(v) / len(v) / ceil) if col == "u_entropy" \
            else sum(v) / len(v)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 6.6, "hatch.linewidth": 0.45})
    table = [["model", "dataset"] + [m[1] for m in MEAS]]
    for mkey, mdisp, dss in MODELS:
        vals = {ds: means(ds, mkey) for ds in dss}
        vals = {d: v for d, v in vals.items() if v}
        if not vals:
            continue
        order = [d for d in dss if d in vals]
        fig, ax = plt.subplots(figsize=(3.4 if len(order) <= 2 else 5.0, 1.9))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")
        ax.grid(True, axis="y", color=GRID, linewidth=0.4, linestyle=(0, (1, 2)),
                zorder=0)
        ax.set_axisbelow(True)
        for sp in ax.spines.values():
            sp.set_color(INK); sp.set_linewidth(0.55)
        ax.tick_params(colors=INK, labelsize=5.8, length=1.8, width=0.5, pad=1.4)
        xs = np.arange(len(order))
        w = 0.26
        for j, (col, lab, colr, hat) in enumerate(MEAS):
            ys = [vals[d].get(col, np.nan) for d in order]
            ax.bar(xs + (j - 1) * w, ys, width=w, color=colr, hatch=hat,
                   edgecolor=INK, linewidth=0.45, zorder=3, label=lab)
        for d in order:
            table.append([mdisp, DISP[d]]
                         + [f"{vals[d].get(c, float('nan')):.4f}" for c, _, _, _ in MEAS])
        ax.set_xticks(xs)
        ax.set_xticklabels([DISP[d] for d in order], fontsize=5.6,
                           rotation=0 if len(order) <= 2 else 24,
                           ha="center" if len(order) <= 2 else "right")
        ax.set_ylabel("Mean uncertainty", fontsize=6.3, color=INK, labelpad=2)
        ax.set_ylim(0, max(0.55, max(v for d in order for v in vals[d].values()) * 1.35))
        leg = ax.legend(fontsize=5.4, frameon=False, ncol=3, loc="upper center",
                        handlelength=1.5, columnspacing=1.2, handletextpad=0.4,
                        borderpad=0.1)
        for t in leg.get_texts():
            t.set_color(INK)
        for ext in ("pdf", "png"):
            fig.savefig(OUT / f"{mdisp}.{ext}", dpi=600, facecolor="white",
                        bbox_inches="tight", pad_inches=0.03)
        plt.close(fig)
        print(f"  {mdisp}: {len(order)} datasets")
    with open(OUT / "uncertainty_mean.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(table)
    print(f"\n  {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()

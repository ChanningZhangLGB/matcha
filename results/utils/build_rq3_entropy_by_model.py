#!/usr/bin/env python3
"""RQ3: mean Entropy uncertainty per dataset, compared across annotator models.

    python results/utils/build_rq3_entropy_by_model.py

One panel, eight datasets, three bars each: the models that annotated that corpus. Text
datasets carry GPT-4o-mini with the two open-weight text models, image datasets carry
GPT-4o-mini with the two vision models, so GPT-4o-mini is the common reference across
the whole figure.

Entropy is divided by its ceiling ln(min(m, |Y|)) so that datasets with different label
spaces are comparable: raw entropy runs to 2.20 at m=9 for a large label space and to
0.69 for a binary one, which would make the 16-way image task look uncertain purely
because it has more classes to spread over.

A low bar means the prompting conditions mostly agree, which is not the same as the
model being right. It means the ranking has little to work with: see
uncertainty_distribution for the share of instances tied at exactly zero.

Writes results/RQ3/entropy_by_model.{pdf,png}
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
OUT = RES / "RQ3"

TEXT = ["sentiment", "movie_reviews", "crowdtruth_pooled", "conll_ner_5k",
        "pico_5k", "quiz"]
IMAGE = ["labelme", "imagenet16h"]
DISP = {"sentiment": "Sentiment", "movie_reviews": "MovieRev.",
        "crowdtruth_pooled": "CrowdTruth", "conll_ner_5k": "CoNLL-03",
        "pico_5k": "PICO", "quiz": "QUIZ", "labelme": "LabelMe",
        "imagenet16h": "ImageNet-16H"}
TM = [("gpt-4o-mini", "GPT-4o-mini"),
      ("llama3.1-8b-instruct-q8_0", "Llama3.1-8B"),
      ("qwen2.5-7b-instruct-q8_0", "Qwen2.5-7B")]
IM = [("gpt-4o-mini", "GPT-4o-mini"),
      ("minicpm-v-8b-2.6-q8_0", "MiniCPM-V-8B"),
      ("qwen2.5vl-7b-q8_0", "Qwen2.5VL-7B")]
COL = {"GPT-4o-mini": "#4169E1", "Llama3.1-8B": "#E8483F", "Qwen2.5-7B": "#7B3294",
       "MiniCPM-V-8B": "#6FC276", "Qwen2.5VL-7B": "#C2185B"}
HATCH = {"GPT-4o-mini": "///", "Llama3.1-8B": "xxx", "Qwen2.5-7B": "\\\\\\",
         "MiniCPM-V-8B": "...", "Qwen2.5VL-7B": "++"}
INK, GRID = "#111111", "#d8d8d8"


def ddir(ds):
    return RES / ds / "categorical" if ds == "movie_reviews" else RES / ds


def mean_entropy(ds, model):
    f = ddir(ds) / "model_analysis" / model / "uncertainty_per_instance.csv"
    if not f.exists():
        return None
    rows = list(csv.DictReader(open(f)))
    v = [float(r["u_entropy"]) for r in rows if r.get("u_entropy") not in (None, "")]
    if not v:
        return None
    k = max(int(r["k_conditions"]) for r in rows if r.get("k_conditions"))
    n_cls = len({r["llm_label"] for r in rows if r["llm_label"]})
    ceil = math.log(min(k, n_cls)) if min(k, n_cls) > 1 else 1.0
    return sum(v) / len(v) / ceil


def main():
    plt.rcParams.update({"font.size": 6.6, "hatch.linewidth": 0.45})
    order = TEXT + IMAGE
    fig, ax = plt.subplots(figsize=(7.0, 2.0))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(True, axis="y", color=GRID, linewidth=0.4, linestyle=(0, (1, 2)), zorder=0)
    ax.set_axisbelow(True)
    for sp in ax.spines.values():
        sp.set_color(INK); sp.set_linewidth(0.55)
    ax.tick_params(colors=INK, labelsize=5.8, length=1.8, width=0.5, pad=1.4)

    rows_out = [["dataset", "model", "mean_entropy_norm"]]
    seen, w = set(), 0.26
    for i, ds in enumerate(order):
        for j, (mkey, mdisp) in enumerate(TM if ds in TEXT else IM):
            v = mean_entropy(ds, mkey)
            if v is None:
                continue
            ax.bar(i + (j - 1) * w, v, width=w, color=COL[mdisp], hatch=HATCH[mdisp],
                   edgecolor=INK, linewidth=0.45, zorder=3,
                   label=mdisp if mdisp not in seen else None)
            seen.add(mdisp)
            rows_out.append([DISP[ds], mdisp, f"{v:.4f}"])
    ax.set_xticks(np.arange(len(order)))
    ax.set_xticklabels([DISP[d] for d in order], fontsize=5.8, rotation=22, ha="right")
    ax.set_ylabel("Mean Entropy (normalised)", fontsize=6.3, color=INK, labelpad=2)
    ax.set_xlim(-0.6, len(order) - 0.4)
    leg = ax.legend(fontsize=5.5, frameon=False, ncol=5, loc="upper center",
                    bbox_to_anchor=(0.5, 1.16), handlelength=1.5, columnspacing=1.3,
                    handletextpad=0.4)
    for t in leg.get_texts():
        t.set_color(INK)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"entropy_by_model.{ext}", dpi=600, facecolor="white",
                    bbox_inches="tight", pad_inches=0.03)
    with open(OUT / "entropy_by_model.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows_out)
    print(f"  {(OUT / 'entropy_by_model.png').relative_to(ROOT)}  "
          f"({len(rows_out) - 1} bars)")


if __name__ == "__main__":
    main()

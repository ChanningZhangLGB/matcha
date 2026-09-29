#!/usr/bin/env python3
"""RQ3 (a): how much does the UNCERTAINTY BASIS contribute?

    python results/utils/build_rq3_uncertainty.py

Grouped bars -- one block per dataset, four bars per block:

    confidence / entropy / inter_rater / random

Each bar is that measure's PEAK accuracy, maximised over aggregator x budget x route
(h-human vs h-human_llm), so every other MATCHA component is held at its best and the
only thing varying within a block is which signal ranked the instances.

`random` is the CONTROL, not a fourth method: its ranking is a seeded shuffle, so it
measures what the same machinery achieves with no uncertainty signal at all. A bar at or
below the grey one contributed nothing.

FIGURE LAYOUT -- three figures, each a text panel beside an image panel:

    gpt-4o-mini    text: 6 datasets | image: 2      (one model, both arms)
    llama3.1-8b + minicpm-v-8b                      (the two 8B-class open models)
    qwen2.5-7b  + qwen2.5vl-7b                      (the two Qwen models)

The arms are drawn as SEPARATE PANELS rather than one 8-block row because, except for
gpt-4o-mini, the two halves are different models -- a shared axis would invite reading
across a boundary where the annotator silently changes. Panels share a y-axis so bar
heights stay comparable, and the width ratio matches the dataset counts so bar widths
come out equal across panels.

SIGNIFICANCE brackets come from build_rq3_significance.py: two-sided Wilcoxon
signed-rank on paired cells (same aggregator, route and budget), Holm-corrected. Most
p-values land in the top tier because those cells are non-independent, NOT because the
effects are overwhelming. ONLY SIGNIFICANT GAINS ARE MARKED: a measure that ties the
control or loses to it is left unannotated, so an absent bracket is not a claim. The
full verdict for every cell, including the ten that are significantly WORSE than random,
is in significance_vs_random.csv; take effect size from median_diff / win_rate there.

Writes results/RQ3/uncertainty/uncertainty_<tag>.{pdf,png} and uncertainty_peaks.csv
"""
import csv
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                      # noqa: E402
import numpy as np                                                   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ3" / "uncertainty"

MEASURES = ["confidence", "entropy", "inter_rater", "random"]
LABEL = {"confidence": "Confidence", "entropy": "Entropy",
         "inter_rater": "Inter-rater agr.", "random": "Random (control)"}
COLOR = {"confidence": "#BBD9EC", "entropy": "#FBD9A9",
         "inter_rater": "#BEE3D3", "random": "#E2E2E2"}
HATCH = {"confidence": "\\\\\\", "entropy": "xxx", "inter_rater": "///",
         "random": "..."}
ROUTES = {"h-human": "human_only", "h-human_llm": "human_plus_llm"}
# Display names as they appear in the model-profile table and every other figure.
SHORT = {"gpt-4o-mini": "GPT-4o-mini", "llama3.1-8b-instruct-q8_0": "Llama3.1-8B",
         "qwen2.5-7b-instruct-q8_0": "Qwen2.5-7B",
         "minicpm-v-8b-2.6-q8_0": "MiniCPM-V-8B", "qwen2.5vl-7b-q8_0": "Qwen2.5VL-7B"}
# significance_vs_random.csv is keyed by these short lowercase forms, independent of the
# display names above -- do not conflate the two.
SIG_KEY = {"gpt-4o-mini": "gpt-4o-mini", "llama3.1-8b-instruct-q8_0": "llama3.1-8b",
           "qwen2.5-7b-instruct-q8_0": "qwen2.5-7b",
           "minicpm-v-8b-2.6-q8_0": "minicpm-v-8b", "qwen2.5vl-7b-q8_0": "qwen2.5vl-7b"}

TEXT_DS = [("sentiment", "sentiment"), ("movie_reviews", "movie_reviews"),
           ("crowdtruth", "crowdtruth_pooled"), ("conll_ner_5k", "conll_ner_5k"),
           ("pico_5k", "pico_5k"), ("quiz", "quiz")]
IMAGE_DS = [("labelme", "labelme"), ("imagenet16h", "imagenet16h")]
# Tick-label rename ONLY. The first element of each TEXT_DS/IMAGE_DS pair above is also
# the dict key used to join against significance_vs_random.csv (keyed by the raw table
# name) -- do not rename it there, or the join silently drops every bracket, as
# renaming SHORT to the display form did to the model join above.
# Two-word names wrap so the label can sit horizontally and centred under its bar block
# without running into the neighbouring one.
DISPLAY = {"sentiment": "Sentiment\nPolarity", "movie_reviews": "MovieReviews",
           "crowdtruth": "CrowdTruth\nRelEx", "conll_ner_5k": "CoNLL-NER",
           "pico_5k": "PICO", "quiz": "QUIZ", "labelme": "LabelMe",
           "imagenet16h": "ImageNet-16H"}

FIGURES = [("gpt-4o-mini", "gpt-4o-mini", "gpt-4o-mini"),
           ("llama-minicpm", "llama3.1-8b-instruct-q8_0", "minicpm-v-8b-2.6-q8_0"),
           ("qwen-qwenvl", "qwen2.5-7b-instruct-q8_0", "qwen2.5vl-7b-q8_0")]


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def peak(table, model, measure):
    best = None
    for folder, route in ROUTES.items():
        f = ddir(table) / "allocation" / model / measure / route / "routing.csv"
        if not f.exists():
            continue
        for r in csv.DictReader(open(f)):
            v = float(r["accuracy"])
            if best is None or v > best[0]:
                best = (v, folder, r["method"], r["X"])
    return best


def significance(model):
    f = OUT / "significance_vs_random.csv"
    if not f.exists():
        return {}
    return {(r["dataset"], r["measure"]): (r["sig_holm_0.05"], r["p_holm"])
            for r in csv.DictReader(open(f)) if r["model"] == SIG_KEY.get(model, model)}


def stars(p):
    """Marker for a significant gain over random. Returns "" below threshold: only
    measures that beat the control are annotated, so a bare bar carries no claim
    either way and the eye is drawn to the gains rather than to the absences."""
    try:
        v = float(p)
    except (TypeError, ValueError):
        return ""
    return "***" if v < 1e-3 else "**" if v < 1e-2 else "*" if v < 0.05 else ""


def collect(dss, model):
    out = {}
    for disp, table in dss:
        for me in MEASURES:
            g = peak(table, model, me)
            if g:
                out[(disp, me)] = g
    return out


def draw(ax, dss, model, data, sig, lo, hi, w=0.20):
    blocks = [d for d, _ in dss if (d, "confidence") in data]
    xs = np.arange(len(blocks))
    span = hi - lo
    floor = lo - span * 0.12
    for i, me in enumerate(MEASURES):
        vals = [data[(b, me)][0] if (b, me) in data else np.nan for b in blocks]
        ax.bar(xs + (i - 1.5) * w, [v - floor for v in vals], width=w, bottom=floor,
               color=COLOR[me], label=LABEL[me], zorder=3, hatch=HATCH[me],
               edgecolor="#111111", linewidth=0.45)
    for j, b in enumerate(blocks):
        top = max(data[(b, m)][0] for m in MEASURES if (b, m) in data)
        for lvl, me in enumerate(m for m in MEASURES if m != "random"):
            if (b, me) not in sig or (b, me) not in data:
                continue
            verdict, p = sig[(b, me)]
            # Only gains are marked. A measure that ties the control, or loses to it,
            # is left unannotated rather than labelled: the figure reports where the
            # ranking helps, and the CSV carries the full verdict for every cell.
            if verdict != "yes" or not stars(p):
                continue
            x0 = xs[j] + (MEASURES.index(me) - 1.5) * w
            x1 = xs[j] + (MEASURES.index("random") - 1.5) * w
            y = top + span * (0.05 + 0.072 * lvl)
            h = span * 0.014
            col = "#111111"
            ax.plot([x0, x0, x1, x1], [y, y + h, y + h, y], color=col,
                    linewidth=0.42, zorder=8, solid_joinstyle="miter")
            ax.annotate(stars(p), xy=((x0 + x1) / 2, y + h), xytext=(0, 0.2),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=3.5, color=col, zorder=9)
    ax.set_xticks(xs)
    # Horizontal and centred under each bar block. The long names are wrapped in
    # DISPLAY rather than angled, so a label stays visually tied to the group it
    # belongs to instead of trailing off toward the neighbouring one.
    ax.set_xticklabels([DISPLAY.get(b, b) for b in blocks], fontsize=5.6,
                       rotation=0, ha="center")
    ax.set_xlim(-0.55, len(blocks) - 0.45)
    return floor


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams["hatch.linewidth"] = 0.45
    rows = [["figure", "arm", "dataset", "model", "uncertainty", "best_accuracy",
             "route", "method", "X", "gain_vs_random"]]

    for tag, tmodel, imodel in FIGURES:
        td, idd = collect(TEXT_DS, tmodel), collect(IMAGE_DS, imodel)
        if not td and not idd:
            print(f"  {tag}: no data")
            continue
        allv = [v[0] for v in list(td.values()) + list(idd.values())]
        lo, hi = min(allv), max(allv)

        fig, axes = plt.subplots(
            1, 2, figsize=(7.0, 2.45), sharey=True,
            gridspec_kw={"width_ratios": [len(TEXT_DS), len(IMAGE_DS)],
                         "wspace": 0.05})
        fig.patch.set_facecolor("white")
        for ax in axes:
            ax.set_facecolor("white")
            ax.grid(True, axis="y", color="#d8d8d8", linewidth=0.35,
                    linestyle=(0, (1, 1.8)), zorder=0)
            ax.set_axisbelow(True)
            for sp in ax.spines.values():
                sp.set_color("#111111")
                sp.set_linewidth(0.55)
            ax.tick_params(colors="#111111", labelsize=5.8, length=1.8, width=0.45,
                           pad=1.4)

        floor = draw(axes[0], TEXT_DS, tmodel, td, significance(tmodel), lo, hi)
        draw(axes[1], IMAGE_DS, imodel, idd, significance(imodel), lo, hi)
        axes[0].set_ylim(floor, hi + (hi - lo) * 0.44)
        axes[0].yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda v, _: f"{v * 100:.0f}"))
        axes[0].set_ylabel("Best accuracy (%)", color="#111111", fontsize=6.8,
                           labelpad=2)
        axes[1].tick_params(axis="y", left=False)
        axes[0].set_title(f"Text  ·  {SHORT[tmodel]}", fontsize=6.6,
                          fontweight="bold", color="#111111", pad=3)
        axes[1].set_title(f"Image  ·  {SHORT[imodel]}", fontsize=6.6,
                          fontweight="bold", color="#111111", pad=3)

        h, l = axes[0].get_legend_handles_labels()
        leg = fig.legend(h, l, fontsize=5.6, frameon=False, ncol=4,
                         loc="upper center", bbox_to_anchor=(0.5, 1.07),
                         handlelength=1.5, columnspacing=1.6, handletextpad=0.45)
        for t in leg.get_texts():
            t.set_color("#111111")

        for ext in ("pdf", "png"):
            fig.savefig(OUT / f"uncertainty_{tag}.{ext}", dpi=600, facecolor="white",
                        bbox_inches="tight", pad_inches=0.02)
        plt.close(fig)

        for arm, dss, mdl, dat in (("text", TEXT_DS, tmodel, td),
                                   ("image", IMAGE_DS, imodel, idd)):
            for disp, _ in dss:
                rnd = dat.get((disp, "random"))
                for me in MEASURES:
                    g = dat.get((disp, me))
                    if not g:
                        continue
                    rows.append([tag, arm, disp, SHORT[mdl], me, f"{g[0]:.4f}",
                                 g[1], g[2], g[3],
                                 f"{g[0] - rnd[0]:+.4f}" if rnd else ""])
        print(f"  uncertainty_{tag}.pdf/.png   text={SHORT[tmodel]}  "
              f"image={SHORT[imodel]}")

    with open(OUT / "uncertainty_peaks.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    print(f"  uncertainty_peaks.csv  ({len(rows) - 1} rows)")


if __name__ == "__main__":
    main()

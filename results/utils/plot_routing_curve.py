#!/usr/bin/env python3
"""Accuracy vs human budget X for one routing cell -- the allocation curve.

    python results/utils/plot_routing_curve.py <dataset> <model> <measure> <route>
    e.g. python results/utils/plot_routing_curve.py labelme gpt-4o-mini confidence human_only

Reads   results/<ds>/allocation/<model>/<measure>/<route>/routing.csv
        results/<ds>/allocation/<model>/<measure>/<route>/routing_pivot_accuracy.csv
Writes  results/<ds>/allocation/<model>/<measure>/<route>/routing_accuracy.png

One line per aggregator over X = 5..95, with the two fixed baselines drawn as horizontal
reference lines: X=0% (LLM-only, every instance takes the model's label) and X=100%
(human-only, the crowd aggregator alone). Those two come from the pivot file, which stores
them as explicit endpoint columns.

A missing (X, method) cell is left as a GAP in the line, not interpolated -- an aggregator
that failed to converge at one budget should be visibly absent rather than silently bridged.
Uses the same light-mode palette as plot_uncertainty_cdf.py.
"""
import csv
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#dcdbd6"
# 8 categorical slots, one per aggregator
PALETTE = ["#2a78d6", "#d1495b", "#2e8b57", "#e08214", "#7b52ab",
           "#00868b", "#b5651d", "#7a7a7a"]
LLM_REF = "#d1495b"
HUM_REF = "#2e8b57"


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def main(ds, model, measure, route):
    d = ddir(ds) / "allocation" / model / measure / route
    rows = list(csv.DictReader(open(d / "routing.csv")))
    piv = {r["method"]: r for r in csv.DictReader(open(d / "routing_pivot_accuracy.csv"))}

    methods = sorted({r["method"] for r in rows})
    xs_all = sorted({int(r["X"]) for r in rows})
    acc = {(int(r["X"]), r["method"]): float(r["accuracy"]) for r in rows}

    # endpoints are identical across methods for LLM-only (all instances take the LLM label)
    any_m = next(iter(piv))
    llm_only = float(piv[any_m]["X=0% (LLM-only)"])
    hum_only = {m: float(piv[m]["X=100% (human-only)"]) for m in piv}
    best_hum = max(hum_only.values())
    best_hum_m = max(hum_only, key=hum_only.get)

    fig, ax = plt.subplots(figsize=(9.2, 5.4))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.9)
    ax.set_axisbelow(True)
    for s in ax.spines:
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=9, length=0)

    # baselines
    ax.axhline(llm_only, color=LLM_REF, linewidth=1.6, linestyle=(0, (5, 3)), alpha=0.95)
    ax.text(96.5, llm_only, f" LLM-only {llm_only:.3f}", color=LLM_REF,
            fontsize=8.5, va="center", ha="left")
    ax.axhline(best_hum, color=HUM_REF, linewidth=1.6, linestyle=(0, (5, 3)), alpha=0.95)
    ax.text(96.5, best_hum, f" human-only {best_hum:.3f}\n ({best_hum_m})", color=HUM_REF,
            fontsize=8.5, va="center", ha="left")

    n_missing = 0
    for i, m in enumerate(methods):
        ys = [acc.get((x, m)) for x in xs_all]          # None -> gap, not interpolated
        n_missing += sum(1 for y in ys if y is None)
        ax.plot(xs_all, ys, color=PALETTE[i % len(PALETTE)], linewidth=1.7,
                marker="o", markersize=3.4, label=m, alpha=0.95)

    # peak over the swept region
    pk = max(acc.items(), key=lambda kv: kv[1])
    ax.scatter([pk[0][0]], [pk[1]], s=90, facecolor="none",
               edgecolor=INK, linewidth=1.4, zorder=5)
    ax.annotate(f"peak {pk[1]:.3f}\n{pk[0][1]} @ X={pk[0][0]}%",
                xy=(pk[0][0], pk[1]), xytext=(6, -20), textcoords="offset points",
                color=INK, fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color=INK_2, linewidth=0.8))

    ax.set_xlabel("human budget X  (% of instances routed to human annotators; "
                  "the remaining 100−X take the LLM label)", color=INK_2, fontsize=9.5)
    ax.set_ylabel("accuracy", color=INK_2, fontsize=9.5)
    ax.set_xlim(0, 108)
    ax.set_xticks(range(0, 100, 10))
    ax.set_title(f"{ds} · {model} · {measure} · {route}",
                 color=INK, fontsize=12, fontweight="bold", loc="left", pad=12)
    note = ("instances are ranked by uncertainty; the most uncertain X% go to humans")
    if n_missing:
        note += f"   ·   {n_missing} cell(s) failed to converge, shown as gaps"
    ax.text(0, 1.015, note, transform=ax.transAxes, color=INK_2, fontsize=8.5)

    leg = ax.legend(loc="lower left", fontsize=8.2, ncol=2, frameon=True,
                    facecolor=SURFACE, edgecolor=GRID)
    for t in leg.get_texts():
        t.set_color(INK_2)

    out = d / "routing_accuracy.png"
    fig.tight_layout()
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    print(f"  {out.relative_to(ROOT)}")
    print(f"    methods={len(methods)}  budgets={len(xs_all)}  missing cells={n_missing}")
    print(f"    LLM-only={llm_only:.4f}  best human-only={best_hum:.4f} ({best_hum_m})")
    print(f"    peak={pk[1]:.4f}  {pk[0][1]} @ X={pk[0][0]}%")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) != 4:
        raise SystemExit(__doc__)
    main(*a)

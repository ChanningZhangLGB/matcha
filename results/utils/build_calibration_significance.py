#!/usr/bin/env python3
"""Significance of the prompt-variation ladder on calibration and discrimination.

    python results/utils/build_calibration_significance.py

Each (dataset, model) cell contributes one paired observation per comparison, so the
tests are PAIRED across the 24 cells: the same corpus and the same annotator model are
scored under two different prompting sources, and only the number and kind of prompting
conditions differ.

Two-sided Wilcoxon signed-rank is used rather than a t-test because ECE and AUROC are
bounded and their per-cell differences are not close to normal. Holm correction is
applied across the comparisons reported in one table.

THE CELLS ARE NOT INDEPENDENT. Each dataset appears three times, once per model, and
each model appears six or eight times. The p-values therefore describe the reliability
of the pattern ACROSS this experimental grid, not a population of corpora, and should be
read as such. The effect sizes (median paired difference, win rate) carry the practical
claim; the tests only establish that the direction is not an artefact of a few cells.

Comparisons, chosen so each isolates one thing:
    k0 -> k3   does the full grid beat a single response?          (confidence only)
    k1 -> k3   does widening beyond the protocol axis help?
    k2 -> k3   does widening beyond the wording axis help?
    k1 vs k2   at EQUAL k=3, which axis of variation matters more?

Writes results/calibration_analysis/significance.csv
"""
import csv
import glob
import pathlib
import statistics

from scipy.stats import wilcoxon

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "results" / "calibration_analysis"
OUT = ROOT / "results" / "RQ3" / "calibration"
MEASURES = ["confidence", "entropy", "inter_rater"]
COMPARISONS = [("k0", "k3"), ("k1", "k3"), ("k2", "k3"), ("k1", "k2")]


def load():
    idx = {}
    for f in glob.glob(str(SRC / "*" / "calibration_summary.csv")):
        for r in csv.DictReader(open(f)):
            if r["status"] != "ok" or not r["ECE"] or not r["AUROC"]:
                continue
            idx[(r["dataset"], r["model"], r["measure"], r["source"])] = (
                float(r["ECE"]), float(r["AUROC"]))
    return idx


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    out = [None] * len(ps)
    run = 0.0
    for rank, i in enumerate(order):
        adj = min(1.0, ps[i] * (len(ps) - rank))
        run = max(run, adj)
        out[i] = run
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    idx = load()
    cells = sorted({(d, m) for d, m, _, _ in idx})
    raw = []
    for mi, metric in enumerate(("ECE", "AUROC")):
        for meas in MEASURES:
            for a, b in COMPARISONS:
                pairs = [(idx[(d, m, meas, a)][mi], idx[(d, m, meas, b)][mi])
                         for d, m in cells
                         if (d, m, meas, a) in idx and (d, m, meas, b) in idx]
                if len(pairs) < 6:
                    continue
                diff = [y - x for x, y in pairs]
                # ECE: lower is better, so an improvement is a NEGATIVE difference
                if metric == "ECE":
                    better = sum(1 for v in diff if v < 0)
                else:
                    better = sum(1 for v in diff if v > 0)
                try:
                    stat, p = wilcoxon([x for x, _ in pairs], [y for _, y in pairs])
                except ValueError:
                    stat, p = float("nan"), 1.0
                raw.append({"metric": metric, "measure": meas,
                            "comparison": f"{a}->{b}", "n": len(pairs),
                            "median_diff": round(statistics.median(diff), 4),
                            "improved": f"{better}/{len(pairs)}",
                            "p": p})
    ps = holm([r["p"] for r in raw])
    for r, q in zip(raw, ps):
        r["p_raw"] = f"{r['p']:.2e}"
        r["p_holm"] = f"{q:.2e}"
        r["sig_0.05"] = "yes" if q < 0.05 else "no"
        del r["p"]
    with open(OUT / "significance.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(raw[0]))
        w.writeheader()
        w.writerows(raw)
    hdr = f"{'metric':6s} {'measure':12s} {'comp':9s} {'n':>3s} {'med diff':>9s} {'improved':>9s} {'p(Holm)':>10s}  sig"
    print(hdr)
    for r in raw:
        print(f"{r['metric']:6s} {r['measure']:12s} {r['comparison']:9s} {r['n']:>3d} "
              f"{r['median_diff']:>9.4f} {r['improved']:>9s} {r['p_holm']:>10s}  "
              f"{r['sig_0.05']}")
    print(f"\n  {(OUT / 'significance.csv').relative_to(ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prompt-variation ladder: mean conf-ECE and AUROC, each source tested against k=9.

    python results/utils/build_calibration_table.py

Rows are the three uncertainty measures, columns the four prompting sources. Each cell
is the mean over the 24 (dataset, model) configurations. Every source other than k=9 is
compared against k=9 by a two-sided Wilcoxon signed-rank test PAIRED on those
configurations, and Holm-corrected across the tests in this table (seven per metric:
confidence has three comparable sources, entropy and inter-rater two, since neither is
defined on a single response).

The cells are not independent: each dataset appears once per model and each model once
per dataset in its arm. The tests establish that the direction of each gap is consistent
across the grid, not that it generalises to a population of corpora.

Writes results/calibration_analysis/ladder_table.csv and .tex
"""
import csv
import glob
import pathlib
import statistics

from scipy.stats import wilcoxon

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "results" / "calibration_analysis"
OUT = ROOT / "results" / "RQ3" / "calibration"
MEASURES = [("confidence", "confidence"), ("entropy", "entropy"),
            ("inter_rater", "inter-rater")]
COLS = [("k0", "$k$=1"), ("k1", "$k$=3 (protocol)"),
        ("k2", "$k$=3 (wording)"), ("k3", "$k$=9")]


def stars(p):
    """Significance marker vs k=9. Blank above 0.05: the table highlights where the
    gap is reliable, and an explicit n.s. on every other cell only adds noise."""
    return "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < 0.05 else ""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    idx = {}
    for f in glob.glob(str(SRC / "*" / "calibration_summary.csv")):
        for r in csv.DictReader(open(f)):
            if r["status"] != "ok" or not r["ECE"] or not r["AUROC"]:
                continue
            idx[(r["dataset"], r["model"], r["measure"], r["source"])] = (
                float(r["ECE"]), float(r["AUROC"]))
    cells = sorted({(d, m) for d, m, _, _ in idx})

    tests, means = [], {}
    for mi, metric in enumerate(("ECE", "AUROC")):
        for meas, _disp in MEASURES:
            for src, _lab in COLS:
                vals = [idx[(d, m, meas, src)][mi] for d, m in cells
                        if (d, m, meas, src) in idx]
                means[(metric, meas, src)] = (statistics.mean(vals), len(vals)) \
                    if vals else (None, 0)
                if src == "k3" or not vals:
                    continue
                pairs = [(idx[(d, m, meas, src)][mi], idx[(d, m, meas, "k3")][mi])
                         for d, m in cells
                         if (d, m, meas, src) in idx and (d, m, meas, "k3") in idx]
                if len(pairs) < 6:
                    continue
                _s, p = wilcoxon([a for a, _ in pairs], [b for _, b in pairs])
                tests.append([metric, meas, src, len(pairs), p])
    order = sorted(range(len(tests)), key=lambda i: tests[i][4])
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, tests[i][4] * (len(tests) - rank)))
        tests[i].append(run)
    hol = {(t[0], t[1], t[2]): t[5] for t in tests}

    rows = [["metric", "measure"] + [c[1] for c in COLS]]
    for metric in ("ECE", "AUROC"):
        for meas, disp in MEASURES:
            row = [metric, disp]
            for src, _ in COLS:
                mu, n = means[(metric, meas, src)]
                if mu is None or n == 0:
                    row.append("degenerate"); continue
                if src == "k3":
                    row.append(f"{mu:.4f}")
                else:
                    q = hol.get((metric, meas, src))
                    st = stars(q) if q is not None else ""
                    row.append(f"{mu:.4f} {st}".rstrip())
            rows.append(row)
    with open(OUT / "ladder_table.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    tex = [
        "\\begin{tabular}{@{}llcccc@{}}", "\\toprule",
        "\\textbf{Metric} & \\textbf{Measure} & "
        + " & ".join(f"\\textbf{{{c[1]}}}" for c in COLS) + " \\\\", "\\midrule"]
    for i, r in enumerate(rows[1:]):
        if i == 3:
            tex.append("\\midrule")
        cells_tex = []
        for j, c in enumerate(r[2:]):
            if c == "degenerate":
                cells_tex.append("\\textit{n/a}")
            elif j == 3:
                cells_tex.append(f"\\textbf{{{c}}}")
            else:
                v, _, st = c.partition(" ")
                cells_tex.append(f"{v}$^{{\\text{{{st}}}}}$" if st else v)
        lab = "conf-ECE" if r[0] == "ECE" else "AUROC"
        tex.append(f"{lab if i % 3 == 0 else ''} & {r[1]} & "
                   + " & ".join(cells_tex) + " \\\\")
    tex += ["\\bottomrule", "\\end{tabular}"]
    (OUT / "ladder_table.tex").write_text("\n".join(tex) + "\n")

    w = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    for r in rows:
        print("  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))
    print(f"\nstars: significance vs $k$=9, Wilcoxon signed-rank, Holm-corrected over "
          f"{len(tests)} tests")
    print(f"  {(OUT / 'ladder_table.csv').relative_to(ROOT)}")


if __name__ == "__main__":
    main()

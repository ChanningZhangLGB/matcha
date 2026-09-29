#!/usr/bin/env python3
"""The prompt-variation ladder broken down by annotator model.

    python results/utils/build_calibration_table_by_model.py

Same quantities as build_calibration_table.py, but each mean is taken over that model's
own datasets instead of over all 24 cells.

SAMPLE SIZES DIFFER SHARPLY and this governs what can be tested. gpt-4o-mini annotates
all eight corpora; the two text-only models six each; the two vision models only the two
image corpora. A paired Wilcoxon over n=2 has no power at all, so the image-only models
are reported as descriptive means with no test. Even at n=6 the smallest attainable
two-sided p is 0.031, so a Holm correction across many tests will suppress almost
everything: read the per-model table for the DIRECTION and size of each gap, and take
the significance claims from the pooled table, where n=24.

Writes results/RQ3/calibration/ladder_table_by_model.{csv,tex}
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
COLS = [("k0", "k=1"), ("k1", "k=3 (protocol)"), ("k2", "k=3 (wording)"), ("k3", "k=9")]
MODELS = [("gpt-4o-mini", "GPT-4o-mini"),
          ("llama3.1-8b-instruct-q8_0", "Llama3.1-8B"),
          ("qwen2.5-7b-instruct-q8_0", "Qwen2.5-7B"),
          ("minicpm-v-8b-2.6-q8_0", "MiniCPM-V-8B"),
          ("qwen2.5vl-7b-q8_0", "Qwen2.5VL-7B")]
MIN_N = 6


def stars(p):
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

    tests, means, ns = [], {}, {}
    for mi, metric in enumerate(("ECE", "AUROC")):
        for mkey, _md in MODELS:
            dss = sorted({d for d, m, _, _ in idx if m == mkey})
            for meas, _x in MEASURES:
                for src, _l in COLS:
                    vals = [idx[(d, mkey, meas, src)][mi] for d in dss
                            if (d, mkey, meas, src) in idx]
                    means[(metric, mkey, meas, src)] = (
                        statistics.mean(vals) if vals else None)
                    ns[(metric, mkey, meas, src)] = len(vals)
                    if src == "k3" or not vals:
                        continue
                    pairs = [(idx[(d, mkey, meas, src)][mi],
                              idx[(d, mkey, meas, "k3")][mi]) for d in dss
                             if (d, mkey, meas, src) in idx
                             and (d, mkey, meas, "k3") in idx]
                    if len(pairs) < MIN_N:
                        continue
                    try:
                        _s, p = wilcoxon([a for a, _ in pairs],
                                         [b for _, b in pairs])
                    except ValueError:
                        continue
                    tests.append([metric, mkey, meas, src, p])
    order = sorted(range(len(tests)), key=lambda i: tests[i][4])
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, min(1.0, tests[i][4] * (len(tests) - rank)))
        tests[i].append(run)
    hol = {(t[0], t[1], t[2], t[3]): t[5] for t in tests}

    rows = [["metric", "model", "n_datasets", "measure"] + [c[1] for c in COLS]]
    for metric in ("ECE", "AUROC"):
        for mkey, mdisp in MODELS:
            n = max(ns.get((metric, mkey, m, "k3"), 0) for m, _ in MEASURES)
            for meas, mdis in MEASURES:
                row = [metric, mdisp, n, mdis]
                for src, _ in COLS:
                    mu = means.get((metric, mkey, meas, src))
                    if mu is None:
                        row.append("n/a"); continue
                    if src == "k3":
                        row.append(f"{mu:.4f}")
                    else:
                        st = stars(hol[(metric, mkey, meas, src)]) \
                            if (metric, mkey, meas, src) in hol else ""
                        row.append(f"{mu:.4f} {st}".rstrip())
                rows.append(row)
    with open(OUT / "ladder_table_by_model.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    tex = ["\\begin{tabular}{@{}llcccc@{}}", "\\toprule",
           "\\textbf{Model} & \\textbf{Measure} & "
           + " & ".join(f"\\textbf{{${c[1].replace('k=', 'k$=')}}}" for c in COLS)
           + " \\\\"]
    for metric in ("ECE", "AUROC"):
        tex += ["\\midrule",
                f"\\multicolumn{{6}}{{@{{}}l}}{{\\textit{{"
                f"{'conf-ECE' if metric == 'ECE' else 'AUROC'}}}}} \\\\"]
        for r in [x for x in rows[1:] if x[0] == metric]:
            cells = []
            for j, c in enumerate(r[4:]):
                if c == "n/a":
                    cells.append("\\textit{n/a}")
                elif j == 3:
                    cells.append(f"\\textbf{{{c}}}")
                else:
                    cells.append(c)
            first = r[1] if r[3] == "confidence" else ""
            tex.append(f"{first} & {r[3]} & " + " & ".join(cells) + " \\\\")
    tex += ["\\bottomrule", "\\end{tabular}"]
    (OUT / "ladder_table_by_model.tex").write_text("\n".join(tex) + "\n")

    w = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    for r in rows:
        print("  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))
    print(f"\n{len(tests)} tests run (models with n>={MIN_N} datasets only), "
          f"Holm-corrected together")
    print(f"  {(OUT / 'ladder_table_by_model.csv').relative_to(ROOT)}")


if __name__ == "__main__":
    main()

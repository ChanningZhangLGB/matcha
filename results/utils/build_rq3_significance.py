#!/usr/bin/env python3
"""RQ3 (a) significance: is each uncertainty basis better than the random control?

    python results/utils/build_rq3_significance.py

WHAT IS BEING TESTED, precisely. For a given (dataset, model, measure) the measure and
the random control are compared CELL BY MATCHED CELL: same aggregator, same route, same
budget X, differing only in how instances were ranked. The paired differences

    d = acc(measure | aggregator, route, X) - acc(random | aggregator, route, X)

are tested against zero with a two-sided Wilcoxon signed-rank test. The hypothesis is
therefore "ranking by this signal beats shuffling, systematically across the allocation
sweep" -- NOT "the peak is significant", which would be a post-selection claim.

Holm-Bonferroni corrects across all tests in the family.

THREE LIMITATIONS, stated because they bound how the p-values may be read:

 1. The paired cells are NOT independent. Routed sets are nested across budgets (the
    X=10% set is a subset of X=15%), and aggregators are fit on the same labels. The
    effective sample size is well below n_pairs, so these p-values are ANTI-conservative
    -- they overstate significance. Treat them as a screen, not as a certificate.
 2. This is a test on ACCURACY VALUES across the sweep, not on instances. The
    instance-level test for two classifiers on the same items is McNemar's, which needs
    per-instance predictions; build_routing.py stores only aggregate accuracy, so that
    test cannot be run from the current artefacts.
 3. Ties are common where a measure and random route identical sets (low budgets on
    coarse measures). Wilcoxon drops zero differences, which is reported as n_ties.

Reported alongside: median paired difference and the win rate, which are effect sizes
and are unaffected by the dependence problem above.

Writes results/RQ3/uncertainty/significance_vs_random.csv (+ .md)
"""
import collections
import csv
import pathlib

from scipy import stats

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ3" / "uncertainty"

MEASURES = ["confidence", "entropy", "inter_rater"]
ROUTES = {"h-human": "human_only", "h-human_llm": "human_plus_llm"}
BLOCKS = [("sentiment", "sentiment"), ("movie_reviews", "movie_reviews"),
          ("crowdtruth", "crowdtruth_pooled"), ("conll_ner_5k", "conll_ner_5k"),
          ("pico_5k", "pico_5k"), ("quiz", "quiz"),
          ("labelme", "labelme"), ("imagenet16h", "imagenet16h")]
TEXT_MODELS = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
IMAGE_MODELS = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]
IMAGE_DS = {"labelme", "imagenet16h"}
SHORT = {"gpt-4o-mini": "gpt-4o-mini", "llama3.1-8b-instruct-q8_0": "llama3.1-8b",
         "qwen2.5-7b-instruct-q8_0": "qwen2.5-7b",
         "minicpm-v-8b-2.6-q8_0": "minicpm-v-8b", "qwen2.5vl-7b-q8_0": "qwen2.5vl-7b"}


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def grid(table, model, measure):
    """-> {(route, method, X): accuracy}"""
    out = {}
    for folder, route in ROUTES.items():
        f = ddir(table) / "allocation" / model / measure / route / "routing.csv"
        if not f.exists():
            continue
        for r in csv.DictReader(open(f)):
            out[(folder, r["method"], r["X"])] = float(r["accuracy"])
    return out


def holm(pvals):
    """Holm-Bonferroni adjusted p-values, order preserved."""
    idx = sorted(range(len(pvals)), key=lambda i: pvals[i])
    m = len(pvals)
    adj = [0.0] * m
    prev = 0.0
    for rank, i in enumerate(idx):
        v = min(1.0, (m - rank) * pvals[i])
        prev = max(prev, v)
        adj[i] = prev
    return adj


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    recs = []
    for disp, table in BLOCKS:
        models = IMAGE_MODELS if table in IMAGE_DS else TEXT_MODELS
        for model in models:
            rnd = grid(table, model, "random")
            if not rnd:
                continue
            for me in MEASURES:
                g = grid(table, model, me)
                keys = sorted(set(g) & set(rnd))
                if not keys:
                    continue
                d = [g[k] - rnd[k] for k in keys]
                nz = [x for x in d if x != 0.0]
                ties = len(d) - len(nz)
                wins = sum(1 for x in d if x > 0)
                med = sorted(d)[len(d) // 2]
                if len(nz) >= 6:
                    stat, p = stats.wilcoxon(d, zero_method="wilcox",
                                             alternative="two-sided")
                else:
                    stat, p = float("nan"), float("nan")
                recs.append({"dataset": disp, "model": SHORT[model], "measure": me,
                             "n_pairs": len(d), "n_ties": ties,
                             "win_rate": f"{wins / len(d):.3f}",
                             "median_diff": f"{med:+.4f}",
                             "mean_diff": f"{sum(d) / len(d):+.4f}",
                             "W": "" if stat != stat else f"{stat:.1f}",
                             "p_raw": "" if p != p else f"{p:.3g}"})

    ps = [float(r["p_raw"]) if r["p_raw"] else 1.0 for r in recs]
    for r, a in zip(recs, holm(ps)):
        r["p_holm"] = f"{a:.3g}"
        r["sig_holm_0.05"] = ("yes" if (r["p_raw"] and a < 0.05
                                        and float(r["median_diff"]) > 0)
                              else ("WORSE" if (r["p_raw"] and a < 0.05
                                                and float(r["median_diff"]) < 0)
                                    else "no"))

    f = OUT / "significance_vs_random.csv"
    with open(f, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(recs[0]))
        w.writeheader()
        w.writerows(recs)

    md = ["# RQ3 — uncertainty basis vs random control: paired significance", "",
          "Two-sided Wilcoxon signed-rank on paired differences, matched cell by cell "
          "(same aggregator, same route, same budget). Holm-Bonferroni across all "
          f"{len(recs)} tests.", "",
          "**Cells are not independent** (routed sets nest across budgets; aggregators "
          "share labels), so p-values are anti-conservative — a screen, not a "
          "certificate. `win_rate` and `median_diff` are the effect sizes and are "
          "unaffected.", "",
          "| dataset | model | measure | n | ties | win rate | median Δ | p (Holm) | sig |",
          "|---|---|---|--:|--:|--:|--:|--:|---|"]
    for r in recs:
        md.append(f"| {r['dataset']} | {r['model']} | {r['measure']} | {r['n_pairs']} "
                  f"| {r['n_ties']} | {r['win_rate']} | {r['median_diff']} "
                  f"| {r['p_holm']} | {r['sig_holm_0.05']} |")
    (OUT / "significance_vs_random.md").write_text("\n".join(md) + "\n")

    print(f"  {f.relative_to(ROOT)}  ({len(recs)} tests)")
    sig = sum(1 for r in recs if r["sig_holm_0.05"] == "yes")
    worse = sum(1 for r in recs if r["sig_holm_0.05"] == "WORSE")
    print(f"  significantly BETTER than random: {sig}/{len(recs)}")
    print(f"  significantly WORSE than random:  {worse}/{len(recs)}")
    print()
    print(f"  {'dataset':16s} {'model':13s} {'measure':12s} {'win':>5s} {'medΔ':>8s} "
          f"{'p_holm':>9s}  sig")
    for r in recs:
        print(f"  {r['dataset']:16s} {r['model']:13s} {r['measure']:12s} "
              f"{r['win_rate']:>5s} {r['median_diff']:>8s} {r['p_holm']:>9s}  "
              f"{r['sig_holm_0.05']}")


if __name__ == "__main__":
    main()

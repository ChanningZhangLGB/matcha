#!/usr/bin/env python3
"""RQ1 baseline allocation: confidence-based annotating, MajorityVote only.

    python results/utils/build_ca_annotating.py

THE POLICY. Instances are ranked by the model's uncertainty. The LOW-uncertainty
(100-X)% keep the LLM's label; the HIGH-uncertainty X% are sent to human annotators and
take the crowd label instead. This is the `human_only` route: routing REPLACES the LLM
label rather than adding to it, so at X=0 every instance is LLM-labelled and at X=100
every instance is crowd-labelled.

Aggregation is MajorityVote ONLY -- the plain vote-count baseline. The other seven
crowd-kit aggregators are deliberately excluded here: this table is the simple
allocation baseline that a stronger method has to beat, so it should not itself contain
a max over 8 aggregators.

FOUR FOLDERS, one per uncertainty basis used to rank instances:
    confidence/    1 - mean stated confidence over the 9 conditions
    entropy/       Shannon entropy of the 9 condition labels
    inter_rater/   1 - mean pairwise agreement of the 9 condition labels
    random/        control -- ranking is a seeded shuffle, no uncertainty at all

The `random` folder is the one that decides whether any of this works. A measure that
does not beat it at the same budget is not selecting informative instances, it is just
buying human labels. `entropy` and `inter_rater` are near-duplicates by construction
(both are dispersion summaries of the same count vector) -- expect them to agree.

TIES MATTER HERE. On several datasets 60-80% of instances share u=0, so the cut at a
given X falls inside a tied block and is resolved by task id, not by uncertainty. The
`n_distinct_u` and `pct_tied_at_0` columns carry that per (dataset, model, measure), so
a budget whose membership is largely arbitrary is visible in the table rather than
having to be remembered.

Writes results/RQ1/CaAnnotating/<measure>/allocation_mv.csv  (+ .md)
   and results/RQ1/CaAnnotating/<measure>/allocation_mv_<dataset>.csv per dataset
"""
import collections
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ1" / "CaAnnotating"

MEASURES = ["confidence", "entropy", "inter_rater", "random"]
METHOD = "MajorityVote"
ROUTE = "human_only"
TEXT_MODELS = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
IMAGE_MODELS = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]
SHORT = {"gpt-4o-mini": "gpt-4o-mini",
         "llama3.1-8b-instruct-q8_0": "llama3.1-8b",
         "qwen2.5-7b-instruct-q8_0": "qwen2.5-7b",
         "minicpm-v-8b-2.6-q8_0": "minicpm-v-8b",
         "qwen2.5vl-7b-q8_0": "qwen2.5vl-7b"}
BLOCKS = [("Text", TEXT_MODELS, [("sentiment", "sentiment"),
                                 ("movie_reviews", "movie_reviews"),
                                 ("crowdtruth", "crowdtruth_pooled"),
                                 ("conll_ner_5k", "conll_ner_5k"),
                                 ("pico_5k", "pico_5k"),
                                 ("quiz", "quiz")]),
          ("Image", IMAGE_MODELS, [("labelme", "labelme"),
                                   ("imagenet16h", "imagenet16h")])]
COLS = ["Modality", "Dataset", "model", "X", "n_human", "n_llm",
        "accuracy", "macro_f1", "n_distinct_u", "pct_tied_at_0"]


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def tie_stats(table, model, measure):
    """-> (n_distinct_u, pct_tied_at_0) from the splits file that produced the ranking.

    random/ has no splits.csv -- its ranking is a shuffle, so 'distinct u' is undefined
    and reported blank rather than faked as 0 or n.
    """
    f = ddir(table) / "allocation" / model / measure / "splits.csv"
    if not f.exists():
        return "", ""
    us = [float(r["u"]) for r in csv.DictReader(open(f))]
    if not us:
        return "", ""
    z = sum(1 for u in us if u == 0.0)
    return len(set(us)), f"{100.0 * z / len(us):.1f}%"


def main():
    for measure in MEASURES:
        d = OUT / measure
        d.mkdir(parents=True, exist_ok=True)
        allrows, per_ds = [], collections.defaultdict(list)
        for block, models, rows in BLOCKS:
            for disp, table in rows:
                for m in models:
                    f = (ddir(table) / "allocation" / m / measure / ROUTE
                         / "routing.csv")
                    if not f.exists():
                        continue
                    nd, pt = tie_stats(table, m, measure)
                    for r in csv.DictReader(open(f)):
                        if r["method"] != METHOD:
                            continue
                        row = [block, disp, SHORT[m], r["X"], r["n_human"],
                               r["n_llm"], r["accuracy"], r["macro_f1"], nd, pt]
                        allrows.append(row)
                        per_ds[disp].append(row)

        with open(d / "allocation_mv.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(COLS)
            w.writerows(allrows)
        for disp, rows in per_ds.items():
            with open(d / f"allocation_mv_{disp}.csv", "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(COLS)
                w.writerows(rows)

        # compact wide view: accuracy by budget, one row per (dataset, model)
        wide = collections.defaultdict(dict)
        for r in allrows:
            wide[(r[0], r[1], r[2])][int(r[3])] = r[6]
        xs = sorted({int(r[3]) for r in allrows})
        md = [f"# CaAnnotating baseline - {measure}, {METHOD}, route={ROUTE}", "",
              "Low-uncertainty (100-X)% keep the LLM label; the high-uncertainty X% go "
              "to human annotators. MajorityVote only.", "",
              "| Modality | Dataset | model | " + " | ".join(f"X={x}" for x in xs)
              + " |", "|---|---|---|" + "--:|" * len(xs)]
        for k in sorted(wide, key=lambda k: (k[0] != "Text", k[1], k[2])):
            md.append(f"| {k[0]} | {k[1]} | {k[2]} | "
                      + " | ".join(wide[k].get(x, "") for x in xs) + " |")
        (d / "allocation_mv.md").write_text("\n".join(md) + "\n")
        print(f"  {measure:12s} {len(allrows):4d} rows  "
              f"{len(per_ds)} datasets  -> {(d / 'allocation_mv.csv').relative_to(ROOT)}")


def best():
    """Best CaAnnotating cell per (dataset, model), with the config that produced it.

    Writes results/RQ1/CaAnnotating/ca_annotating_best.{csv,md}.

    The aggregation is MajorityVote for every row BY CONSTRUCTION -- this baseline fixes
    it, so the column is constant and is carried only so the table is self-describing.
    What actually varies, and what `best` selects over, is the UNCERTAINTY BASIS (4) and
    the BUDGET X (19): 76 cells per dataset-model pair.

    Two honesty columns travel with the peak, because a maximum over 76 cells will find
    something even in pure noise:
        random_at_same_X   the random control at the SAME budget and aggregator
        gain_vs_random     peak minus that. This is the number that says whether
                           uncertainty ranking did any work. A peak with gain <= 0 means
                           the budget bought human labels, not informative selection.
    """
    rows = [["Modality", "Dataset", "model", "aggregation", "best_accuracy",
             "uncertainty", "X", "n_human", "n_llm",
             "random_at_same_X", "gain_vs_random", "pct_tied_at_0"]]
    data, tied = {}, {}
    for measure in MEASURES:
        f = OUT / measure / "allocation_mv.csv"
        if not f.exists():
            continue
        for r in csv.DictReader(open(f)):
            k = (r["Modality"], r["Dataset"], r["model"])
            data[(measure, *k, r["X"])] = r
            if measure != "random":
                tied[(measure, *k)] = r["pct_tied_at_0"]

    pairs = sorted({(m, d, mo) for (_, m, d, mo, _) in data},
                   key=lambda k: (k[0] != "Text", k[1], k[2]))
    md = ["# CaAnnotating - best allocation per dataset and model", "",
          "Policy: low-uncertainty (100-X)% keep the LLM label, high-uncertainty X% go "
          "to humans. Aggregation is **MajorityVote** for every row (this baseline fixes "
          "it); `best` selects over 4 uncertainty bases x 19 budgets.", "",
          "`gain_vs_random` is the peak minus the random control at the SAME budget -- "
          "the test of whether uncertainty ranking selected anything. Non-positive means "
          "it did not.", "",
          "| Modality | Dataset | model | best | uncertainty | X | gain vs random "
          "| tied at u=0 |",
          "|---|---|---|--:|---|--:|--:|--:|"]
    for mod, ds, model in pairs:
        cand = [(float(r["accuracy"]), me, x, r)
                for (me, m2, d2, mo2, x), r in data.items()
                if (m2, d2, mo2) == (mod, ds, model) and me != "random"]
        if not cand:
            continue
        acc, me, X, r = max(cand, key=lambda t: t[0])
        rnd = data.get(("random", mod, ds, model, X))
        rv = float(rnd["accuracy"]) if rnd else None
        gain = f"{acc - rv:+.4f}" if rv is not None else ""
        pt = tied.get((me, mod, ds, model), "")
        rows.append([mod, ds, model, METHOD, f"{acc:.4f}", me, X,
                     r["n_human"], r["n_llm"],
                     f"{rv:.4f}" if rv is not None else "", gain, pt])
        md.append(f"| {mod} | {ds} | {model} | **{acc:.4f}** | {me} | {X} "
                  f"| {gain} | {pt} |")

    with open(OUT / "ca_annotating_best.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    (OUT / "ca_annotating_best.md").write_text("\n".join(md) + "\n")
    print(f"  {(OUT / 'ca_annotating_best.csv').relative_to(ROOT)}")
    print(f"  {(OUT / 'ca_annotating_best.md').relative_to(ROOT)}\n")
    print("\n".join(md))


if __name__ == "__main__":
    import sys
    if "best" in sys.argv[1:]:
        best()
    else:
        main()
        best()

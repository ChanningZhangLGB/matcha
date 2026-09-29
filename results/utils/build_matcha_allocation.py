#!/usr/bin/env python3
"""MATCHA allocation records: both routes x 4 uncertainty bases x 8 aggregators.

    python results/utils/build_matcha_allocation.py

The full allocation surface, unreduced. Where CaAnnotating fixes MajorityVote as the
simple baseline, this keeps every aggregator so the method can be compared against that
baseline on equal footing.

LAYOUT
    results/RQ1/MATCHA/
        h-human/        route = human_only      routed instances REPLACE the LLM label
        h-human_llm/    route = human_plus_llm  the LLM stays in the pool as one worker
            confidence/  entropy/  inter_rater/  random/
                allocation_<Aggregator>.csv     one per aggregator (8)
                allocation_all_methods.csv      all 8 together
                allocation_by_budget.md         wide view, accuracy by X

THE TWO ROUTES ARE DIFFERENT POLICIES, not two views of one. Under `h-human` a routed
instance's LLM label is DISCARDED and the crowd label used instead, so at X=100 the
result is the crowd alone. Under `h-human_llm` the LLM remains an annotator alongside
the humans on routed instances, so its vote still counts everywhere. That is why the
confusion-matrix aggregators (DawidSkene, GLAD, MACE, OneCoinDawidSkene) behave so
differently between them: only in `h-human_llm` can they learn a reliability weight for
the LLM and up-weight it above the average human.

`random` is the control, not a method: its ranking is a seeded shuffle. Any measure that
does not beat it at the same budget and aggregator has selected nothing.

TIE CAVEAT carried per row. On most datasets 50-90% of instances share u=0 under
entropy/inter_rater, so the cut at a given X falls inside a tied block and is resolved
by task id. `pct_tied_at_0` makes that visible where it applies; it is blank for
`random`, which has no u.
"""
import collections
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ1" / "MATCHA"

ROUTES = {"h-human": "human_only", "h-human_llm": "human_plus_llm"}
MEASURES = ["confidence", "entropy", "inter_rater", "random"]
AGGREGATORS = ["MajorityVote", "Wawa", "ZeroBasedSkill", "DawidSkene",
               "OneCoinDawidSkene", "GLAD", "MACE", "MMSR"]
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
COLS = ["Modality", "Dataset", "model", "route", "uncertainty", "method", "X",
        "n_human", "n_llm", "accuracy", "macro_f1", "pct_tied_at_0"]


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def tie_pct(table, model, measure):
    f = ddir(table) / "allocation" / model / measure / "splits.csv"
    if not f.exists():
        return ""
    us = [float(r["u"]) for r in csv.DictReader(open(f))]
    if not us:
        return ""
    return f"{100.0 * sum(1 for u in us if u == 0.0) / len(us):.1f}%"


def main():
    total = 0
    for folder, route in ROUTES.items():
        for measure in MEASURES:
            d = OUT / folder / measure
            d.mkdir(parents=True, exist_ok=True)
            by_method = collections.defaultdict(list)
            for block, models, rows in BLOCKS:
                for disp, table in rows:
                    for m in models:
                        f = (ddir(table) / "allocation" / m / measure / route
                             / "routing.csv")
                        if not f.exists():
                            continue
                        pt = tie_pct(table, m, measure)
                        for r in csv.DictReader(open(f)):
                            by_method[r["method"]].append(
                                [block, disp, SHORT[m], folder, measure,
                                 r["method"], r["X"], r["n_human"], r["n_llm"],
                                 r["accuracy"], r["macro_f1"], pt])

            allrows = []
            for a in AGGREGATORS:
                rws = by_method.get(a, [])
                if not rws:
                    continue
                allrows += rws
                with open(d / f"allocation_{a}.csv", "w", newline="") as fh:
                    w = csv.writer(fh)
                    w.writerow(COLS)
                    w.writerows(rws)
            with open(d / "allocation_all_methods.csv", "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(COLS)
                w.writerows(allrows)

            xs = sorted({int(r[6]) for r in allrows})
            wide = collections.defaultdict(dict)
            for r in allrows:
                wide[(r[0], r[1], r[2], r[5])][int(r[6])] = r[9]
            md = [f"# MATCHA allocation - route={route}, uncertainty={measure}", "",
                  "Accuracy by human budget X, one row per (dataset, model, "
                  "aggregator).", "",
                  "| Modality | Dataset | model | method | "
                  + " | ".join(f"X={x}" for x in xs) + " |",
                  "|---|---|---|---|" + "--:|" * len(xs)]
            for k in sorted(wide, key=lambda k: (k[0] != "Text", k[1], k[2],
                                                 AGGREGATORS.index(k[3])
                                                 if k[3] in AGGREGATORS else 99)):
                md.append(f"| {k[0]} | {k[1]} | {k[2]} | {k[3]} | "
                          + " | ".join(wide[k].get(x, "") for x in xs) + " |")
            (d / "allocation_by_budget.md").write_text("\n".join(md) + "\n")

            n_files = len([a for a in AGGREGATORS if by_method.get(a)])
            total += len(allrows)
            print(f"  {folder:13s} {measure:12s} {len(allrows):5,d} rows  "
                  f"{n_files} aggregator files")
    print(f"\n  total {total:,} rows -> {OUT.relative_to(ROOT)}")


def best():
    """Best MATCHA cell per (dataset, model), with the full config that produced it.

    Writes results/RQ1/MATCHA/matcha_best.{csv,md}.

    SELECTION SIZE. `best` is a maximum over
        2 routes x 3 uncertainty bases x 8 aggregators x 19 budgets = 912 cells
    per dataset-model pair (`random` is excluded from the search -- it is the control,
    not a candidate). That is a very large multiplicity, so part of every margin here is
    selection over noise. Two columns are carried to keep that honest:

        random_same_config   the random control at the SAME route, aggregator and budget
        gain_vs_random       peak minus that

    gain_vs_random is the only column that distinguishes "uncertainty ranking worked"
    from "we bought human labels and searched 912 cells". A peak with a small or
    non-positive gain is a null result however high its accuracy looks.
    """
    rows = [["Modality", "Dataset", "model", "best_accuracy", "route", "uncertainty",
             "method", "X", "n_human", "n_llm", "random_same_config",
             "gain_vs_random", "pct_tied_at_0"]]
    cells = {}
    for folder in ROUTES:
        for measure in MEASURES:
            f = OUT / folder / measure / "allocation_all_methods.csv"
            if not f.exists():
                continue
            for r in csv.DictReader(open(f)):
                cells[(r["Modality"], r["Dataset"], r["model"], folder, measure,
                       r["method"], r["X"])] = r

    pairs = sorted({(k[0], k[1], k[2]) for k in cells},
                   key=lambda k: (k[0] != "Text", k[1], k[2]))
    md = ["# MATCHA - best allocation per dataset and model", "",
          "`best` is a maximum over 2 routes x 3 uncertainty bases x 8 aggregators x 19 "
          "budgets = **912 cells** per row. `random` is the control and is excluded from "
          "the search.", "",
          "`gain_vs_random` compares the peak against the random control at the SAME "
          "route, aggregator and budget. With 912 cells searched, this column -- not the "
          "accuracy -- is what says whether uncertainty ranking did any work.", "",
          "| Modality | Dataset | model | best | route | uncertainty | method | X "
          "| gain vs random |",
          "|---|---|---|--:|---|---|---|--:|--:|"]
    for mod, ds, model in pairs:
        cand = [(float(r["accuracy"]), k, r) for k, r in cells.items()
                if (k[0], k[1], k[2]) == (mod, ds, model) and k[4] != "random"]
        if not cand:
            continue
        acc, k, r = max(cand, key=lambda t: t[0])
        _, _, _, folder, measure, method, X = k
        rnd = cells.get((mod, ds, model, folder, "random", method, X))
        rv = float(rnd["accuracy"]) if rnd else None
        gain = f"{acc - rv:+.4f}" if rv is not None else ""
        rows.append([mod, ds, model, f"{acc:.4f}", folder, measure, method, X,
                     r["n_human"], r["n_llm"],
                     f"{rv:.4f}" if rv is not None else "", gain,
                     r["pct_tied_at_0"]])
        md.append(f"| {mod} | {ds} | {model} | **{acc:.4f}** | {folder} | {measure} "
                  f"| {method} | {X} | {gain} |")

    with open(OUT / "matcha_best.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    (OUT / "matcha_best.md").write_text("\n".join(md) + "\n")
    print(f"  {(OUT / 'matcha_best.csv').relative_to(ROOT)}")
    print(f"  {(OUT / 'matcha_best.md').relative_to(ROOT)}\n")
    print("\n".join(md))


if __name__ == "__main__":
    if "best" in sys.argv[1:]:
        best()
    else:
        main()
        print()
        best()

#!/usr/bin/env python3
"""Uncertainty-routed annotation: humans on the uncertain X%, LLM on the rest.

    python results/build_routing.py gpt-4o-mini [--datasets a,b] [--measures ...]
                                    [--methods ...] [--random]

For each (dataset, uncertainty measure, X in 5..95 step 5):

  HIGH batch  = top X% by uncertainty rank -> sent to the human crowd.
                The crowd annotation matrix is RESTRICTED to those tasks and every
                aggregator is RE-FITTED on that subset. This matters: DawidSkene,
                GLAD, MACE, MMSR and the skill-based methods estimate per-annotator
                reliability from the data they see, so slicing a full-data run would
                use parameters fitted on instances that are no longer in the pool --
                which is not the same experiment.

  LOW batch   = the remaining (1-X)% -> takes the LLM-only label (majority vote over
                the 9 prompt conditions) with no human annotation at all.

The two label sets are concatenated to cover the dataset and scored against gold, so
every X is evaluated on the same instances and the numbers are comparable across X.

--random adds the control: the same X% routed to humans, chosen uniformly at random
(seed 42) instead of by uncertainty. Without it, "accuracy rises with X" is trivially
true -- more human labels always help -- and says nothing about whether the RANKING
is doing any work. The gap between a measure and random is the actual finding.

Two ROUTES, selected with --route, differing only in how the high batch is labelled:

  human_only       the human crowd alone annotates the uncertain X%
  human_plus_llm   the LLM's MV label joins that subset as one extra annotator

Writes results/<dataset>/allocation/<model>/<measure>/<route>/routing.csv
   and results/<dataset>/allocation/<model>/random/<route>/routing.csv (with --random)
"""
import argparse
import csv
import pathlib
import random
import sys
import time
import warnings

warnings.filterwarnings("ignore")

import pandas as pd                                                  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval"))
from common.metrics import categorical_metrics                       # noqa: E402

from crowdkit.aggregation import (                                   # noqa: E402
    GLAD, MACE, MMSR, DawidSkene, MajorityVote, OneCoinDawidSkene,
    Wawa, ZeroBasedSkill,
)

LONG = ROOT / "eval" / "data"
RES = ROOT / "results"
N_ITER = 100
XS = list(range(5, 100, 5))
ALL_DS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
          "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"]
ALL_ME = ["confidence", "entropy", "inter_rater"]
POSITIVE = {"sentiment": "pos", "crowdtruth_cause": "yes",
            "crowdtruth_treat": "yes", "crowdtruth_pooled": "yes", "pico_5k": "in"}
BUILD = {
    "MajorityVote": lambda: MajorityVote(),
    "Wawa": lambda: Wawa(),
    "DawidSkene": lambda: DawidSkene(n_iter=N_ITER),
    "OneCoinDawidSkene": lambda: OneCoinDawidSkene(n_iter=N_ITER),
    "ZeroBasedSkill": lambda: ZeroBasedSkill(n_iter=N_ITER),
    "MMSR": lambda: MMSR(n_iter=N_ITER),
    "GLAD": lambda: GLAD(n_iter=N_ITER),
    "MACE": lambda: MACE(n_iter=N_ITER),
}


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def load(ds, model):
    crowd = pd.read_csv(LONG / f"{ds}_crowd.csv", dtype=str)
    gold = {r["task"]: r["true_label"]
            for r in csv.DictReader(open(LONG / f"{ds}_gold.csv"))}
    f = ddir(ds) / "model_analysis" / model / "uncertainty_per_instance.csv"
    llm = {r["task"]: r["llm_label"]
           for r in csv.DictReader(open(f)) if r["llm_label"]}
    return crowd, gold, llm


def ranking(ds, measure, model):
    """Task ids ordered most-uncertain-first, from the precomputed splits."""
    f = ddir(ds) / "allocation" / model / measure / "splits.csv"
    if not f.exists():
        return None
    return [r["task"] for r in csv.DictReader(open(f))]     # already sorted by rank


def run_one(ds, order, crowd, gold, llm, methods, out_csv, tag, route, model):
    """route = 'human_only'      : the high batch is aggregated from human votes alone
       route = 'human_plus_llm'  : the LLM's MV label joins the high batch as one
                                   extra annotator before aggregation.
    Both routes give the low batch the LLM-only label untouched, so the two differ
    ONLY in what the humans' subset looks like."""
    n = len(order)
    rows = []
    for x in XS:
        k = max(1, min(n - 1, round(n * x / 100)))
        high, low = set(order[:k]), order[k:]
        sub = crowd[crowd["task"].isin(high)]
        if route == "human_plus_llm":
            extra = [(t, f"LLM::{model}", llm[t]) for t in high if t in llm]
            if extra:
                sub = pd.concat(
                    [sub, pd.DataFrame(extra, columns=["task", "worker", "label"])],
                    ignore_index=True)
        for name in methods:
            t0 = time.time()
            try:
                pred = BUILD[name]().fit_predict(sub)
                lab = dict(pred)
            except Exception as e:                                   # noqa: BLE001
                print(f"    x{x:02d} {name:18s} FAILED {type(e).__name__}: "
                      f"{str(e)[:60]}", flush=True)
                continue
            # low batch takes the LLM label untouched
            for t in low:
                if t in llm:
                    lab[t] = llm[t]
            ids = [t for t in order if t in lab and t in gold]
            m = categorical_metrics([gold[t] for t in ids], [lab[t] for t in ids],
                                    positive=POSITIVE.get(ds))
            rows.append({
                "X": x, "route": route, "method": name,
                "n_human": len(high), "n_llm": len(low),
                "accuracy": round(m["accuracy"], 4),
                "macro_f1": round(m["macro_f1"], 4),
                "weighted_f1": round(m["weighted_f1"], 4),
                **({f"f1_{POSITIVE[ds]}": round(m[f"f1_{POSITIVE[ds]}"], 4)}
                   if POSITIVE.get(ds) and f"f1_{POSITIVE[ds]}" in m else {}),
                "coverage": round(len(ids) / len(gold), 4),
                "seconds": round(time.time() - t0, 1),
            })
        done = [r for r in rows if r["X"] == x]
        if done:
            best = max(done, key=lambda r: r["macro_f1"])
            print(f"    {tag} x{x:02d}  human={len(high):5,d} llm={len(low):5,d}  "
                  f"best {best['method']:18s} macroF1={best['macro_f1']:.4f}", flush=True)
    if rows:
        cols = list(rows[0].keys())
        with open(out_csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", default="gpt-4o-mini")
    ap.add_argument("--datasets", default=",".join(ALL_DS))
    ap.add_argument("--measures", default=",".join(ALL_ME))
    ap.add_argument("--methods", default=",".join(BUILD))
    ap.add_argument("--random", action="store_true")
    ap.add_argument("--route", default="human_only",
                    choices=["human_only", "human_plus_llm"])
    a = ap.parse_args()
    methods = [m for m in a.methods.split(",") if m in BUILD]

    for ds in a.datasets.split(","):
        crowd, gold, llm = load(ds, a.model)
        print(f"\n=== {ds}: {len(gold):,} tasks, {crowd.worker.nunique():,} workers, "
              f"LLM labels for {len(llm):,}", flush=True)
        for measure in a.measures.split(","):
            order = ranking(ds, measure, a.model)
            if not order:
                print(f"  {measure}: no splits.csv, skipped", flush=True)
                continue
            out = ddir(ds) / "allocation" / a.model / measure / a.route
            out.mkdir(parents=True, exist_ok=True)
            run_one(ds, order, crowd, gold, llm, methods,
                    out / "routing.csv", measure[:4], a.route, a.model)
        if a.random:
            order = sorted(gold)
            random.Random(42).shuffle(order)
            out = ddir(ds) / "allocation" / a.model / "random" / a.route
            out.mkdir(parents=True, exist_ok=True)
            run_one(ds, order, crowd, gold, llm, methods,
                    out / "routing.csv", "rand", a.route, a.model)
    print("\nROUTING_DONE", flush=True)


if __name__ == "__main__":
    main()

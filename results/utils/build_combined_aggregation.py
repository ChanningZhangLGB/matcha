#!/usr/bin/env python3
"""Human + LLM aggregation: add the LLM as ONE extra annotator, re-run all 8 methods.

    python results/build_combined_aggregation.py gpt-4o-mini

The LLM contributes a single vote per instance -- its majority-vote label over the 9
(protocol x prompt-strategy) conditions, i.e. the same label that fills the LLM-only
column. It is appended to the human crowd table as one additional worker, then the
same 8 unsupervised crowd-kit aggregators run on the combined pool and are scored
against the same gold.

Two things this is NOT:
  - not 9 extra annotators (the conditions are the same model under different prompts;
    their errors are correlated, so treating them as independent raters would give the
    LLM ~9x the weight of any human)
  - not a replacement for a human (the human labels are all retained)

Instances with no LLM label keep their human votes unchanged, so coverage never drops.

Writes results/<dataset>/combined_aggregation_<model>.{md,csv}
"""
import collections
import csv
import pathlib
import sys
import time
import warnings

warnings.filterwarnings("ignore")

import pandas as pd                                                  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
from common.metrics import categorical_metrics                       # noqa: E402

from crowdkit.aggregation import (                                   # noqa: E402
    GLAD, MACE, MMSR, DawidSkene, MajorityVote, OneCoinDawidSkene,
    Wawa, ZeroBasedSkill,
)

LONG = ROOT / "eval" / "data"
RES = ROOT / "results"
N_ITER = 100
DATASETS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
            "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"]
POSITIVE = {"sentiment": "pos", "crowdtruth_cause": "yes",
            "crowdtruth_treat": "yes", "crowdtruth_pooled": "yes", "pico_5k": "in"}


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def mdir(ds, model, base=None):
    """Per-model output dir: <dataset>/model_analysis/<model>/ (created on demand)."""
    d = (base or ddir(ds)) / "model_analysis" / model
    d.mkdir(parents=True, exist_ok=True)
    return d



def methods():
    return [
        ("MajorityVote", lambda: MajorityVote()),
        ("DawidSkene", lambda: DawidSkene(n_iter=N_ITER)),
        ("OneCoinDawidSkene", lambda: OneCoinDawidSkene(n_iter=N_ITER)),
        ("GLAD", lambda: GLAD(n_iter=N_ITER)),
        ("MACE", lambda: MACE(n_iter=N_ITER)),
        ("MMSR", lambda: MMSR(n_iter=N_ITER)),
        ("Wawa", lambda: Wawa()),
        ("ZeroBasedSkill", lambda: ZeroBasedSkill(n_iter=N_ITER)),
    ]


def llm_labels(ds, model):
    """The LLM's majority-vote label per task, from the per-instance uncertainty table."""
    f = ddir(ds) / "model_analysis" / model / "uncertainty_per_instance.csv"
    if not f.exists():
        return {}
    return {r["task"]: r["llm_label"] for r in csv.DictReader(open(f))
            if r["llm_label"]}


def main(model):
    for ds in DATASETS:
        crowd = pd.read_csv(LONG / f"{ds}_crowd.csv", dtype=str)
        gold = pd.read_csv(LONG / f"{ds}_gold.csv", dtype=str).set_index("task")["true_label"]
        lab = llm_labels(ds, model)
        if not lab:
            print(f"  {ds}: no LLM labels, skipped")
            continue

        # --- correctness checks before mixing anything in -------------------
        human_labels = set(crowd["label"])
        gold_labels = set(gold)
        llm_lset = set(lab.values())
        stray = llm_lset - (human_labels | gold_labels)
        worker_name = f"LLM::{model}"
        assert worker_name not in set(crowd["worker"]), "worker id collision"

        add = pd.DataFrame({"task": list(lab), "worker": worker_name,
                            "label": [lab[t] for t in lab]})
        add = add[add["task"].isin(set(crowd["task"]))]     # only tasks the humans rated
        combined = pd.concat([crowd, add], ignore_index=True)

        n_h = crowd["worker"].nunique()
        cov = add["task"].nunique() / gold.size
        print(f"\n=== {ds}: {n_h:,} human workers + 1 LLM; LLM votes on "
              f"{add['task'].nunique():,}/{gold.size:,} tasks ({100*cov:.1f}%)"
              + (f"  [stray LLM labels: {sorted(stray)}]" if stray else ""))

        rows = []
        for name, build in methods():
            t0 = time.time()
            try:
                pred = build().fit_predict(combined).reindex(gold.index)
                ok = pred.notna()
                m = categorical_metrics(gold[ok], pred[ok], positive=POSITIVE.get(ds))
                m.update(method=name, seconds=round(time.time() - t0, 1))
                rows.append(m)
                print(f"    {name:20s} acc={m['accuracy']:.4f} "
                      f"macroF1={m['macro_f1']:.4f}  ({m['seconds']}s)")
            except Exception as e:                                   # noqa: BLE001
                print(f"    {name:20s} FAILED {type(e).__name__}: {str(e)[:70]}")

        if not rows:
            continue
        pos = POSITIVE.get(ds)
        cols = ["accuracy", "macro_f1", "weighted_f1"] + ([f"f1_{pos}"] if pos else [])
        d = ddir(ds)
        with open(mdir(ds, model, d) / "combined_aggregation.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["method"] + cols + ["seconds"])
            for r in sorted(rows, key=lambda x: -x["macro_f1"]):
                w.writerow([r["method"]] + [f"{r.get(c, float('nan')):.4f}" for c in cols]
                           + [r["seconds"]])

        H = {r["method"]: r for r in csv.DictReader(open(d / "crowd_aggregation.csv"))}
        L = [f"# {ds} - Human + {model} aggregation", "",
             f"The LLM is appended as **one additional annotator** ({worker_name}) whose "
             f"label is its majority vote over the 9 prompt conditions, joining "
             f"{n_h:,} human workers. All 8 aggregators then re-run on the combined pool.",
             "", "| Method | macro-F1 human-only | macro-F1 human+LLM | delta |",
             "|---|--:|--:|--:|"]
        for r in sorted(rows, key=lambda x: -x["macro_f1"]):
            h = float(H[r["method"]]["macro_f1"]) if r["method"] in H else float("nan")
            L.append(f"| {r['method']} | {h:.4f} | **{r['macro_f1']:.4f}** | "
                     f"{r['macro_f1']-h:+.4f} |")
        (mdir(ds, model, d) / "combined_aggregation.md").write_text("\n".join(L) + "\n")
    print("\ndone")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

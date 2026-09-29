#!/usr/bin/env python3
"""Track 1 — categorical aggregation.

Runs 8 crowd-kit aggregators over every long-form table in eval/data/.
GoldMajorityVote is deliberately excluded: it consumes ground truth at fit time,
which would make it non-comparable with the unsupervised methods.

    python eval/run_categorical.py [dataset ...]
"""
import sys
import time
import warnings
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common.metrics import categorical_metrics          # noqa: E402
from common.paths import LONG, RESULTS                  # noqa: E402

warnings.filterwarnings("ignore")

from crowdkit.aggregation import (                      # noqa: E402
    GLAD, MACE, MMSR, DawidSkene, MajorityVote, OneCoinDawidSkene,
    Wawa, ZeroBasedSkill,
)

N_ITER = 100

# The positive class used for the extra binary F1 column, per dataset.
_POSITIVE = {"sentiment": "pos", "crowdtruth_cause": "yes",
             "crowdtruth_treat": "yes", "crowdtruth_pooled": "yes",
             "pico": "in"}


def positive_of(name):
    """Positive class, ignoring any `_5k` subsample suffix."""
    return _POSITIVE.get(name[:-3] if name.endswith("_5k") else name)


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


def datasets():
    return sorted(p.name[: -len("_crowd.csv")] for p in LONG.glob("*_crowd.csv"))


def run(name):
    crowd = pd.read_csv(LONG / f"{name}_crowd.csv", dtype=str)
    gold = pd.read_csv(LONG / f"{name}_gold.csv", dtype=str).set_index("task")["true_label"]
    print(f"\n=== {name}: {gold.size:,} tasks, {crowd.worker.nunique():,} workers, "
          f"{len(crowd):,} judgments, {gold.nunique()} classes")

    rows = []
    for label, build in methods():
        t0 = time.time()
        try:
            pred = build().fit_predict(crowd)
            pred = pred.reindex(gold.index)
            n_missing = int(pred.isna().sum())
            m = categorical_metrics(gold[pred.notna()], pred[pred.notna()],
                                    positive=positive_of(name))
            m.update(method=label, dataset=name, seconds=round(time.time() - t0, 1),
                     n_unpredicted=n_missing)
            rows.append(m)
            pos = positive_of(name)
            extra = f"  f1_{pos}={m['f1_' + pos]:.4f}" if pos and ("f1_" + pos) in m else ""
            print(f"  {label:20s} acc={m['accuracy']:.4f}  macroF1={m['macro_f1']:.4f}"
                  f"{extra}  ({m['seconds']}s)")
        except Exception as e:
            print(f"  {label:20s} FAILED  {type(e).__name__}: {str(e)[:90]}")
            rows.append({"method": label, "dataset": name,
                         "error": f"{type(e).__name__}: {e}",
                         "seconds": round(time.time() - t0, 1)})
    return rows


if __name__ == "__main__":
    RESULTS.mkdir(parents=True, exist_ok=True)
    targets = sys.argv[1:] or datasets()
    all_rows = []
    for ds in targets:
        all_rows += run(ds)
    df = pd.DataFrame(all_rows)
    out = RESULTS / "categorical.csv"

    # UPSERT, don't overwrite. Only the datasets just scored are replaced; every other
    # dataset's rows are carried through untouched. Without this, scoring one dataset
    # (`run_categorical.py quiz`) would leave a file containing ONLY that dataset and
    # silently destroy the rest, forcing a full ~7-minute re-run to add anything.
    if out.exists():
        prev = pd.read_csv(out)
        kept = prev[~prev["dataset"].isin(df["dataset"].unique())]
        if len(kept):
            print(f"\ncarrying forward {len(kept)} rows for "
                  f"{', '.join(sorted(kept['dataset'].unique()))}")
        df = pd.concat([kept, df], ignore_index=True)

    cols = [c for c in ["dataset", "method", "accuracy", "macro_f1", "weighted_f1"]
            if c in df.columns] + sorted(c for c in df.columns if c.startswith("f1_")) \
        + [c for c in ["n_unpredicted", "seconds", "error"] if c in df.columns]
    df[cols].to_csv(out, index=False)
    print(f"\nwrote {out}")

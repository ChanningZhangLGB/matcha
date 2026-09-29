#!/usr/bin/env python3
"""Subsample the two token-recast tables down to ~5,000 tasks.

Sampling is done at the NATURAL UNIT, never at the token: whole CoNLL sentences and
whole PICO documents are drawn, then all of their tokens are kept. Cutting tokens
loose from their sentence/document would destroy the context that makes the
annotation meaningful, so the target of 5,000 is approached from below by adding
whole units and is slightly overshot by the last one.

    python eval/convert/subsample.py

Writes <name>_5k_{crowd,gold}.csv next to the full tables; the full tables are left
in place.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.paths import LONG  # noqa: E402

SEED = 42
TARGET = 5000

# task-id -> natural unit. conll: "s{sent}_t{tok}" ; pico: "{docid}_{i}"
UNIT = {
    "conll_ner": (lambda t: t.str.split("_").str[0], "sentence"),
    "pico": (lambda t: t.str.rsplit("_", n=1).str[0], "document"),
}


def subsample(name):
    key_fn, unit_name = UNIT[name]
    crowd = pd.read_csv(LONG / f"{name}_crowd.csv", dtype=str)
    gold = pd.read_csv(LONG / f"{name}_gold.csv", dtype=str)

    gold["unit"] = key_fn(gold["task"])
    sizes = gold.groupby("unit")["task"].nunique()

    rng = np.random.default_rng(SEED)
    units = sizes.index.to_numpy()
    rng.shuffle(units)

    chosen, total = [], 0
    for u in units:
        if total >= TARGET:
            break
        chosen.append(u)
        total += int(sizes[u])
    chosen = set(chosen)

    g = gold[gold["unit"].isin(chosen)].drop(columns="unit")
    crowd["unit"] = key_fn(crowd["task"])
    c = crowd[crowd["unit"].isin(chosen)].drop(columns="unit")

    g.to_csv(LONG / f"{name}_5k_gold.csv", index=False)
    c.to_csv(LONG / f"{name}_5k_crowd.csv", index=False)
    print(f"  {name}_5k: {len(chosen):,} {unit_name}s of {len(sizes):,} "
          f"({100*len(chosen)/len(sizes):.1f}%)  ->  {len(g):,} tasks, "
          f"{c.worker.nunique():,} workers, {len(c):,} judgments")
    return len(chosen), len(sizes), len(g)


if __name__ == "__main__":
    print(f"subsampling to ~{TARGET:,} tasks, whole units only, seed={SEED}")
    for n in ["conll_ner", "pico"]:
        subsample(n)

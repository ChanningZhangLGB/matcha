#!/usr/bin/env python3
"""Split the cross-dataset roll-ups by MODALITY: text arm vs image arm.

    python results/utils/build_modality_split.py

The per-dataset directories under results/<dataset>/ are NOT moved -- 16 scripts resolve
paths through their own ddir(), and relocating them would risk the completed text pipeline
for no analytical gain. What this does instead is split the roll-ups that currently mix
both arms in one file, which is the part that actually needs separating: the two arms use
DIFFERENT annotator line-ups and cannot be read as one table.

    text arm   7 datasets  x  gpt-4o-mini, llama3.1-8b, qwen2.5-7b      (text LLMs)
    image arm  2 datasets  x  gpt-4o-mini, minicpm-v-2.6, qwen2.5-VL    (VLMs)

Only gpt-4o-mini spans both (it is multimodal), so it is the single point of comparison
between the arms; the other four models appear in exactly one.

Writes results/by_modality/{text,image}/{overview_human_vs_llm,overview_human_plus_llm,
allocation_best,budget}.csv and a combined results/RESULTS_BY_MODALITY.md.
"""
import csv
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "by_modality"

TEXT_DATASETS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
                 "conll_ner_5k", "pico_5k", "quiz"]
IMAGE_DATASETS = ["labelme", "imagenet16h"]
TEXT_MODELS = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
IMAGE_MODELS = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]

ARMS = {"text": (TEXT_DATASETS, TEXT_MODELS), "image": (IMAGE_DATASETS, IMAGE_MODELS)}


def split_by_dataset(src, key="dataset"):
    """-> {arm: [rows]} for a roll-up keyed on a dataset column."""
    if not (RES / src).exists():
        return {}
    rows = list(csv.DictReader(open(RES / src)))
    out = {}
    for arm, (dss, _) in ARMS.items():
        keep = [r for r in rows if r.get(key) in dss]
        if keep:
            out[arm] = keep
    return out


def write(arm, name, rows, drop_empty_cols=True):
    """Write rows, optionally dropping columns that are entirely blank for this arm.

    The union-column overview carries one llm-only column per model across BOTH arms, so
    an arm-scoped copy would otherwise keep 2-3 permanently empty columns for models that
    never ran on it.
    """
    if not rows:
        return
    d = OUT / arm
    d.mkdir(parents=True, exist_ok=True)
    cols = list(rows[0])
    if drop_empty_cols:
        cols = [c for c in cols if any(str(r.get(c, "")).strip() for r in rows)]
    with open(d / name, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  by_modality/{arm}/{name}  ({len(rows)} rows x {len(cols)} cols)")


def budgets():
    """Per-arm budget table: one row per (model, dataset), only that arm's models."""
    for arm, (dss, models) in ARMS.items():
        rows = []
        for m in models:
            f = RES / f"budget_{m}.csv"
            if not f.exists():
                continue
            for r in csv.DictReader(open(f)):
                if r["dataset"] in dss:
                    rows.append({"model": m, **r})
        write(arm, "budget.csv", rows)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)          # regenerate cleanly; purely derived, nothing original
    for name in ["overview_human_vs_llm.csv", "overview_human_plus_llm.csv",
                 "allocation_best.csv"]:
        for arm, rows in split_by_dataset(name).items():
            write(arm, name, rows)
    budgets()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cross-dataset Human+LLM overview: accuracy, one row per (dataset, model).

    python results/utils/build_overview_human_plus_llm.py

Every cell is an accuracy from the 8 crowd-kit aggregators. The `annotator_pool`
column says WHO was aggregated:

    human-only          the human crowd alone
    <model> + human     the same crowd plus the LLM as ONE extra annotator,
                        with every aggregator re-fitted on the combined pool

Each dataset leads with its human-only row, so the delta from adding a model reads
straight down the column. Single header row -- no merged section cells -- so the
file opens cleanly in a spreadsheet.

Writes results/overview_human_plus_llm.csv
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
DATASETS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
            "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"]
HUMAN = ["DawidSkene", "MajorityVote", "GLAD", "Wawa", "MMSR", "MACE",
         "ZeroBasedSkill", "OneCoinDawidSkene"]
# TEXT and IMAGE arms use different annotator line-ups; only gpt-4o-mini is in
# both. A flat MODELS list silently omits the two VLMs from the image rows.
MODELS_TEXT = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
MODELS_IMAGE = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]
IMAGE_DATASETS = {"labelme", "imagenet16h"}


def models_for(ds):
    """Annotator line-up for a dataset."""
    return MODELS_IMAGE if ds in IMAGE_DATASETS else MODELS_TEXT


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def main():
    out = RES / "overview_human_plus_llm.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset", "annotator_pool"] + HUMAN)
        n = 0
        for ds in DATASETS:
            d = ddir(ds)
            # human-only reference row first
            H = {r["method"]: r for r in
                 csv.DictReader(open(d / "crowd_aggregation.csv"))}
            w.writerow([ds, "human-only"]
                       + [f"{float(H[m]['accuracy']):.4f}" if m in H else "" for m in HUMAN])
            f = d / "summary_table_human_plus_llm.csv"
            if not f.exists():
                continue
            rows = list(csv.DictReader(open(f)))
            for model in models_for(ds):
                r = next((x for x in rows
                          if x["annotator_pool"] == f"{model} + human"
                          and x["metric"] == "Acc"), None)
                if not r:
                    continue
                w.writerow([ds, f"{model} + human"] + [r.get(m, "") for m in HUMAN])
                n += 1
    print(f"  {out.relative_to(ROOT)}  ({len(DATASETS)} datasets x "
          f"(1 human-only + {n // len(DATASETS)} model) rows, accuracy)")


if __name__ == "__main__":
    main()

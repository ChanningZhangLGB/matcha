#!/usr/bin/env python3
"""Cross-dataset overview: accuracy, one row per dataset.

    python results/utils/build_overview.py

One row per dataset, accuracy only. Column names carry their own prefix so a single
header row is enough -- no merged section cells to confuse a spreadsheet:

    human-only: <aggregator>   the human crowd aggregated by that method
    llm-only:   <model>        that model's majority vote over its 9
                               protocol x prompt-strategy conditions, no humans

Per-dataset macro-F1 lives in each dataset's own summary_table.

Writes results/overview_human_vs_llm.csv
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


# This overview is ONE flat CSV, so its columns must be the UNION of both line-ups.
# A dataset only carries values for the models actually run on it; the rest stay blank
# (text models cannot see images, and the VLMs were never run on text).
ALL_MODELS = MODELS_TEXT + [m for m in MODELS_IMAGE if m not in MODELS_TEXT]


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def main():
    out = RES / "overview_human_vs_llm.csv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset"]
                   + [f"human-only: {m}" for m in HUMAN]
                   + [f"llm-only: {m}" for m in ALL_MODELS])
        for ds in DATASETS:
            d = ddir(ds)
            H = {r["method"]: r for r in
                 csv.DictReader(open(d / "crowd_aggregation.csv"))}
            # summary_table.csv: single header, first data row is Acc
            st = list(csv.DictReader(open(d / "summary_table.csv")))
            acc = {k.split(": ", 1)[-1]: v
                   for k, v in next(x for x in st if x["metric"] == "Acc").items()
                   if k != "metric"}
            w.writerow([ds]
                       + [f"{float(H[m]['accuracy']):.4f}" if m in H else "" for m in HUMAN]
                       + [acc.get(m, "") for m in ALL_MODELS])
    print(f"  {out.relative_to(ROOT)}  ({len(DATASETS)} rows x "
          f"{len(HUMAN) + len(ALL_MODELS)} columns, accuracy)")


if __name__ == "__main__":
    main()

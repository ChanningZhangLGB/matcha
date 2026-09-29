#!/usr/bin/env python3
"""Convert datasets_pass/imagenet16h into crowd-kit long form.

    python eval/convert/build_imagenet16h.py

ImageNet-16H (Steyvers, Tejeda, Kerrigan & Smyth, PNAS 2022): 1,200 ImageNet photos in 16
categories, each shown at four phase-noise levels, classified by 145 crowd participants.

Emits into eval/data/:
    imagenet16h_crowd.csv   task, worker, label
    imagenet16h_gold.csv    task, true_label

THE INSTANCE UNIT IS (image x noise level), NOT image. Each noise variant was judged
separately and is a different stimulus with a different difficulty, so a task id is
`<image_name>_n<level>` -- 1,200 x 4 = 4,800 tasks from 28,997 judgments (~6 per task).
Collapsing across noise would pool four difficulty regimes into one instance and destroy
the gradient that makes this corpus worth having:

    noise  80  human accuracy 0.900
    noise  95                 0.860
    noise 110                 0.771
    noise 125                 0.603

The 1,200 `original` (noiseless) images carry gold but were never shown to participants,
so they have no crowd labels and are absent from datasets_pass and from this table.

GOLD is `image_category`, verified constant across every row of an image. The corpus also
ships a `correct` column; check() asserts it equals (participant_classification ==
image_category) on every row, which is what licenses using image_category as ground truth.

Per-trial `confidence` (high/medium/low) and response times exist in the source CSV and are
NOT carried here -- the long form is strictly task/worker/label. Read them from
datasets_pass/imagenet16h/behavioral/ if the analysis needs measured human uncertainty.
"""
import collections
import csv
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common.paths import DATA, LONG  # noqa: E402

SRC = pathlib.Path(DATA) / "imagenet16h"
BEHAV = SRC / "behavioral" / "human_only_classification_6per_img_export.csv"


def main():
    LONG.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(BEHAV)))

    # gold must be a property of the IMAGE, not of the trial
    by_img = collections.defaultdict(set)
    for r in rows:
        by_img[r["image_name"]].add(r["image_category"])
    bad = {k: v for k, v in by_img.items() if len(v) != 1}
    if bad:
        raise SystemExit(f"image_category varies within an image: {list(bad)[:3]}")

    # the shipped `correct` flag must agree with our reading of which column is gold
    mism = [r["id"] for r in rows
            if (r["participant_classification"] == r["image_category"]) != (r["correct"] == "1")]
    if mism:
        raise SystemExit(f"`correct` disagrees with participant==category on {len(mism)} rows")

    crowd, gold = [], {}
    for r in rows:
        task = f"{r['image_name']}_n{int(r['noise_level']):03d}"
        crowd.append((task, r["worker_id"], r["participant_classification"]))
        gold[task] = r["image_category"]

    # every task must resolve to a stimulus on disk
    missing = [t for t in gold
               if not (SRC / "images" / f"phase_noise_{t.rsplit('_n', 1)[1]}"
                       / f"{t.rsplit('_n', 1)[0]}.png").exists()]
    if missing:
        raise SystemExit(f"{len(missing)} stimuli not found, e.g. {missing[:3]}")

    crowd = pd.DataFrame(crowd, columns=["task", "worker", "label"])
    gold = pd.DataFrame(sorted(gold.items()), columns=["task", "true_label"])
    assert gold.task.is_unique
    assert set(crowd.task) == set(gold.task)
    crowd.to_csv(LONG / "imagenet16h_crowd.csv", index=False)
    gold.to_csv(LONG / "imagenet16h_gold.csv", index=False)

    ind = (crowd.label.values == gold.set_index("task").true_label.reindex(crowd.task).values).mean()
    mv = crowd.groupby("task").label.agg(lambda s: s.value_counts().idxmax())
    acc = (mv.reindex(gold.task).values == gold.true_label.values).mean()
    print(f"  imagenet16h  tasks={len(gold):,} (1,200 images x 4 noise levels)  "
          f"workers={crowd.worker.nunique()}  judgments={len(crowd):,} "
          f"({len(crowd)/len(gold):.2f}/task)")
    print(f"               classes={gold.true_label.nunique()}")
    print(f"               individual accuracy={ind:.4f}   majority-vote={acc:.4f}")
    for lvl in sorted({t.rsplit('_n', 1)[1] for t in gold.task}):
        sub = gold[gold.task.str.endswith(f"_n{lvl}")]
        a = (mv.reindex(sub.task).values == sub.true_label.values).mean()
        print(f"               noise {lvl}: MV={a:.4f}  (n={len(sub):,})")


if __name__ == "__main__":
    main()

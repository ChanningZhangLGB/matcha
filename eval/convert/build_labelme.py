#!/usr/bin/env python3
"""Convert datasets_pass/labelme_crowd into crowd-kit long form.

    python eval/convert/build_labelme.py

LabelMe scene classification (Rodrigues & Pereira, AAAI-18): 1,000 training images over
8 classes, labelled by AMT workers. Only the train split has per-annotator labels -- the
valid (500) and test (1,188) splits ship gold but no crowd, so they are not in
datasets_pass and are not represented here.

Emits into eval/data/:
    labelme_crowd.csv   task, worker, label
    labelme_gold.csv    task, true_label

TASK IDS are the image filename stem (`street_hexp30`), so a task maps directly to
`datasets_pass/labelme_crowd/train/<class>/<stem>.jpg` for the VLM annotators. Row i of
answers.txt corresponds to line i of filenames_train.txt / labels_train.txt -- the join is
POSITIONAL, and check() re-asserts that every referenced image exists.

LABELS are class NAMES, not the shipped integer codes. The integer->name map is derived
from the corpus itself (labels_train.txt vs labels_train_names.txt) rather than hard-coded,
and asserted to be one-to-one:
    0 highway  1 insidecity  2 tallbuilding  3 street
    4 forest   5 coast       6 mountain      7 opencountry

WORKERS are positional column indices (`w00`..`w76`) -- answers.txt carries no worker ids.
18 of the 77 columns are ENTIRELY EMPTY and are dropped: an annotator with zero
observations contributes nothing but breaks per-worker parameter estimation in
DawidSkene/GLAD/MACE. Annotation depth is only ~2.55 labels per image, the thinnest in
this project, so those aggregators are weakly determined here regardless.
"""
import collections
import csv
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common.paths import DATA, LONG  # noqa: E402

SRC = pathlib.Path(DATA) / "labelme_crowd"
MISSING = -1


def class_map(codes, names):
    """int -> class name, derived from the corpus and asserted one-to-one."""
    m = collections.defaultdict(set)
    for c, n in zip(codes, names):
        m[c].add(n)
    bad = {k: sorted(v) for k, v in m.items() if len(v) != 1}
    if bad:
        raise SystemExit(f"label code maps to multiple names: {bad}")
    return {k: v.pop() for k, v in m.items()}


def main():
    LONG.mkdir(parents=True, exist_ok=True)
    ans = np.loadtxt(SRC / "answers.txt")
    codes = [int(l) for l in open(SRC / "labels_train.txt")]
    names = [l.strip() for l in open(SRC / "labels_train_names.txt")]
    files = [l.strip() for l in open(SRC / "filenames_train.txt")]
    if not (ans.shape[0] == len(codes) == len(names) == len(files)):
        raise SystemExit(f"row counts differ: answers={ans.shape[0]} labels={len(codes)} "
                         f"names={len(names)} files={len(files)}")

    cmap = class_map(codes, names)
    tasks = [pathlib.Path(f).stem for f in files]
    if len(set(tasks)) != len(tasks):
        raise SystemExit("image stems are not unique -- cannot be task ids")

    # every task must resolve to an image on disk, or the VLM arm silently loses it
    missing = [t for t, n in zip(tasks, names) if not (SRC / "train" / n / f"{t}.jpg").exists()]
    if missing:
        raise SystemExit(f"{len(missing)} images not found, e.g. {missing[:3]}")

    active = [j for j in range(ans.shape[1]) if (ans[:, j] != MISSING).any()]
    empty = ans.shape[1] - len(active)

    crowd = []
    for i, t in enumerate(tasks):
        for j in active:
            v = ans[i, j]
            if v == MISSING:
                continue
            crowd.append((t, f"w{j:02d}", cmap[int(v)]))
    crowd = pd.DataFrame(crowd, columns=["task", "worker", "label"])
    gold = pd.DataFrame({"task": tasks, "true_label": names})

    assert gold.task.is_unique
    assert set(crowd.task) <= set(gold.task)
    crowd.to_csv(LONG / "labelme_crowd.csv", index=False)
    gold.to_csv(LONG / "labelme_gold.csv", index=False)

    # majority vote as a sanity anchor against the published number
    mv = crowd.groupby("task").label.agg(lambda s: s.value_counts().idxmax())
    acc = (mv.reindex(gold.task).values == gold.true_label.values).mean()
    print(f"  labelme  tasks={len(gold):,}  workers={crowd.worker.nunique()} "
          f"({empty} empty columns dropped)  judgments={len(crowd):,} "
          f"({len(crowd)/len(gold):.2f}/task)")
    print(f"           classes={sorted(cmap.values())}")
    print(f"           majority-vote accuracy={acc:.4f}")


if __name__ == "__main__":
    main()

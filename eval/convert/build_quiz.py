#!/usr/bin/env python3
"""Convert datasets_pass/quiz_crowd_li into crowd-kit long form -- ONE combined table.

    python eval/convert/build_quiz.py

Six multiple-choice subsets (Li 2024, ICASSP; Li et al. 2017, CIKM). Each ships
`quiz.csv` (question text + options + key), `answer.csv` (a DENSE worker x question
matrix -- every worker answers every question), and `truth.csv` (the answer key).

The six are pooled into a SINGLE table rather than kept apart: at 20-36 items each they
are far too small to fit per-annotator aggregators on individually (SCIENCE is 111 workers
over 20 items). Pooled, the table is 155 items / 8,930 judgments.

Emits into eval/data/:
    quiz_crowd.csv   task, worker, label
    quiz_gold.csv    task, true_label

JOIN IS POSITIONAL, not by question_id. ENGLISH/quiz.csv retains the original source ids
(1,2,3,4,6,7,8,11,...,59) while its truth.csv and answer.csv were renumbered 1..30, so an
id join silently mismatches 25 of its 30 rows (it agrees on 5 by coincidence). Row order is
consistent across all three files in every subset, so position is the reliable key; the
other five subsets have contiguous ids and join identically either way. `check()` below
re-asserts this every run.

TASK IDS are prefixed per subset (`chi1`, `eng1`, ...) so pooling cannot collide ids.

WORKER IDS are prefixed too (`chi_worker1`). This is not cosmetic: the subsets came from
separate worker pools of different sizes, so `worker1` in CHINESE is not the same person as
`worker1` in SCIENCE. Pooling without the prefix would fuse unrelated annotators into one
confusion matrix and corrupt every per-annotator aggregator.

Label space is the union A-F. It is NOT a shared class space -- "C" means a different
option in every question, and the subsets have different option counts (ITMANAGE/MEDICINE
4, CHINESE/ENGLISH/SCIENCE 5, POKEMON 6). Aggregators that estimate a global class prior or
a full KxK confusion matrix will therefore see a prior that has no meaning across subsets.
See datasets_pass/README.md for the rest of the caveats.
"""
import csv
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.paths import DATA, LONG  # noqa: E402

SRC = Path(DATA) / "quiz_crowd_li" / "Datasets"

# subset -> short task/worker prefix
SUBSETS = {"CHINESE": "chi", "ENGLISH": "eng", "ITMANAGE": "itm",
           "MEDICINE": "med", "POKEMON": "pok", "SCIENCE": "sci"}


def read_subset(name, prefix):
    """-> (crowd rows, gold rows, options) for one subset, joined POSITIONALLY."""
    quiz = list(csv.DictReader(open(SRC / name / "quiz.csv")))
    truth = list(csv.DictReader(open(SRC / name / "truth.csv")))
    ans = list(csv.DictReader(open(SRC / name / "answer.csv")))
    if not len(quiz) == len(truth) == len(ans):
        raise SystemExit(f"{name}: row counts differ "
                         f"quiz={len(quiz)} truth={len(truth)} answer={len(ans)}")

    # Two independent checks that positional alignment is the right join.
    # 1. quiz.csv duplicates the answer key in its own `truth` column, so aligning by
    #    position must reproduce truth.csv exactly. (By ID it does not: ENGLISH matches
    #    only 5 of 30, which is why this join is positional.)
    bad = [i for i, (q, t) in enumerate(zip(quiz, truth))
           if q["truth"].strip() != t["truth"].strip()]
    if bad:
        raise SystemExit(f"{name}: quiz.csv key disagrees with truth.csv at rows {bad}")
    # 2. truth.csv and answer.csv must agree row-for-row on question_id -- these two are
    #    renumbered together, so here position and id have to coincide. Nothing upstream
    #    guarantees it, and a silent drift would misattribute every worker's answers.
    drift = [(t["question_id"], a["question_id"]) for t, a in zip(truth, ans)
             if t["question_id"] != a["question_id"]]
    if drift:
        raise SystemExit(f"{name}: truth.csv/answer.csv question_id drift at {drift[:5]}")

    options = sorted(c for c in quiz[0] if len(c) == 1 and c.isalpha())
    workers = [c for c in ans[0] if c != "question_id"]

    crowd, gold = [], []
    for i, (t, a) in enumerate(zip(truth, ans), start=1):
        task = f"{prefix}{i}"
        gold.append((task, t["truth"].strip()))
        for w in workers:
            v = (a[w] or "").strip()
            if not v:
                continue
            if v not in options:
                raise SystemExit(f"{name} row {i} {w}: '{v}' not in {options}")
            crowd.append((task, f"{prefix}_{w}", v))
    return crowd, gold, options


def main():
    LONG.mkdir(parents=True, exist_ok=True)
    all_c, all_g = [], []
    print(f"  {'subset':10s} {'items':>6s} {'workers':>8s} {'judgments':>10s} {'options':>8s}")
    for name, prefix in SUBSETS.items():
        c, g, opts = read_subset(name, prefix)
        print(f"  {name:10s} {len(g):6d} {len({w for _, w, _ in c}):8d} "
              f"{len(c):10d} {''.join(opts):>8s}")
        all_c += c
        all_g += g

    crowd = pd.DataFrame(all_c, columns=["task", "worker", "label"])
    gold = pd.DataFrame(all_g, columns=["task", "true_label"])
    assert gold.task.is_unique, "task ids collided across subsets"
    assert set(crowd.task) == set(gold.task), "crowd/gold task sets differ"
    crowd.to_csv(LONG / "quiz_crowd.csv", index=False)
    gold.to_csv(LONG / "quiz_gold.csv", index=False)
    print(f"\n  {'quiz (pooled)':18s} tasks={len(gold):5,d}  "
          f"workers={crowd.worker.nunique():5,d}  judgments={len(crowd):7,d}  "
          f"classes={sorted(gold.true_label.unique())}")


if __name__ == "__main__":
    main()

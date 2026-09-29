#!/usr/bin/env python3
"""Pool crowdtruth_cause and crowdtruth_treat into ONE table of binary subtasks.

    python eval/convert/build_crowdtruth_pooled.py

WHY THIS IS ONE DATASET. Both tables come from a single CrowdTruth medical relation
extraction collection, and the evidence that they are one collection is direct:

    treat's 621 sentence ids are a strict SUBSET of cause's 975
    treat's 9,610 (task,worker) cells are a strict SUBSET of cause's 14,920
    286 of 286 treat workers also appear in cause
    gold is mutually exclusive -- of the 621 shared sentences, ZERO are yes to both

So one worker, in one HIT, answered two relation questions about the same sentence,
and one LLM call answers both (score_llm.map_crowdtruth reads [CAUSES]/[TREATS] out of
a single multi-select response).

WHAT THIS SCRIPT DOES -- and what it deliberately does NOT do. It concatenates the two
tables as two binary SUBTASKS, namespacing ids `c<id>` / `t<id>` so a sentence judged
for both relations becomes two independent instances. It does NOT reconstruct the
underlying 3-way question (cause / treat / neither), which would be the more faithful
object but is a different dataset needing fresh prompts and a full regeneration.

TWO CONSEQUENCES THAT MUST BE REPORTED WITH ANY NUMBER FROM THIS TABLE:

 1. DOUBLE WEIGHT. The 621 sentences present in both tables contribute two instances
    each, so they count twice in every accuracy figure. The pooled table is 1,596
    instances over 975 distinct sentences.
 2. CORRELATED JUDGMENTS. A worker's cause and treat answers came from the same HIT
    and are not independent -- 28 of the 9,610 shared cells say yes to BOTH relations
    even though gold never does. crowd-kit aggregators assume conditional independence
    given the true label, so their confusion-matrix estimates are optimistic here.

Base rates also differ between the halves (cause 25.3% yes, treat 47.3% yes); the
pooled prior sits between them and matches neither.

Writes eval/data/crowdtruth_pooled_{gold,crowd}.csv
"""
import collections
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
LONG = ROOT / "eval" / "data"
PREFIX = {"crowdtruth_cause": "c", "crowdtruth_treat": "t"}


def read(name, kind):
    return list(csv.DictReader(open(LONG / f"{name}_{kind}.csv")))


def main():
    gold_rows, crowd_rows = [], []
    stats = {}
    for table, pre in PREFIX.items():
        g = read(table, "gold")
        c = read(table, "crowd")
        gold_rows += [{"task": pre + r["task"], "true_label": r["true_label"]}
                      for r in g]
        crowd_rows += [{"task": pre + r["task"], "worker": r["worker"],
                        "label": r["label"]} for r in c]
        pos = sum(1 for r in g if r["true_label"] == "yes")
        stats[table] = (len(g), len(c), pos / len(g))

    # ---- assertions: catch a namespacing collision or a dropped row -------------
    ids = [r["task"] for r in gold_rows]
    assert len(ids) == len(set(ids)), "id collision after namespacing"
    assert len(gold_rows) == sum(v[0] for v in stats.values())
    assert len(crowd_rows) == sum(v[1] for v in stats.values())
    gold_ids = set(ids)
    orphan = {r["task"] for r in crowd_rows} - gold_ids
    assert not orphan, f"{len(orphan)} crowd ids have no gold row"

    for name, rows, cols in [("gold", gold_rows, ["task", "true_label"]),
                             ("crowd", crowd_rows, ["task", "worker", "label"])]:
        f = LONG / f"crowdtruth_pooled_{name}.csv"
        with open(f, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(f"  {f.relative_to(ROOT)}  ({len(rows):,} rows)")

    print()
    for t, (n, j, p) in stats.items():
        print(f"    {t:18s} {n:5,d} instances  {j:6,d} judgments  {p:5.1%} yes")
    n_g = len(gold_rows)
    pos = sum(1 for r in gold_rows if r["true_label"] == "yes")
    workers = len({r["worker"] for r in crowd_rows})
    print(f"    {'POOLED':18s} {n_g:5,d} instances  {len(crowd_rows):6,d} judgments  "
          f"{pos / n_g:5.1%} yes   ({workers} workers)")
    dup = len(set(r["task"][1:] for r in gold_rows))
    print(f"\n    {n_g:,} instances over {dup:,} distinct sentences "
          f"-- {n_g - dup:,} sentences carry DOUBLE weight")
    jpi = collections.Counter(r["task"] for r in crowd_rows)
    print(f"    judgments per instance: min={min(jpi.values())} "
          f"median={sorted(jpi.values())[len(jpi) // 2]} max={max(jpi.values())}")


if __name__ == "__main__":
    main()

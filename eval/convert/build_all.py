#!/usr/bin/env python3
"""Convert every datasets_pass/ dataset into crowd-kit long form.

Emits, per dataset, into eval/data/:
    <name>_crowd.csv   task, worker, label
    <name>_gold.csv    task, true_label

Datasets produced:
    sentiment          binary sentiment, native
    movie_reviews      ratings binned to poor/medium/good (the `bin` recast)
    conll_ner          BIO tags, one task per token (the `tok` recast)
    crowdtruth_cause   binary "does this sentence express CAUSES?"
    crowdtruth_treat   binary "does this sentence express TREATS?"
    pico               in-span/out-of-span, one task per token (the `tok` recast)
"""
import csv
import glob
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.paths import DATA, LONG, MR_MISSING, bin_rating  # noqa: E402

LONG.mkdir(parents=True, exist_ok=True)


def dump(name, crowd, gold):
    crowd = crowd.dropna(subset=["task", "worker", "label"])
    gold = gold.dropna(subset=["task", "true_label"])
    # keep only tasks that have both crowd labels and gold
    common = set(crowd["task"]) & set(gold["task"])
    crowd = crowd[crowd["task"].isin(common)]
    gold = gold[gold["task"].isin(common)].drop_duplicates("task")
    crowd.to_csv(LONG / f"{name}_crowd.csv", index=False)
    gold.to_csv(LONG / f"{name}_gold.csv", index=False)
    print(f"  {name:18s} tasks={len(gold):7,d}  workers={crowd.worker.nunique():5,d}  "
          f"judgments={len(crowd):9,d}  classes={sorted(map(str, gold.true_label.unique()))[:6]}")


# ---------------------------------------------------------------- sentiment
def build_sentiment():
    src = DATA / "sentiment_polarity_ma_lr" / "mturk_answers.csv"
    df = pd.read_csv(src, dtype=str)
    crowd = df.rename(columns={"Input.id": "task", "WorkerId": "worker",
                               "Answer.sent": "label"})[["task", "worker", "label"]]
    gold = (df.rename(columns={"Input.id": "task", "Input.true_sent": "true_label"})
              [["task", "true_label"]])
    dump("sentiment", crowd, gold)


# ------------------------------------------------------------ movie reviews
def build_movie_reviews():
    d = DATA / "movie_reviews_crowd"
    Y = np.array([[float(x) for x in l.split()] for l in open(d / "answers.txt")])
    gold_r = np.loadtxt(d / "ratings_train.txt")
    assert Y.shape[0] == gold_r.shape[0], (Y.shape, gold_r.shape)
    items, workers = np.where(Y != MR_MISSING)          # -0.1 / 1.1 are valid ratings
    crowd = pd.DataFrame({
        "task": [f"mr{i}" for i in items],
        "worker": [f"w{w}" for w in workers],
        "label": bin_rating(Y[items, workers]),
    })
    gold = pd.DataFrame({"task": [f"mr{i}" for i in range(len(gold_r))],
                         "true_label": bin_rating(gold_r)})
    dump("movie_reviews", crowd, gold)


# ---------------------------------------------------------------- conll ner
def _read_conll(path):
    """Yield (sentence_index, token_index, [columns...])."""
    s = t = 0
    for line in open(path):
        line = line.rstrip("\n")
        if not line.strip():
            if t:
                s, t = s + 1, 0
            continue
        yield s, t, line.split()
        t += 1


def build_conll_ner():
    d = DATA / "conll2003_ner_crowd"
    rows = []
    for s, t, cols in _read_conll(d / "answers.txt"):
        task = f"s{s}_t{t}"
        for r, tag in enumerate(cols[1:]):
            if tag != "?":                              # ? = worker did not annotate
                rows.append((task, f"a{r}", tag))
    crowd = pd.DataFrame(rows, columns=["task", "worker", "label"])
    gold = pd.DataFrame([(f"s{s}_t{t}", cols[1]) for s, t, cols in _read_conll(d / "ground_truth.txt")],
                        columns=["task", "true_label"])
    dump("conll_ner", crowd, gold)


# -------------------------------------------------------------- crowdtruth
def build_crowdtruth():
    d = DATA / "crowdtruth_medical_re"
    relex = []
    for f in sorted(glob.glob(str(d / "raw" / "RelEx" / "*.csv"))):
        relex.extend(csv.DictReader(open(f)))

    for rel, tag, gt_file in [("cause", "CAUSES", "ground_truth_cause.csv"),
                              ("treat", "TREATS", "ground_truth_treat.csv")]:
        rows = {}
        for r in relex:
            sid = str(r.get("sent_id", "")).split("-")[0]
            w = r.get("_worker_id")
            if not sid or not w:
                continue
            sel = (r.get("step_1_select_the_valid_relations") or "").upper()
            yes = f"[{tag}]" in sel
            rows[(sid, w)] = rows.get((sid, w), False) or yes   # OR over term pairs
        crowd = pd.DataFrame([(k[0], k[1], "yes" if v else "no") for k, v in rows.items()],
                             columns=["task", "worker", "label"])
        gold = pd.DataFrame(
            [(r["SID"], "yes" if r["expert"] == "1" else "no")
             for r in csv.DictReader(open(d / gt_file)) if r["expert"] not in ("NA", "")],
            columns=["task", "true_label"])
        dump(f"crowdtruth_{rel}", crowd, gold)


# -------------------------------------------------------------------- pico
def build_pico():
    d = DATA / "pico_data"
    a = d / "annotations" / "acl17-test"
    crowd_ann = [json.loads(l) for l in open(a / "PICO-annos-crowdsourcing.json") if l.strip()]
    gold_ann = {json.loads(l)["docid"]: json.loads(l)["Participants"]
                for l in open(a / "PICO-annos-professional.json") if l.strip()}

    c_rows, g_rows = [], []
    for doc in crowd_ann:
        did = doc["docid"]
        if did not in gold_ann:
            continue
        text = (d / "docs" / f"{did}.txt").read_text()
        toks = [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]
        n = len(text)

        def mask(spans):
            m = np.zeros(n, dtype=bool)
            for s, e in spans:
                m[max(0, s):min(int(e), n)] = True
            return m

        gmask = mask(gold_ann[did].get("MedicalStudent", []))
        for i, (s, e) in enumerate(toks):
            g_rows.append((f"{did}_{i}", "in" if gmask[s:e].any() else "out"))
        # only workers who annotated THIS doc emit labels for its tokens
        for w, spans in doc["Participants"].items():
            wmask = mask(spans)
            for i, (s, e) in enumerate(toks):
                c_rows.append((f"{did}_{i}", w, "in" if wmask[s:e].any() else "out"))

    dump("pico",
         pd.DataFrame(c_rows, columns=["task", "worker", "label"]),
         pd.DataFrame(g_rows, columns=["task", "true_label"]))


if __name__ == "__main__":
    print("building long-form tables ->", LONG)
    build_sentiment()
    build_movie_reviews()
    build_conll_ner()
    build_crowdtruth()
    build_pico()
    print("done")

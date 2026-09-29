#!/usr/bin/env python3
"""Best routed allocation vs the three fixed baselines, per dataset.

    python results/utils/build_allocation_best.py [model]

Writes results/<dataset>/allocation/<model>/best_allocation.csv (one row each)
and upserts this model's rows into results/allocation_best.csv -- ONE combined
table, model x dataset. Columns:

    llm_only        that model's majority vote over its 9 prompt conditions
    human_only      best of the 8 aggregators on the human crowd alone
    human_plus_llm  best of the 8 with the LLM added as one extra annotator
    peak_*          the single best cell over the whole routing sweep, and the
                    condition that produced it (budget, method, uncertainty, route)
    judgments_*     human effort at that allocation, counted as DISTINCT
                    (effort, worker) pairs taken from the peak measure's splits.csv --
                    the exact instances routed, not a prorated share. Effort is in
                    JUDGMENTS, not money: annotator expertise is not uniform across
                    these corpora, so no single wage is defensible. The LLM must label
                    100% of instances to rank them, but contributes ZERO human
                    judgments at any X.
                    acc_vs_human_only is peak_routed - human_only, i.e. what the
                    saving buys or costs in accuracy.

All accuracy. Only models whose allocation sweep is COMPLETE (48 routing files)
are written -- a partial sweep would understate the peak.

Caveat carried in the file: the peak is a maximum over 4 uncertainty measures x
~6 methods x 19 budgets x 2 routes, so part of its margin is selection over noise.
Treat it as an upper bound, not a recommendation.
"""
import collections
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
DATASETS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
            "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"]
# A model is only ever run on ONE arm (except gpt-4o-mini, which is multimodal and
# runs on both). Without this split, incomplete_sweeps() would demand image sweeps
# from the text-only models -- which can never exist -- and silently refuse to write
# their rows, destroying completed text results.
IMAGE_DATASETS = ["labelme", "imagenet16h"]
TEXT_DATASETS = [d for d in DATASETS if d not in IMAGE_DATASETS]
IMAGE_ONLY_MODELS = {"minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"}
TEXT_ONLY_MODELS = {"llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"}


def datasets_for(model):
    """Datasets this model was actually run on."""
    if model in IMAGE_ONLY_MODELS:
        return IMAGE_DATASETS
    if model in TEXT_ONLY_MODELS:
        return TEXT_DATASETS
    return DATASETS          # gpt-4o-mini: multimodal, both arms
MEASURES = ["confidence", "entropy", "inter_rater", "random"]
ROUTES = ["human_only", "human_plus_llm"]
# (no global EXPECTED: completeness is checked per dataset per model,
#  see incomplete_sweeps / datasets_for)
HEADER = ["model", "dataset", "llm_only", "human_only", "human_only_method",
          "human_plus_llm", "human_plus_llm_method",
          "peak_routed", "peak_budget_X", "peak_method",
          "peak_uncertainty", "peak_route",
          # Human effort is counted in JUDGMENTS -- one annotator labelling one
          # instance once -- not in money. Wage and seconds-per-judgment are dropped
          # entirely: annotator expertise varies across these corpora (medical experts
          # on crowdtruth/pico vs open crowds on sentiment/labelme), so a single
          # hourly rate cannot be defended, and ASSUMED_SEC was a guess on 5 of 8
          # datasets. Judgment counts rest on no such assumption.
          "human_judgments_full", "judgments_at_peak", "judgments_saved",
          "judgments_saved_pct", "acc_vs_human_only"]


def effort_key(table, task):
    """The identity of the HUMAN EFFORT behind a row, which is not always the task id.

    crowdtruth_pooled namespaces one sentence into `c<id>` and `t<id>` because it scores
    two relations as separate instances -- but a single CrowdFlower HIT asked BOTH
    questions about that sentence, so the two rows are one act of human annotation, not
    two. Counting rows there overstates the crowd's effort by 64% (24,530 vs 14,920).
    Stripping the namespace collapses them back to the sentence a person actually read.
    """
    return task[1:] if table == "crowdtruth_pooled" else task


def judgments_at(ds, model, measure, X):
    """Human judgments consumed when the top X% by `measure` are routed to humans.

    Counted EXACTLY from splits.csv rather than as n_judgments * X/100: judgments per
    instance are not uniform on any dataset in this study (crowdtruth 15-30 per
    sentence, conll_ner 1-8 per token), so a proportional estimate would be wrong
    wherever routing happens to select instances with unusual annotator counts.
    """
    sp = ddir(ds) / "allocation" / model / measure / "splits.csv"
    cf = ROOT / "eval" / "data" / f"{ds}_crowd.csv"
    if not (sp.exists() and cf.exists()):
        return None, None
    col = f"x{int(X):02d}"
    rows = list(csv.DictReader(open(sp)))
    if col not in rows[0]:
        return None, None
    high = {r["task"] for r in rows if r[col] == "high"}
    # DISTINCT (effort, worker) pairs, not rows: this both collapses the
    # crowdtruth_pooled namespace and drops the 6 duplicate (task, worker) rows in
    # imagenet16h, where one worker labelled the same image twice.
    full, routed = set(), set()
    for r in csv.DictReader(open(cf)):
        pair = (effort_key(ds, r["task"]), r["worker"])
        full.add(pair)
        if r["task"] in high:
            routed.add(pair)
    return len(full), len(routed)



def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def incomplete_sweeps(model):
    """Datasets in DATASETS whose sweep is short of 4 measures x 2 routes.

    Checked PER DATASET, not as a global total. A global count is wrong here: the old
    `RES.glob("*/**/allocation/...")` also matched movie_reviews/REGRESSION, which
    DATASETS does not cover, so the total ran 8 files ahead of the guard. With 6
    datasets that was harmless (48 expected vs 56 matched, and all six really were
    complete); adding a 7th made it actively dangerous -- the guard passed at 58/56
    while quiz held only its 2 random files, which would have written a "peak" derived
    from the random control alone. ddir() resolves movie_reviews to categorical/, so
    the regression track is excluded by construction.
    """
    want = len(MEASURES) * len(ROUTES)
    short = []
    for ds in datasets_for(model):
        n = len(list(ddir(ds).glob(f"allocation/{model}/*/*/routing.csv")))
        if n < want:
            short.append(f"{ds} {n}/{want}")
    return short


def main(model):
    short = incomplete_sweeps(model)
    if short:
        print(f"  {model}: allocation incomplete ({'; '.join(short)}) - skipped")
        return
    collected = []
    for ds in datasets_for(model):
        d = ddir(ds)
        hp = [r for r in csv.DictReader(open(d / "summary_table_human_plus_llm.csv"))
              if r["metric"] == "Acc"]

        def best_of(pool):
            r = next((x for x in hp if x["annotator_pool"] == pool), None)
            if not r:
                return ""
            vals = [(k, float(v)) for k, v in r.items()
                    if k not in ("annotator_pool", "metric") and v]
            return max(vals, key=lambda kv: kv[1]) if vals else ""

        h_m, h_v = best_of("human-only")
        hp_m, hp_v = best_of(f"{model} + human")

        peak = None
        llm = ""
        for meas in MEASURES:
            for rt in ROUTES:
                f = d / "allocation" / model / meas / rt / "routing_pivot_accuracy.csv"
                if not f.exists():
                    continue
                for r in csv.DictReader(open(f)):
                    if not llm and r.get("X=0% (LLM-only)"):
                        llm = r["X=0% (LLM-only)"]
                    for c, v in r.items():
                        if not c.startswith("X=") or "only" in c or not v:
                            continue
                        val = float(v)
                        if peak is None or val > peak[0]:
                            peak = (val, c.strip("X=%"), r["method"], meas, rt)
        if peak is None:
            continue
        pv, px, pm, pmeas, prt = peak

        # ---- human effort at the peak allocation -----------------------------
        jf, jp = judgments_at(ds, model, pmeas, px)
        if jf:
            eff = [f"{jf}", f"{jp}", f"{jf - jp}",
                   f"{100 * (jf - jp) / jf:.1f}%", f"{pv - h_v:+.4f}"]
        else:
            eff = [""] * 5
        row = [model, ds, llm, f"{h_v:.4f}", h_m, f"{hp_v:.4f}", hp_m,
               f"{pv:.4f}", px, pm, pmeas, prt] + eff
        collected.append(row)
        out = d / "allocation" / model / "best_allocation.csv"
        with open(out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(HEADER)
            w.writerow(row)
        extra = (f" | {eff[2]} of {eff[0]} judgments saved ({eff[3]}), "
                 f"acc {eff[4]}" if jf else "")
        print(f"  {ds:18s} peak {pv:.4f} @ X={px}%{extra}")

    # one combined table at the results root: upsert this model's rows
    if collected:
        allf = RES / "allocation_best.csv"
        keep = []
        if allf.exists():
            keep = [[r.get(c, "") for c in HEADER] for r in csv.DictReader(open(allf))
                    if r["model"] != model]
        order = {m: i for i, m in enumerate(
            ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"])}
        rows = keep + collected
        rows.sort(key=lambda r: (order.get(r[0], 99), DATASETS.index(r[1])))
        with open(allf, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(HEADER)
            w.writerows(rows)
        print(f"\n  {allf.relative_to(ROOT)}  ({len(rows)} rows)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

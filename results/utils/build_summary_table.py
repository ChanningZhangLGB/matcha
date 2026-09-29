#!/usr/bin/env python3
"""Per-dataset headline table: Human-only aggregators vs LLM-only.

    python results/build_summary_table.py

Rows are Acc and macro_f1. Columns are the 8 unsupervised crowd-kit aggregators
applied to the HUMAN annotations, then one column per LLM. The LLM column is the
majority vote over that model's (protocol x prompt-strategy) conditions -- the
LLM-side analogue of aggregating multiple human annotators.

Writes results/<dataset>/summary_table.{md,csv}. The CSV carries a two-level header
(section row + method row) to match the intended spreadsheet layout.
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"

DATASETS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
            "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"]
HUMAN = ["DawidSkene", "MajorityVote", "GLAD", "Wawa", "MMSR", "MACE",
         "ZeroBasedSkill", "OneCoinDawidSkene"]
# The TEXT and IMAGE arms use different annotator line-ups -- only gpt-4o-mini is in both
# (it is multimodal). The two text open models cannot see images and the two VLMs were
# never run on text, so a single flat LLMS list silently emitted 1-model image tables.
LLMS_TEXT = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
LLMS_IMAGE = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]
IMAGE_DATASETS = {"labelme", "imagenet16h"}


def llms_for(ds):
    """Annotator line-up for a dataset. See LLMS_TEXT / LLMS_IMAGE above."""
    return LLMS_IMAGE if ds in IMAGE_DATASETS else LLMS_TEXT

def ddir(ds):
    """Output dir for a dataset. movie_reviews is scored under TWO framings, so its
    categorical artefacts live in movie_reviews/categorical/ and the continuous ones
    in movie_reviews/regression/."""
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d



def human(ds):
    f = ddir(ds) / "crowd_aggregation.csv"
    if not f.exists():
        return {}
    return {r["method"]: r for r in csv.DictReader(open(f))}


def combined(ds, model):
    """The 8 aggregators re-run with the LLM added as one extra annotator."""
    f = ddir(ds) / "model_analysis" / model / "combined_aggregation.csv"
    if not f.exists():
        return {}
    return {r["method"]: r for r in csv.DictReader(open(f))}


def llm(ds, model):
    """Majority vote over all conditions for this model, if it exists."""
    f = ddir(ds) / "model_analysis" / model / "majority_vote.csv"
    if not f.exists():
        return None
    for r in csv.DictReader(open(f)):
        if r["condition"].startswith("MAJORITY_VOTE"):
            return r
    return None


def regression_table():
    """movie_reviews second framing: continuous ratings, same two-level layout.

    Human columns are the aggregation methods over the human ratings; the LLM column
    is the MEAN over that model's continuous conditions -- the continuous analogue of
    the majority vote used in the categorical table.
    """
    d = RES / "movie_reviews" / "regression"
    hf = d / "regression_aggregation.csv"
    if not hf.exists():
        return
    H = list(csv.DictReader(open(hf)))
    hcols = [r["method"] for r in H]

    models, mvals = [], []
    for m in LLMS_TEXT:      # regression track is movie_reviews only (text)
        f = d / "model_analysis" / m / "regression.csv"
        if not f.exists():
            continue
        rows = list(csv.DictReader(open(f)))
        agg = next((r for r in rows if r["condition"].startswith("MEAN_of")
                    and "continuous" in r["condition"]), None)
        if agg:
            models.append(m)
            mvals.append(agg)
    # Human+LLM: the same aggregators refit with the LLM as one extra rater
    comb = []
    for m in models:
        f = d / "model_analysis" / m / "combined_regression.csv"
        if not f.exists():
            continue
        rs = [r for r in csv.DictReader(open(f)) if r["pool"] == "human+LLM"]
        if rs:
            comb.append((m, rs))
    cols = hcols + models
    METRICS = [("MAE", "MAE"), ("RMSE", "RMSE"), ("R2", "R2"), ("pearson_r", "r")]

    def val(key):
        return ([f"{float(r[key]):.4f}" for r in H]
                + [f"{float(r[key]):.4f}" for r in mvals])

    with open(d / "summary_table.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["metric"]
                   + [f"human-only: {m}" for m in hcols]
                   + [f"llm-only: {m}" for m in models])
        for key, label in METRICS:
            w.writerow([label] + val(key))

    L = [f"# movie_reviews (regression) - summary", "",
         "Continuous ratings on [0,1]; **not** comparable to the categorical table.  ",
         "**Human-only**: aggregation over the human ratings.  ",
         "**LLM-only**: mean over that model's continuous conditions "
         "(`basic` + `control`; `customized` is a lettered choice and is excluded).", "",
         "| | " + " | ".join(f"**{c}**" for c in cols) + " |",
         "|---|" + "--:|" * len(cols),
         "| | " + " | ".join(["*Human-only*"] + [""] * (len(hcols) - 1)
                             + ["*LLM-only*"] + [""] * (max(len(models) - 1, 0))) + " |"]
    for key, label in METRICS:
        L.append(f"| **{label}** | " + " | ".join(val(key)) + " |")
    L += ["", "Lower MAE/RMSE is better; higher R2/r is better."]
    (d / "summary_table.md").write_text("\n".join(L) + "\n")
    # ---- Human+LLM as its own table: one ROW per model --------------------
    if comb:
        AGG = ["Mean", "EMBias"]          # shipped_DS cannot be re-fitted
        hb = {r["method"]: r for r in H}
        with open(d / "summary_table_human_plus_llm.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["annotator_pool", "metric"] + AGG)
            for key, lab in METRICS:
                w.writerow(["human-only", lab]
                           + [f"{float(hb[a][key]):.4f}" if a in hb else "" for a in AGG])
            for m, rs in comb:
                by = {r["method"]: r for r in rs}
                for key, lab in METRICS:
                    w.writerow([f"{m} + human", lab]
                               + [f"{float(by[a][key]):.4f}" if a in by else ""
                                  for a in AGG])
        K = ["# movie_reviews (regression) - Human + LLM", "",
             "The LLM joins the human raters as **one extra annotator**; the aggregators "
             "are re-fitted on the combined pool.  ",
             "`shipped_DS` is a precomputed artefact and cannot be re-fitted, so it stays "
             "human-only.", "",
             "| model | metric | " + " | ".join(AGG) + " |",
             "|---|---|" + "--:|" * len(AGG)]
        for m, rs in comb:
            by = {r["method"]: r for r in rs}
            for key, lab in METRICS:
                K.append(f"| {m} | {lab} | " + " | ".join(
                    f"{float(by[a][key]):.4f}" if a in by else "" for a in AGG) + " |")
        K += ["", "**Human-only reference**", "",
              "| | " + " | ".join(AGG) + " |", "|---|" + "--:|" * len(AGG)]
        for key, lab in METRICS:
            K.append(f"| {lab} | " + " | ".join(
                f"{float(hb[a][key]):.4f}" if a in hb else "" for a in AGG) + " |")
        K += ["", "Lower MAE/RMSE is better; higher R2/r is better."]
        (d / "summary_table_human_plus_llm.md").write_text("\n".join(K) + "\n")
    print(f"  results/movie_reviews/regression/summary_table.{{md,csv}}  "
          f"({len(hcols)} human + {len(models)} llm)  + human_plus_llm "
          f"({len(comb)} model rows)")


def main():
    for ds in DATASETS:
        H = human(ds)
        if not H:
            continue
        models = [(m, llm(ds, m)) for m in llms_for(ds)]
        models = [(m, r) for m, r in models if r]
        # Human+LLM: the same 8 aggregators, refit with the LLM as one extra annotator
        comb = [(m, combined(ds, m)) for m, _ in models]
        comb = [(m, c) for m, c in comb if c]
        cols = HUMAN + [m for m, _ in models]

        def val(metric):
            out = []
            for meth in HUMAN:
                r = H.get(meth)
                out.append(f"{float(r[metric]):.4f}" if r else "")
            for _, r in models:
                out.append(f"{float(r[metric]):.4f}")
            return out

        acc, f1 = val("accuracy"), val("macro_f1")

        with open(ddir(ds) / "summary_table.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["metric"]
                       + [f"human-only: {m}" for m in HUMAN]
                       + [f"llm-only: {m}" for m, _ in models])
            w.writerow(["Acc"] + acc)
            w.writerow(["macro_f1"] + f1)

        nh = len(HUMAN)
        L = [f"# {ds} - summary", "",
             f"**Human-only**: the 8 unsupervised crowd-kit aggregators over the human "
             f"annotations.  ",
             f"**LLM-only**: majority vote over that model's protocol x prompt-strategy "
             f"conditions.", "",
             "| | " + " | ".join(f"**{c}**" for c in cols) + " |",
             "|---|" + "--:|" * len(cols),
             "| | " + " | ".join(["*Human-only*"] + [""] * (nh - 1)
                                 + ["*LLM-only*"] + [""] * (len(models) - 1)) + " |",
             "| **Acc** | " + " | ".join(acc) + " |",
             "| **macro_f1** | " + " | ".join(f1) + " |"]
        (ddir(ds) / "summary_table.md").write_text("\n".join(L) + "\n")

        # ---- Human+LLM as its own table: one ROW per model ------------------
        if comb:
            with open(ddir(ds) / "summary_table_human_plus_llm.csv", "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["annotator_pool", "metric"] + HUMAN)
                for key, lab in [("accuracy", "Acc"), ("macro_f1", "macro_f1")]:
                    w.writerow(["human-only", lab]
                               + [f"{float(H[x][key]):.4f}" if H.get(x) else ""
                                  for x in HUMAN])
                for m, c in comb:
                    for key, lab in [("accuracy", "Acc"), ("macro_f1", "macro_f1")]:
                        w.writerow([f"{m} + human", lab]
                                   + [f"{float(c[x][key]):.4f}" if c.get(x) else ""
                                      for x in HUMAN])
            K = [f"# {ds} - Human + LLM", "",
                 "The LLM joins the human crowd as **one extra annotator**; all 8 "
                 "aggregators are then re-fitted on the combined pool.  ",
                 "One row per model per metric; compare against the Human-only row of "
                 "`summary_table.md`.", "",
                 "| model | metric | " + " | ".join(HUMAN) + " |",
                 "|---|---|" + "--:|" * len(HUMAN)]
            for m, c in comb:
                for key, lab in [("accuracy", "Acc"), ("macro_f1", "macro_f1")]:
                    K.append(f"| {m} | {lab} | " + " | ".join(
                        f"{float(c[x][key]):.4f}" if c.get(x) else "" for x in HUMAN) + " |")
            K += ["", "**Human-only reference**", "",
                  "| | " + " | ".join(HUMAN) + " |", "|---|" + "--:|" * len(HUMAN),
                  "| Acc | " + " | ".join(f"{float(H[x]['accuracy']):.4f}" if H.get(x) else ""
                                          for x in HUMAN) + " |",
                  "| macro_f1 | " + " | ".join(f"{float(H[x]['macro_f1']):.4f}" if H.get(x) else ""
                                               for x in HUMAN) + " |"]
            (ddir(ds) / "summary_table_human_plus_llm.md").write_text("\n".join(K) + "\n")
        print(f"  results/{ds}/summary_table.{{md,csv}}  ({nh} human + {len(models)} llm)"
              f"  + human_plus_llm ({len(comb)} model rows)")


if __name__ == "__main__":
    main()
    regression_table()

#!/usr/bin/env python3
"""Paper-layout reference tables: one metric column, laid out modality x dataset x model.

    python results/utils/build_reference_table.py [metric ...]

Emits the shape of the submission table -- Text block then Image block, three model
columns each -- so a block can be pasted straight into the spreadsheet. The two blocks
carry DIFFERENT model line-ups (only gpt-4o-mini spans both arms), which is why they
are written as separate blocks rather than one grid with blank cells.

Metrics available now:
    llm_only      9-condition majority vote of that model, accuracy

`crowdtruth` is the POOLED table (cause + treat as two binary subtasks, 1,596
instances over 975 distinct sentences). Its n is therefore not the count of distinct
sentences -- see eval/convert/build_crowdtruth_pooled.py.

Every value is cross-checked against the per-model source file it should equal, and a
mismatch raises rather than being written, so the pasted numbers cannot silently drift
from the artefacts they came from.

Writes results/temp_reference/<metric>.csv and .md
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
OUT = RES / "RQ1"          # was temp_reference; renamed once the tables became RQ1

TEXT_MODELS = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
IMAGE_MODELS = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]
SHORT = {"gpt-4o-mini": "gpt-4o-mini",
         "llama3.1-8b-instruct-q8_0": "llama3.1-8b",
         "qwen2.5-7b-instruct-q8_0": "qwen2.5-7b",
         "minicpm-v-8b-2.6-q8_0": "minicpm-v-8b",
         "qwen2.5vl-7b-q8_0": "qwen2.5vl-7b"}

# (display name, table name) -- crowdtruth shows as one row, backed by the pooled table
BLOCKS = [
    ("Text", TEXT_MODELS, [("sentiment", "sentiment"),
                           ("movie_reviews", "movie_reviews"),
                           ("crowdtruth", "crowdtruth_pooled"),
                           ("conll_ner_5k", "conll_ner_5k"),
                           ("pico_5k", "pico_5k"),
                           ("quiz", "quiz")]),
    ("Image", IMAGE_MODELS, [("labelme", "labelme"),
                             ("imagenet16h", "imagenet16h")]),
]


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def gold_n(table):
    f = ROOT / "eval" / "data" / f"{table}_gold.csv"
    return sum(1 for _ in csv.DictReader(open(f))) if f.exists() else None


def _mv(ds, model):
    """-> (accuracy, coverage) from the per-model 9-condition majority vote."""
    f = ddir(ds) / "model_analysis" / model / "majority_vote.csv"
    if not f.exists():
        return None, None
    for r in csv.DictReader(open(f)):
        return float(r["accuracy"]), float(r["coverage"])
    return None, None


def llm_only(ds, model):
    """Cross-checked against results/overview_human_vs_llm.csv.

    Coverage is carried because it is NOT 1.0 everywhere -- llama on conll_ner_5k
    reaches 0.9910, since unparseable token sequences are rejected rather than padded.
    An accuracy compared across cells with different coverage is comparing different
    denominators, so the number travels with it.
    """
    acc, cov = _mv(ds, model)
    ov = {r["dataset"]: r for r in
          csv.DictReader(open(RES / "overview_human_vs_llm.csv"))}
    ref = ov.get(ds, {}).get(f"llm-only: {model}", "")
    if ref and acc is not None and abs(float(ref) - acc) > 1e-6:
        raise SystemExit(f"MISMATCH {ds}/{model}: majority_vote={acc} overview={ref}")
    return acc, cov


METRICS = {"llm_only": (llm_only, "LLM-only (9-condition majority vote), accuracy")}

# ---------------------------------------------------------------- human-only
AGGREGATORS = ["MajorityVote", "Wawa", "ZeroBasedSkill", "DawidSkene",
               "OneCoinDawidSkene", "GLAD", "MACE", "MMSR"]


def human_only():
    """dataset x aggregator, from results/<ds>/crowd_aggregation.csv.

    "human-only" = the 8 crowd-kit aggregators fit on CROWD WORKER LABELS ALONE: no
    LLM vote in the annotator pool, and no ground truth at fit time (GoldMajorityVote
    is excluded from the pipeline for exactly that reason -- see eval/run_categorical.py).
    Gold enters only to score the aggregated label afterwards.

    This is MODEL-INDEPENDENT. In the submission layout the human-only column sits
    under each model banner, but the value is identical across all three columns of a
    row, because no model participates. Written once here rather than triplicated.

    Both accuracy and macro-F1 are emitted. On the skewed binary tables they diverge
    sharply -- crowdtruth is 33.9% positive and pico_5k more skewed still, so a strong
    accuracy can hide a weak minority class.
    """
    out = OUT / "human_only"
    out.mkdir(parents=True, exist_ok=True)
    for metric in ("accuracy", "macro_f1"):
        csv_rows, md = [], [f"# Human-only (crowd aggregation), {metric}", "",
                            "8 crowd-kit aggregators fit on crowd worker labels only "
                            "-- no LLM, no gold at fit time.", "",
                            "**Model-independent**: the same value applies under all "
                            "three model columns of the submission table.", ""]
        head = ["Modality", "Dataset", "n"] + AGGREGATORS + ["best", "best method"]
        csv_rows.append(head)
        md += ["| Modality | Dataset | n | " + " | ".join(AGGREGATORS)
               + " | best | best method |",
               "|---|---|--:|" + "--:|" * len(AGGREGATORS) + "--:|---|"]
        for block, _models, rows in BLOCKS:
            for disp, table in rows:
                f = ddir(table) / "crowd_aggregation.csv"
                if not f.exists():
                    continue
                got = {r["method"]: float(r[metric])
                       for r in csv.DictReader(open(f))}
                vals = [f"{got[a]:.4f}" if a in got else "" for a in AGGREGATORS]
                bm = max(got, key=got.get)
                n = gold_n(table)
                csv_rows.append([block, disp, f"{n:,}" if n else ""] + vals
                                + [f"{got[bm]:.4f}", bm])
                md.append(f"| {block} | {disp} | {n:,} | " + " | ".join(vals)
                          + f" | **{got[bm]:.4f}** | {bm} |")
        fcsv = out / f"human_only_{metric}.csv"
        with open(fcsv, "w", newline="") as fh:
            csv.writer(fh).writerows(csv_rows)
        (out / f"human_only_{metric}.md").write_text("\n".join(md) + "\n")
        print(f"  {fcsv.relative_to(ROOT)}")
        if metric == "accuracy":
            print("\n".join(md))


def main(metric):
    fn, title = METRICS[metric]
    OUT.mkdir(parents=True, exist_ok=True)
    csv_rows, md = [], [f"# {title}", ""]

    notes = []
    for block, models, rows in BLOCKS:
        head = ["Modality", "Dataset"] + [SHORT[m] for m in models] + ["n"]
        csv_rows.append(head)
        md += [f"**{block}**", "",
               "| Modality | Dataset | " + " | ".join(SHORT[m] for m in models)
               + " | n |",
               "|---|---|" + "--:|" * len(models) + "--:|"]
        for disp, table in rows:
            vals = []
            for m in models:
                a, cov = fn(table, m)
                vals.append("" if a is None else f"{a:.4f}")
                if cov is not None and cov < 0.9999:
                    notes.append(f"{disp}/{SHORT[m]}: coverage {cov:.4f} "
                                 f"-- accuracy is over {cov:.2%} of instances")
            n = gold_n(table)
            n_txt = f"{n:,}" if n else ""
            csv_rows.append([block, disp] + vals + [n_txt])
            md.append(f"| {block} | {disp} | " + " | ".join(vals) + f" | {n_txt} |")
        csv_rows.append([])
        md.append("")
    if notes:
        md += ["**Coverage below 100% — these cells use a smaller denominator:**", ""]
        md += [f"- {t}" for t in notes] + [""]

    f = OUT / f"{metric}.csv"
    with open(f, "w", newline="") as fh:
        csv.writer(fh).writerows(csv_rows)
    (OUT / f"{metric}.md").write_text("\n".join(md) + "\n")
    print(f"  {f.relative_to(ROOT)}")
    print(f"  {(OUT / f'{metric}.md').relative_to(ROOT)}")
    print()
    print("\n".join(md))


def crowd_llm():
    """dataset x aggregator, PER MODEL, from combined_aggregation.csv.

    "Crowd-LLM" = the same 8 aggregators refit on an annotator pool of the crowd
    workers PLUS the LLM as one additional worker. The LLM contributes a single vote
    per instance -- its 9-condition majority-vote label -- so it is one annotator among
    many, not a weighted oracle. Confusion-matrix aggregators (DawidSkene, GLAD, MACE,
    OneCoinDawidSkene) can learn it is more reliable than the average human and
    up-weight it; the vote-counting ones (MajorityVote, Wawa, ZeroBasedSkill) cannot,
    which is why the two families separate on the datasets where the LLM is strong.

    Unlike human-only this IS model-dependent, so one row per (dataset, model).

    Reported STANDALONE: no human-only baseline column and no delta. Each block of the
    submission table is being assembled on its own first, and a delta would also be a
    difference of two maxima (best-of-8 minus best-of-8), which biases positive -- if
    that comparison is wanted later it should be built deliberately, not carried along
    here by default.
    """
    out = OUT / "crowd-LLM"
    out.mkdir(parents=True, exist_ok=True)
    for metric in ("accuracy", "macro_f1"):
        csv_rows, md = [], [f"# Crowd-LLM (crowd workers + LLM as one extra annotator), "
                            f"{metric}", "",
                            "Same 8 aggregators as human-only, refit on a pool of the "
                            "crowd PLUS the LLM's 9-condition majority-vote label as a "
                            "single additional worker.", ""]
        head = (["Modality", "Dataset", "n", "model"]
                + AGGREGATORS + ["best", "best method"])
        csv_rows.append(head)
        md += ["| Modality | Dataset | n | model | "
               + " | ".join(AGGREGATORS) + " | best | best method |",
               "|---|---|--:|---|" + "--:|" * len(AGGREGATORS) + "--:|---|"]
        for block, models, rows in BLOCKS:
            for disp, table in rows:
                n = gold_n(table)
                for m in models:
                    f = (ddir(table) / "model_analysis" / m
                         / "combined_aggregation.csv")
                    if not f.exists():
                        continue
                    got = {r["method"]: float(r[metric])
                           for r in csv.DictReader(open(f))}
                    vals = [f"{got[a]:.4f}" if a in got else "" for a in AGGREGATORS]
                    bm = max(got, key=got.get)
                    csv_rows.append([block, disp, f"{n:,}", SHORT[m]]
                                    + vals + [f"{got[bm]:.4f}", bm])
                    md.append(f"| {block} | {disp} | {n:,} | {SHORT[m]} | "
                              + " | ".join(vals)
                              + f" | **{got[bm]:.4f}** | {bm} |")
        fcsv = out / f"crowd_llm_{metric}.csv"
        with open(fcsv, "w", newline="") as fh:
            csv.writer(fh).writerows(csv_rows)
        (out / f"crowd_llm_{metric}.md").write_text("\n".join(md) + "\n")
        print(f"  {fcsv.relative_to(ROOT)}")
        if metric == "accuracy":
            print("\n".join(md))


# ----------------------------------------------------------------- regression
# movie_reviews is the only dataset scored under a CONTINUOUS framing as well as a
# categorical one. Its metrics (MAE, RMSE, R2) do not share a scale with accuracy, so
# these are companion files rather than extra rows in the accuracy tables.
REG = RES / "movie_reviews" / "regression"
REG_METRICS = ["MAE", "RMSE", "R2"]
REG_AGG = ["Mean", "EMBias"]        # shipped_DS is reference-only, not a paper method
REG_MODELS = TEXT_MODELS


def _fmt(row):
    return [f"{float(row[k]):.4f}" for k in REG_METRICS]


def regression():
    """movie_reviews continuous framing, for all three table blocks.

    LLM-only uses MEAN_of_all_9_conditions ONLY -- the direct analogue of the
    categorical column's 9-condition majority vote, so the two framings describe the
    same annotator.

    The 6-condition variant (basic + control, dropping `customized`) is deliberately NOT
    reported. It exists in the source regression.csv and is better for gpt-4o-mini
    (R2 0.5653 vs 0.4544) because movie_reviews' `customized` prompts reverse the letter
    scale (A = 10 stars) and score R2 < 0 -- the categorical mapper inverts that back,
    a continuous mean cannot. Reporting the 6 would measure a different condition set
    than the categorical column and would not be uniformly favourable anyway (llama and
    qwen are slightly WORSE on 6 than on 9).

    Human-only and Crowd-LLM use Mean and EMBias only, per the paper's method set.
    LOWER is better for MAE/RMSE, HIGHER for R2 -- no `best` column is emitted here,
    because a single winner is not well defined across three metrics of opposite sign.
    """
    lines = ["# movie_reviews - regression (continuous framing)", "",
             "MAE / RMSE lower is better; R2 higher is better. n = 1,498.", ""]

    # ---- LLM-only ----------------------------------------------------------
    lines += ["## LLM-only", "",
              "Mean over all 9 conditions (3 prompt groups x 3 protocols) -- the "
              "continuous analogue of the categorical 9-condition majority vote.", "",
              "| model | conditions | MAE | RMSE | R2 |", "|---|---|--:|--:|--:|"]
    rows_llm = [["model", "conditions"] + REG_METRICS]
    for m in REG_MODELS:
        f = REG / "model_analysis" / m / "regression.csv"
        if not f.exists():
            continue
        got = {r["condition"]: r for r in csv.DictReader(open(f))}
        cond = "MEAN_of_all_9_conditions"
        if cond in got:
            v = _fmt(got[cond])
            rows_llm.append([SHORT[m], "9 conditions"] + v)
            lines.append(f"| {SHORT[m]} | 9 conditions | " + " | ".join(v) + " |")
    lines.append("")

    # ---- human-only --------------------------------------------------------
    # NO model column, deliberately. Human-only aggregation contains no LLM vote, so the
    # crowd result cannot depend on which model a column is labelled with. Repeating the
    # same two rows under three model headers would assert a dependency that does not
    # exist and invite reading them as three separate measurements.
    lines += ["## Human-only (crowd aggregation)", "",
              "No model column: human-only involves no LLM, so this is a single "
              "measurement of the crowd. It applies unchanged wherever the submission "
              "table places a human-only column.", "",
              "| method | MAE | RMSE | R2 |", "|---|--:|--:|--:|"]
    rows_hum = [["method"] + REG_METRICS]
    hum = {r["method"]: r for r in
           csv.DictReader(open(REG / "regression_aggregation.csv"))}
    for a in REG_AGG:
        if a in hum:
            v = _fmt(hum[a])
            rows_hum.append([a] + v)
            lines.append(f"| {a} | " + " | ".join(v) + " |")
    lines.append("")

    # ---- Crowd-LLM ---------------------------------------------------------
    lines += ["## Crowd-LLM (crowd + LLM as one extra annotator)", "",
              "| model | method | MAE | RMSE | R2 |", "|---|---|--:|--:|--:|"]
    rows_cl = [["model", "method"] + REG_METRICS]
    for m in REG_MODELS:
        f = REG / "model_analysis" / m / "combined_regression.csv"
        if not f.exists():
            continue
        got = {(r["method"], r["pool"]): r for r in csv.DictReader(open(f))}
        for a in REG_AGG:
            r = got.get((a, "human+LLM"))
            if r:
                v = _fmt(r)
                rows_cl.append([SHORT[m], a] + v)
                lines.append(f"| {SHORT[m]} | {a} | " + " | ".join(v) + " |")

    for sub, rows, name in [(".", rows_llm, "llm_only_regression"),
                            ("human_only", rows_hum, "human_only_regression"),
                            ("crowd-LLM", rows_cl, "crowd_llm_regression")]:
        d = OUT / sub
        d.mkdir(parents=True, exist_ok=True)
        with open(d / f"{name}.csv", "w", newline="") as fh:
            csv.writer(fh).writerows(rows)
        print(f"  {(d / f'{name}.csv').relative_to(ROOT)}")
    (OUT / "movie_reviews_regression.md").write_text("\n".join(lines) + "\n")
    print(f"  {(OUT / 'movie_reviews_regression.md').relative_to(ROOT)}\n")
    print("\n".join(lines))


def rq1_human_only():
    """RQ1: the best human-only (crowd-alone) result per dataset, with its aggregator.

    Writes results/RQ1/human_only/.

    "Best" is a MAXIMUM OVER 8 AGGREGATORS chosen on the same gold it is scored
    against -- there is no held-out selection. That is an optimistic estimate of what
    the crowd can do, not an estimate of what a practitioner would achieve picking a
    method in advance. The per-aggregator spread is carried in the `range` column so
    the size of that advantage is visible: where the spread is wide (quiz) the choice
    of aggregator matters more than the crowd itself.
    """
    out = RES / "RQ1" / "human_only"
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# RQ1 - Human-only (crowd aggregation): best per dataset", "",
             "8 crowd-kit aggregators fit on crowd worker labels ONLY -- no LLM in the "
             "pool, no gold at fit time (GoldMajorityVote is excluded from the pipeline "
             "for that reason). Gold is used only to score.", "",
             "`best` is a max over the 8 methods selected on the scoring gold, so it is "
             "an upper bound; `range` is max - min across the 8.", ""]
    rows = [["Modality", "Dataset", "n", "metric", "best", "best method",
             "worst", "worst method", "range"]]
    for metric in ("accuracy", "macro_f1"):
        lines += [f"## {metric}", "",
                  "| Modality | Dataset | n | best | best method | range across 8 |",
                  "|---|---|--:|--:|---|--:|"]
        for block, _models, brows in BLOCKS:
            for disp, table in brows:
                f = ddir(table) / "crowd_aggregation.csv"
                if not f.exists():
                    continue
                got = {r["method"]: float(r[metric]) for r in csv.DictReader(open(f))}
                bm, wm = max(got, key=got.get), min(got, key=got.get)
                n = gold_n(table)
                rng = got[bm] - got[wm]
                rows.append([block, disp, f"{n:,}", metric, f"{got[bm]:.4f}", bm,
                             f"{got[wm]:.4f}", wm, f"{rng:.4f}"])
                lines.append(f"| {block} | {disp} | {n:,} | **{got[bm]:.4f}** | {bm} "
                             f"| {rng:.4f} |")
        lines.append("")

    # movie_reviews regression is NOT duplicated here -- regression() owns it and
    # writes human_only/human_only_regression.csv. Emitting a second copy under a
    # different name is how the two files drifted apart in the first place.
    with open(out / "human_only_best.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    (out / "human_only_best.md").write_text("\n".join(lines) + "\n")
    for p in ("human_only_best.csv", "human_only_best.md"):
        print(f"  {(out / p).relative_to(ROOT)}")
    print()
    print("\n".join(lines))


def rq1_crowd_llm_best():
    """RQ1: best Crowd-LLM result per (dataset, model), with its aggregator.

    Writes results/RQ1/crowd-LLM/crowd_llm_best.{csv,md}. Mirrors rq1_human_only, and
    carries the same caveat: `best` is a max over 8 aggregators selected on the gold it
    is scored against, so it is an upper bound rather than what choosing a method in
    advance would give. `range` shows how much of the value is that selection.

    No human-only baseline and no delta -- the blocks are still being assembled
    separately, and a delta between two best-of-8 maxima biases positive.

    Regression is not duplicated here; regression() owns crowd_llm_regression.csv, and
    a single `best` is undefined across MAE/RMSE/R2 anyway.
    """
    out = OUT / "crowd-LLM"
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# RQ1 - Crowd-LLM: best per dataset and model", "",
             "8 crowd-kit aggregators refit on the crowd PLUS the LLM's 9-condition "
             "majority-vote label as one additional annotator.", "",
             "`best` is a max over the 8 methods selected on the scoring gold, so it is "
             "an upper bound; `range` is max - min across the 8.", ""]
    rows = [["Modality", "Dataset", "n", "model", "metric", "best", "best method",
             "worst", "worst method", "range"]]
    for metric in ("accuracy", "macro_f1"):
        lines += [f"## {metric}", "",
                  "| Modality | Dataset | n | model | best | best method "
                  "| range across 8 |",
                  "|---|---|--:|---|--:|---|--:|"]
        for block, models, brows in BLOCKS:
            for disp, table in brows:
                n = gold_n(table)
                for m in models:
                    f = (ddir(table) / "model_analysis" / m
                         / "combined_aggregation.csv")
                    if not f.exists():
                        continue
                    got = {r["method"]: float(r[metric])
                           for r in csv.DictReader(open(f))}
                    bm, wm = max(got, key=got.get), min(got, key=got.get)
                    rng = got[bm] - got[wm]
                    rows.append([block, disp, f"{n:,}", SHORT[m], metric,
                                 f"{got[bm]:.4f}", bm, f"{got[wm]:.4f}", wm,
                                 f"{rng:.4f}"])
                    lines.append(f"| {block} | {disp} | {n:,} | {SHORT[m]} "
                                 f"| **{got[bm]:.4f}** | {bm} | {rng:.4f} |")
        lines.append("")

    with open(out / "crowd_llm_best.csv", "w", newline="") as fh:
        csv.writer(fh).writerows(rows)
    (out / "crowd_llm_best.md").write_text("\n".join(lines) + "\n")
    for p in ("crowd_llm_best.csv", "crowd_llm_best.md"):
        print(f"  {(out / p).relative_to(ROOT)}")
    print()
    print("\n".join(lines))


if __name__ == "__main__":
    for _m in (sys.argv[1:] or ["llm_only"]):
        if _m in ("rq1_crowd_llm", "rq1_crowd_llm_best"):
            rq1_crowd_llm_best()
        elif _m in ("rq1_human_only", "rq1"):
            rq1_human_only()
        elif _m == "regression":
            regression()
        elif _m == "human_only":
            human_only()
        elif _m in ("crowd_llm", "crowd-llm", "crowd-LLM"):
            crowd_llm()
        else:
            main(_m)

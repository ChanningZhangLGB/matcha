#!/usr/bin/env python3
"""Write results/<dataset>/crowd_aggregation.{md,csv} - the human-crowd baseline.

For each dataset: the corpus statistics, the gold label distribution, and the eight
unsupervised crowd-kit aggregators scored against ground truth. This is the human
side of the comparison; LLM annotator results land alongside it later.
"""
import collections
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
LONG = ROOT / "eval" / "data"
RES = ROOT / "results"

ORDER = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
         "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"]

UNIT = {"sentiment": "sentences", "movie_reviews": "reviews",
        "crowdtruth_cause": "sentences", "crowdtruth_treat": "sentences",
        "crowdtruth_pooled": "sentence-relation pairs",
        "conll_ner_5k": "tokens (from 392 sentences)",
        "pico_5k": "tokens (from 22 abstracts)",
        "quiz": "multiple-choice questions (6 subsets pooled)",
        "labelme": "images (8-way scene classification)",
        "imagenet16h": "images (16-way object classification; image x noise level)"}

RECAST = {"sentiment": "none - native task/worker/label",
          "movie_reviews": "**bin** - ratings [0,1] -> poor / medium / good",
          "crowdtruth_cause": "none - RelEx multi-select reduced to binary [CAUSES]",
          "crowdtruth_treat": "none - RelEx multi-select reduced to binary [TREATS]",
          "crowdtruth_pooled": "cause+treat pooled as two binary subtasks; 621 sentences counted twice",
          "conll_ner_5k": "**tok** - one task per token; 392 of 5,985 sentences, seed 42",
          "pico_5k": "**tok** - one task per token; 22 of 191 gold abstracts, seed 42",
          "quiz": "none - native task/worker/label; 6 subsets pooled, ids and worker "
                  "ids namespaced per subset (separate worker pools)",
          "labelme": "none - native task/worker/label; 18 all-empty worker columns "
                     "dropped at melt time",
          "imagenet16h": "none - native task/worker/label; instance unit is "
                         "(image x phase-noise level), 1,200 x 4"}

GOLD_SRC = {"sentiment": "Pang & Lee polarity label (from review star rating)",
            "movie_reviews": "the review author's own rating",
            "crowdtruth_cause": "medical expert judgement",
            "crowdtruth_treat": "medical expert judgement",
            "crowdtruth_pooled": "medical expert judgement",
            "conll_ner_5k": "original CoNLL-2003 expert annotation",
            "pico_5k": "a single professional annotator (`MedicalStudent`)",
            "quiz": "the quiz answer key (truth.csv)",
            "labelme": "the original LabelMe scene class",
            "imagenet16h": "the true ImageNet category"}

METRICS = ["accuracy", "macro_f1", "weighted_f1"]

def ddir(ds):
    """Output dir for a dataset. movie_reviews is scored under TWO framings, so its
    categorical artefacts live in movie_reviews/categorical/ and the continuous ones
    in movie_reviews/regression/."""
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d



def load_results():
    rows = list(csv.DictReader(open(ROOT / "eval" / "results" / "categorical.csv")))
    by = collections.defaultdict(list)
    for r in rows:
        by[r["dataset"]].append(r)
    return by


def stats(ds):
    crowd = list(csv.DictReader(open(LONG / f"{ds}_crowd.csv")))
    gold = list(csv.DictReader(open(LONG / f"{ds}_gold.csv")))
    dist = collections.Counter(r["true_label"] for r in gold)
    return {
        "tasks": len(gold),
        "workers": len({r["worker"] for r in crowd}),
        "judgments": len(crowd),
        "per_task": len(crowd) / max(len(gold), 1),
        "classes": len(dist),
        "dist": dist,
    }


def main():
    by = load_results()
    for ds in ORDER:
        d = ddir(ds)
        d.mkdir(parents=True, exist_ok=True)
        s = stats(ds)
        rows = by[ds]
        extra = [c for c in rows[0] if c.startswith("f1_") and rows[0][c]]
        cols = METRICS + extra
        rows = sorted(rows, key=lambda r: -float(r["macro_f1"]))

        # csv
        with open(d / "crowd_aggregation.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["method"] + cols + ["seconds"])
            for r in rows:
                w.writerow([r["method"]] + [r[c] for c in cols] + [r["seconds"]])

        # md
        best, worst = rows[0], rows[-1]
        total = sum(s["dist"].values())
        L = [f"# {ds} - crowd aggregation vs ground truth", "",
             "## Corpus", "",
             f"| | |", "|---|---|",
             f"| Instances (tasks scored) | **{s['tasks']:,}** {UNIT[ds]} |",
             f"| Annotators | {s['workers']:,} |",
             f"| Judgments | {s['judgments']:,} ({s['per_task']:.2f} per instance) |",
             f"| Classes | {s['classes']} |",
             f"| Recast | {RECAST[ds]} |",
             f"| Ground truth | {GOLD_SRC[ds]} |", "",
             "**Gold label distribution**", "", "| Label | n | % |", "|---|--:|--:|"]
        for k, v in s["dist"].most_common():
            L.append(f"| `{k}` | {v:,} | {100*v/total:.1f}% |")
        L += ["", "## Aggregators (8 unsupervised crowd-kit methods)", "",
              "Sorted by macro-F1. GoldMajorityVote is excluded: it consumes ground "
              "truth at `fit()`.", "",
              "| Method | " + " | ".join(c.replace("_", "-") for c in cols) + " | sec |",
              "|---|" + "--:|" * (len(cols) + 1)]
        for r in rows:
            cells = " | ".join(f"{float(r[c]):.4f}" for c in cols)
            L.append(f"| {r['method']} | {cells} | {float(r['seconds']):.1f} |")
        L += ["", f"**Best:** {best['method']} (macro-F1 {float(best['macro_f1']):.4f})  ",
              f"**Worst:** {worst['method']} (macro-F1 {float(worst['macro_f1']):.4f})  ",
              f"**Spread:** {float(best['macro_f1'])-float(worst['macro_f1']):.4f}"]

        # accuracy vs macro-F1 disagreement is the thing most likely to mislead
        acc_best = max(rows, key=lambda r: float(r["accuracy"]))
        if acc_best["method"] != best["method"]:
            L += ["", f"> **Accuracy ranks differently.** Top accuracy is "
                      f"{acc_best['method']} ({float(acc_best['accuracy']):.4f}) while "
                      f"{best['method']} leads macro-F1. With this class balance, "
                      f"accuracy is the misleading metric - report macro-F1."]
        (d / "crowd_aggregation.md").write_text("\n".join(L) + "\n")
        print(f"  results/{ds}/crowd_aggregation.{{md,csv}}  "
              f"({s['tasks']:,} tasks, best={best['method']})")


if __name__ == "__main__":
    main()

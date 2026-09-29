#!/usr/bin/env python3
"""Majority-vote across every (protocol x prompt-strategy) condition for one model.

    python results/build_majority_vote.py gpt-4o-mini

Each condition is one prompt file run under one protocol, so for a given model each
instance receives up to 9 labels (3 protocols x 3 strategies). Sentiment's customized
prompt is True/False asked twice (counterbalanced), so it contributes 2 conditions per
protocol, giving 12 there.

The vote is per instance, over whichever conditions produced a usable label.
Ties break deterministically on the alphabetically-first label, so the result is
reproducible; the tie count is reported so it can be checked.

Writes results/<dataset>/<model>_majority_vote.{md,csv} and appends the row to
<model>_prompt_comparison.md.
"""
import collections
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval" / "llm"))
sys.path.insert(0, str(ROOT / "eval"))
from common.metrics import categorical_metrics                      # noqa: E402
import score_llm as S                                               # noqa: E402

RES = ROOT / "results"
PROTOS = ["vanilla", "cot", "topk"]
GROUPS = {"basic_instruction": "basic", "control": "control", "customized": "customized"}
# eval table -> the generation dataset that feeds it
SOURCE = {"sentiment": "sentiment", "movie_reviews": "movie_reviews",
          "crowdtruth_cause": "crowdtruth", "crowdtruth_treat": "crowdtruth",
          "crowdtruth_pooled": "crowdtruth",
          "conll_ner_5k": "conll_ner", "pico_5k": "pico", "quiz": "quiz",
          "labelme": "labelme", "imagenet16h": "imagenet16h"}

def ddir(ds):
    """Output dir for a dataset. movie_reviews is scored under TWO framings, so its
    categorical artefacts live in movie_reviews/categorical/ and the continuous ones
    in movie_reviews/regression/."""
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def mdir(ds, model, base=None):
    """Per-model output dir: <dataset>/model_analysis/<model>/ (created on demand)."""
    d = (base or ddir(ds)) / "model_analysis" / model
    d.mkdir(parents=True, exist_ok=True)
    return d




def predictions(model, table):
    """-> {condition_name: {task: label}} across all groups x protocols."""
    ds = SOURCE[table]
    out = {}
    for group, short in GROUPS.items():
        fn = S.MAPPERS_BY_GROUP.get(group, {}).get(ds, S.MAPPERS[ds])
        for proto in PROTOS:
            recs = S.read(model, group, ds, proto)
            if not recs:
                continue
            res = fn(recs, proto)
            tables = res[0] if isinstance(res, tuple) else res
            pred = tables.get(table)
            if not pred:
                continue
            # a mapper may split into sub-conditions (sentiment true/false)
            if isinstance(next(iter(pred.values())), dict):
                for cond, cp in pred.items():
                    out[f"{short}/{proto}[{cond}]"] = cp
            else:
                out[f"{short}/{proto}"] = pred
    return out


def vote(conds):
    """Per-task majority vote. Ties -> alphabetically first label (deterministic)."""
    tally = collections.defaultdict(collections.Counter)
    for pred in conds.values():
        for t, lab in pred.items():
            tally[t][lab] += 1
    voted, ties = {}, 0
    for t, c in tally.items():
        top = max(c.values())
        winners = sorted(k for k, v in c.items() if v == top)
        if len(winners) > 1:
            ties += 1
        voted[t] = winners[0]
    return voted, ties


def main(model):
    for table in SOURCE:
        gold_f = ROOT / "eval" / "data" / f"{table}_gold.csv"
        gold = {r["task"]: r["true_label"] for r in csv.DictReader(open(gold_f))}
        conds = predictions(model, table)
        if not conds:
            continue
        voted, ties = vote(conds)
        ids = [i for i in gold if i in voted]
        if not ids:
            continue
        m = categorical_metrics([gold[i] for i in ids], [voted[i] for i in ids],
                                positive=S.POSITIVE.get(table))
        cov = len(ids) / len(gold)

        # per-condition accuracy, for context
        per = []
        for name, pred in sorted(conds.items()):
            cid = [i for i in gold if i in pred]
            if not cid:
                continue
            cm = categorical_metrics([gold[i] for i in cid], [pred[i] for i in cid],
                                     positive=S.POSITIVE.get(table))
            per.append((name, cm["accuracy"], cm["macro_f1"], len(cid) / len(gold)))

        best = max(per, key=lambda r: r[1])
        L = [f"# {table} - {model}: majority vote across conditions", "",
             f"Each (protocol x prompt-strategy) pair is one condition; **{len(conds)} "
             f"conditions** vote per instance.",
             f"Ties break on the alphabetically-first label ({ties:,} ties).", "",
             "| | accuracy | macro-F1 | coverage |", "|---|--:|--:|--:|",
             f"| **Majority vote ({len(conds)} conditions)** | **{m['accuracy']:.4f}** | "
             f"**{m['macro_f1']:.4f}** | {100*cov:.1f}% |",
             f"| best single condition (`{best[0]}`) | {best[1]:.4f} | {best[2]:.4f} | "
             f"{100*best[3]:.1f}% |", "",
             "## Conditions that voted", "",
             "| condition | accuracy | macro-F1 | coverage |", "|---|--:|--:|--:|"]
        for name, acc, f1, c in per:
            L.append(f"| {name} | {acc:.4f} | {f1:.4f} | {100*c:.1f}% |")

        cf = ddir(table) / "crowd_aggregation.csv"
        if cf.exists():
            rs = list(csv.DictReader(open(cf)))
            cb = max(rs, key=lambda r: float(r["macro_f1"]))
            L += ["", f"**Crowd baseline**: {cb['method']} accuracy "
                      f"{float(cb['accuracy']):.4f}, macro-F1 {float(cb['macro_f1']):.4f}"]

        (mdir(table, model) / "majority_vote.md").write_text("\n".join(L) + "\n")
        with open(mdir(table, model) / "majority_vote.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["condition", "accuracy", "macro_f1", "coverage"])
            w.writerow([f"MAJORITY_VOTE_{len(conds)}", f"{m['accuracy']:.4f}",
                        f"{m['macro_f1']:.4f}", f"{cov:.4f}"])
            for name, acc, f1, c in per:
                w.writerow([name, f"{acc:.4f}", f"{f1:.4f}", f"{c:.4f}"])

        # append to the protocol x strategy table
        pc = mdir(table, model) / "prompt_comparison.md"
        if pc.exists():
            txt = pc.read_text()
            marker = "\n## Majority vote"
            if marker in txt:
                txt = txt[:txt.index(marker)]
            txt += (f"{marker} across all {len(conds)} conditions\n\n"
                    f"| | accuracy | macro-F1 | coverage |\n|---|--:|--:|--:|\n"
                    f"| Majority vote | **{m['accuracy']:.4f}** | **{m['macro_f1']:.4f}** "
                    f"| {100*cov:.1f}% |\n")
            pc.write_text(txt)
        print(f"  {table:18s} {len(conds):2d} conditions  acc={m['accuracy']:.4f} "
              f"macroF1={m['macro_f1']:.4f}  cov={100*cov:.1f}%  ties={ties:,}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

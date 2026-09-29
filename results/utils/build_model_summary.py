#!/usr/bin/env python3
"""Per-dataset protocol x prompt-strategy table for one model.

    python results/build_model_summary.py gpt-4o-mini

Writes results/<dataset>/<model>_prompt_comparison.{md,csv}: rows are the three
protocols (Vanilla / CoT / Top-K), columns the three prompt strategies
(basic / control / customized).
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
DATASETS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
            "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"]
GROUPS = ["basic", "control", "customized"]
PROTOS = ["vanilla", "cot", "topk"]
NICE = {"vanilla": "Vanilla", "cot": "CoT", "topk": "Top-K"}

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




def read(ds, group, model):
    f = ddir(ds) / "model_analysis" / model / "llm" / f"{group}.csv"
    if not f.exists():
        return {}
    return {r["protocol"]: r for r in csv.DictReader(open(f))}


def cell(rows, proto, field):
    """Exact match first; else any sub-condition of that protocol (e.g. sentiment
    True/False splits into `vanilla [assert=positive]` / `[assert=negative]`)."""
    if proto in rows:
        return [(None, rows[proto][field])]
    subs = [(k[len(proto):].strip(), v[field]) for k, v in rows.items()
            if k.startswith(proto + " ")]
    return sorted(subs) or [(None, None)]


def main(model):
    for ds in DATASETS:
        data = {g: read(ds, g, model) for g in GROUPS}
        if not any(data.values()):
            continue
        crowd = None
        cf = ddir(ds) / "crowd_aggregation.csv"
        if cf.exists():
            rs = list(csv.DictReader(open(cf)))
            crowd = max(rs, key=lambda r: float(r["macro_f1"]))

        L = [f"# {ds} - {model}: protocol x prompt strategy", "",
             "Accuracy of the model as a single annotator, scored against ground truth.",
             "`control` = paraphrase; `customized` = the task-fitted manipulation.", ""]

        for field, title in [("accuracy", "Accuracy"), ("macro_f1", "Macro-F1")]:
            L += [f"## {title}", "",
                  "| Protocol | basic | control | customized |", "|---|--:|--:|--:|"]
            multi = False
            for proto in PROTOS:
                cells = []
                for g in GROUPS:
                    vals = cell(data[g], proto, field)
                    if len(vals) > 1:
                        multi = True
                        cells.append(" / ".join(
                            "-" if v is None else f"{float(v):.4f}" for _, v in vals))
                    else:
                        v = vals[0][1]
                        cells.append("-" if v is None else f"{float(v):.4f}")
                L.append(f"| {NICE[proto]} | " + " | ".join(cells) + " |")
            if multi:
                L += ["", "*sentiment `customized` is True/False asked twice, counterbalanced;*",
                      "*the two values are `assert=negative / assert=positive`.*"]
            L.append("")

        # coverage, only where it is not 100%
        low = []
        for g in GROUPS:
            for p, r in sorted(data[g].items()):
                c = float(r.get("coverage", 1))
                if c < 0.999:
                    low.append(f"| {g} | {p} | {100*c:.1f}% | {int(r['n_scored']):,}/"
                               f"{int(r['n_gold']):,} |")
        if low:
            L += ["## Coverage below 100%", "",
                  "Records the model failed to produce are dropped, so these cells are scored",
                  "on a subset - read them alongside the metric, not as equivalent.", "",
                  "| strategy | protocol | coverage | scored |", "|---|---|--:|--:|"] + low + [""]

        if crowd:
            L += [f"**Crowd baseline** (best of 8 aggregators): {crowd['method']} "
                  f"accuracy {float(crowd['accuracy']):.4f}, "
                  f"macro-F1 {float(crowd['macro_f1']):.4f}"]

        (mdir(ds, model) / "prompt_comparison.md").write_text("\n".join(L) + "\n")

        with open(mdir(ds, model) / "prompt_comparison.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["protocol", "metric"] + GROUPS)
            for field in ("accuracy", "macro_f1"):
                for proto in PROTOS:
                    variants = {g: cell(data[g], proto, field) for g in GROUPS}
                    n = max(len(v) for v in variants.values())
                    for i in range(n):
                        tag = next((variants[g][i][0] for g in GROUPS
                                    if i < len(variants[g]) and variants[g][i][0]), "")
                        row = [proto + (f" {tag}" if tag else ""), field]
                        for g in GROUPS:
                            v = variants[g]
                            got = v[i] if i < len(v) else (None, None)
                            row.append("" if got[1] is None else f"{float(got[1]):.4f}")
                        w.writerow(row)
        print(f"  results/{ds}/model_analysis/{model}/prompt_comparison.{{md,csv}}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

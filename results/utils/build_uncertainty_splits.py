#!/usr/bin/env python3
"""Rank-based X% / (1-X)% splits of each dataset, one per uncertainty measure.

    python results/build_uncertainty_splits.py gpt-4o-mini

For each measure the instances are ranked by uncertainty (most uncertain first) and
cut at a POSITION, not at a value: the "high" batch is the top X% of the dataset by
count, the "low" batch is the remaining (1-X)%. X sweeps 5..95 in steps of 5.

Ties are pervasive in two of the three measures -- entropy and pairwise agreement can
only take a few distinct values over k conditions, and most instances sit at exactly
0. Ranking therefore cannot separate instances inside a tie group, so a cut that falls
inside one is arbitrary with respect to uncertainty. The manifest records, for every X,
how much of the cut lands inside a tie group, so an arbitrary split is never mistaken
for an informative one. Tie order is broken deterministically by task id.

Writes, under results/<dataset>/allocation/<model>/<measure>/:
    splits.csv     task, u, rank, pct_rank, x05 ... x95  (high|low)
    manifest.md    cut value, tie diagnostics per X

The ranking is MODEL-SPECIFIC -- each model has its own uncertainty -- so the
filenames carry the model. A shared splits.csv would silently let one model
overwrite another and route by the wrong ranking.
"""
import collections
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
DATASETS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
            "conll_ner_5k", "pico_5k", "quiz", "labelme", "imagenet16h"]
MEASURES = [("u_confidence", "confidence"), ("u_entropy", "entropy"),
            ("u_agreement", "inter_rater")]
XS = list(range(5, 100, 5))          # 5,10,...,95


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def main(model):
    for ds in DATASETS:
        base = ddir(ds)
        src = base / "model_analysis" / model / "uncertainty_per_instance.csv"
        if not src.exists():
            print(f"  {ds}: no per-instance uncertainty, skipped")
            continue
        rows = list(csv.DictReader(open(src)))

        for col, folder in MEASURES:
            vals = [(r["task"], float(r[col])) for r in rows if r[col] not in ("", None)]
            if not vals:
                print(f"  {ds}/{folder}: column empty, skipped")
                continue
            n = len(vals)
            # most uncertain first; task id breaks ties deterministically
            vals.sort(key=lambda tv: (-tv[1], tv[0]))
            tasks = [t for t, _ in vals]
            us = [u for _, u in vals]
            rank = {t: i + 1 for i, t in enumerate(tasks)}

            out = base / "allocation" / model / folder
            out.mkdir(parents=True, exist_ok=True)

            cuts = {}
            for x in XS:
                k = max(1, min(n - 1, round(n * x / 100)))   # both batches non-empty
                cuts[x] = k

            with open(out / "splits.csv", "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["task", "u", "rank", "pct_rank"] + [f"x{x:02d}" for x in XS])
                for i, t in enumerate(tasks):
                    w.writerow([t, f"{us[i]:.6f}", i + 1, f"{100*(i+1)/n:.4f}"]
                               + ["high" if i < cuts[x] else "low" for x in XS])

            # tie diagnostics: does the cut fall inside a run of equal values?
            grp = collections.Counter(us)
            lines = [f"# {ds} / {folder} — rank-based splits ({model})", "",
                     f"{n:,} instances ranked by `{col}`, most uncertain first.",
                     f"Cut is positional: the **high** batch is the top X% by count.",
                     f"Distinct uncertainty values: **{len(grp)}**"
                     f"{' (heavily tied)' if len(grp) <= 12 else ''}", ""]
            zero = sum(1 for u in us if u == 0.0)
            if zero:
                lines += [f"⚠️ **{zero:,} instances ({100*zero/n:.1f}%) sit at u = 0.**"
                          f" Any cut beyond the {100*(n-zero)/n:.1f}% mark divides that"
                          f" block arbitrarily.", ""]
            lines += ["| X | high n | low n | u at cut | cut inside a tie group? |",
                      "|--:|--:|--:|--:|---|"]
            for x in XS:
                k = cuts[x]
                u_cut = us[k - 1]
                tied = (k < n and us[k] == u_cut)
                same = grp[u_cut]
                note = (f"yes — {same:,} share u={u_cut:.4f}" if tied else "no")
                lines.append(f"| {x}% | {k:,} | {n-k:,} | {u_cut:.4f} | {note} |")
            (out / "manifest.md").write_text("\n".join(lines) + "\n")

            arb = sum(1 for x in XS if cuts[x] < n and us[cuts[x]] == us[cuts[x] - 1])
            print(f"  {ds:18s} {folder:11s} n={n:5,d}  distinct_u={len(grp):3d}  "
                  f"u=0: {100*zero/n:5.1f}%   arbitrary cuts: {arb}/{len(XS)}")

    print("\nnote: movie_reviews/regression has no per-instance uncertainty yet "
          "(needs continuous-measure definitions)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

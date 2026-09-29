#!/usr/bin/env python3
"""Per-instance uncertainty for the REGRESSION track (movie_reviews).

    python eval/llm/uncertainty_regression.py gpt-4o-mini

The categorical measures cannot be reused: entropy and pairwise agreement are defined
over label FREQUENCIES, and a continuous rating has none. The continuous analogues,
over the k conditions that gave a free numeric answer (basic + control x 3 protocols;
`customized` is a lettered choice and is excluded, as in regression_llm.py):

  u_confidence   1 - mean of the model's stated confidence          [unchanged]
  u_spread       standard deviation of the k ratings                [<- entropy]
  u_disagreement mean pairwise |r_a - r_b| over the k ratings        [<- inter-rater]

Spread and disagreement measure the same thing on different scales (for k ratings,
mean pairwise distance is proportional to SD for a normal sample) but they are kept
separate because the ratings are bounded and discrete, so the two rank ties
differently.

llm_rating is the MEAN over the k conditions -- the continuous analogue of the
majority-vote label, and the value the regression track already scores.

Writes results/movie_reviews/regression/model_analysis/<model>/
       uncertainty_per_instance.csv
"""
import collections
import csv
import itertools
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
sys.path.insert(0, str(ROOT / "eval" / "llm"))
import score_llm as S                                              # noqa: E402
from regression_llm import CONTINUOUS, GROUPS, PROTOS, stars       # noqa: E402

DATA = ROOT / "datasets_pass" / "movie_reviews_crowd"
RES = ROOT / "results" / "movie_reviews" / "regression"


def conf01(v):
    if not isinstance(v, (int, float)):
        return None
    v = float(v)
    return min(max(v / 100.0 if v > 1.0 else v, 0.0), 1.0)


def main(model):
    per = collections.defaultdict(list)       # task -> [(rating, confidence)]
    k_total = 0
    for group, short in GROUPS.items():
        if short not in CONTINUOUS:
            continue
        for proto in PROTOS:
            recs = S.read(model, group, "movie_reviews", proto)
            if not recs:
                continue
            k_total += 1
            for r in recs:
                v = stars(r, proto, short)
                if v is None:
                    continue
                per[r["id"]].append((v, conf01(S.confidence(r.get("parsed"), proto))))
    if not per:
        print(f"  no continuous output for {model}")
        return

    gold = {f"mr{i}": g for i, g in
            enumerate(float(x) for x in open(DATA / "ratings_train.txt"))}

    out = RES / "model_analysis" / model
    out.mkdir(parents=True, exist_ok=True)
    cols = ["task", "llm_rating", "gold", "abs_error", "k_conditions",
            "u_confidence", "u_spread", "u_disagreement"]
    n = 0
    with open(out / "uncertainty_per_instance.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for t in sorted(per, key=lambda x: int(x[2:])):
            vals = [v for v, _ in per[t]]
            cs = [c for _, c in per[t] if c is not None]
            k = len(vals)
            rating = sum(vals) / k
            spread = statistics.stdev(vals) if k > 1 else 0.0
            pairs = list(itertools.combinations(vals, 2))
            disag = sum(abs(a - b) for a, b in pairs) / len(pairs) if pairs else 0.0
            g = gold.get(t)
            w.writerow({
                "task": t, "llm_rating": round(rating, 6),
                "gold": "" if g is None else round(g, 6),
                "abs_error": "" if g is None else round(abs(rating - g), 6),
                "k_conditions": k,
                "u_confidence": round(1 - sum(cs) / len(cs), 6) if cs else "",
                "u_spread": round(spread, 6),
                "u_disagreement": round(disag, 6),
            })
            n += 1
    print(f"  movie_reviews/regression  rows={n:,}  k={k_total} continuous conditions"
          f"  -> {(out / 'uncertainty_per_instance.csv').relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

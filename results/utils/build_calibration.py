#!/usr/bin/env python3
"""Calibration: does LLM accuracy fall as its own uncertainty rises?

    python results/utils/build_calibration.py <dataset> [model ...]

Bins instances into 5 uncertainty levels and reports accuracy per bin. A calibrated
annotator is monotone: the most-uncertain bin should be the least accurate. The slope
across bins is what makes routing work -- if accuracy is flat in u, ranking by u cannot
select instances worth sending to humans.

FOUR UNCERTAINTY SOURCES -- what the uncertainty is measured ACROSS. k0 varies
nothing, k1 and k2 hold one axis fixed and vary the other, k3 varies both.

    k0   basic instruction x vanilla                k=1   NO variation: the model's
                                                          own stated confidence on a
                                                          single response
    k1   basic instruction x {vanilla, cot, topk}   k=3   vary REASONING PROTOCOL
    k2   {basic, control, customized} x vanilla     k=3   vary PROMPT WORDING
    k3   3 prompt groups x 3 protocols             k=9   the full grid (the pipeline)

k0 is the cheap baseline every other source must beat: one API call, no ensembling,
uncertainty read straight off the model's self-report. Only `confidence` is defined
there -- entropy and inter_rater need >=2 conditions to have any spread to measure --
so its other two cells come back DEGENERATE by construction. They are still emitted
rather than skipped, because "single-shot cannot support the dispersion measures at
all" is the point of including k0.

k1 vs k2 is the informative contrast, and it is clean because they are EQUAL-k: any
difference between them is about which perturbation the model is more sensitive to,
not about how many conditions were averaged. k1 asks "does the answer move when the
model reasons differently?"; k2 asks "does it move when the same question is worded
differently?".

THREE MEASURES, each per instance over those k conditions
    confidence   1 - mean(stated confidence)          self-report
    entropy      -sum f_l ln f_l over label freqs      how much the answer MOVES
    inter_rater  1 - mean pairwise agreement           same, Gini-Simpson form

DEGENERACY is still checked and reported (status=DEGENERATE), not assumed absent:
at k=1 entropy is identically 0 and inter_rater divides by k(k-1)=0. With every
source now at k>=3 that branch should stay silent; if it fires, conditions are
missing from llm_output rather than the measure being ill-posed.

BINNING. 15 equal-width bins, the number used by Guo et al. for ECE, on u
normalised to [0,1] (entropy by its ceiling
ln(min(k, n_classes)); the other two are already [0,1]). Equal-width, NOT quintiles:
60-80% of instances sit at exactly u=0 on these datasets, so equal-frequency bins
cannot be formed -- they would split a single tied value across bin edges arbitrarily.
Bin populations are written out so that concentration stays visible.

The accuracy in each bin is of the MAJORITY-VOTE label over that source's k conditions
(ties -> alphabetically first, matching build_majority_vote.py), so accuracy and
uncertainty always describe the same aggregate.

Writes results/<dataset>_calibration/calibration_summary.csv (one row per
model x source x measure). The per-model calibration.csv/png this used to emit were
dropped -- the reliability figures from build_reliability.py replaced them.
"""
import collections
import csv
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
sys.path.insert(0, str(ROOT / "eval" / "llm"))
import uncertainty as U                                              # noqa: E402

RES = ROOT / "results"
LONG = ROOT / "eval" / "data"
NBINS = 15

# Which conditions feed each source. Predicates take the PARSED (group, proto) rather
# than matching the raw key: sentiment emits "basic/vanilla[pos]", so a bare
# endswith("/vanilla") would silently drop both of its polarity conditions.
SOURCES = [
    ("k0", "basic instruction x vanilla (single response)",
     lambda g, p: g == "basic" and p == "vanilla"),
    ("k1", "basic instruction x 3 protocols",
     lambda g, p: g == "basic"),
    ("k2", "3 prompt paraphrases x vanilla",
     lambda g, p: p == "vanilla"),
    ("k3", "3 prompt groups x 3 protocols",
     lambda g, p: True),
]
MEASURES = ["confidence", "entropy", "inter_rater"]

# A model only ever ran on ONE arm, except gpt-4o-mini which is multimodal and ran on
# both. Asking for a text model on an image dataset yields no conditions and a spurious
# "skipped" line, so the arm is resolved from the dataset instead.
TEXT_DATASETS = ["sentiment", "movie_reviews", "crowdtruth_cause", "crowdtruth_treat", "crowdtruth_pooled",
                 "conll_ner_5k", "pico_5k", "quiz"]
IMAGE_DATASETS = ["labelme", "imagenet16h"]
DATASETS = TEXT_DATASETS + IMAGE_DATASETS
TEXT_MODELS = ["gpt-4o-mini", "llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0"]
IMAGE_MODELS = ["gpt-4o-mini", "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"]


def models_for(ds):
    return IMAGE_MODELS if ds in IMAGE_DATASETS else TEXT_MODELS


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def outdir(ds):
    """Where the calibration artefacts go:
    results/calibration_analysis/<dataset>_calibration/.

    Deliberately NOT under results/<dataset>/model_analysis/ -- the per-model
    calibration.csv/png that used to live there were removed, and keeping the
    surviving summary beside the reliability figures makes the pair self-contained.
    All nine dataset folders sit under one calibration_analysis/ parent rather than
    loose at the results root, where they would interleave with the per-dataset
    result directories they are named after.
    """
    return RES / "calibration_analysis" / f"{ds}_calibration"


def _f(v):
    return "" if v is None else f"{v:.4f}"


def parse_cond(name):
    """'basic/vanilla' -> ('basic','vanilla');  'basic/vanilla[pos]' -> ('basic','vanilla')."""
    group, _, rest = name.partition("/")
    return group, rest.split("[", 1)[0]


def merge_variants(conds):
    """Collapse bracketed variants of one condition into a single condition.

    Sentiment's True/False manipulation asks each sentence TWICE, counterbalanced over
    the asserted polarity, so `customized/vanilla` arrives as `[positive]` and
    `[negative]`. Left uncollapsed it inflates k to 4 and 12 where every other dataset
    has 3 and 9, which destroys the equal-k property that makes the k1 vs k2 contrast
    interpretable.

    The pair is merged probabilistically rather than by picking a winner. Each response
    contributes its stated confidence to its own label and spreads the remainder over
    the others; the two distributions are averaged and the argmax is taken, with the
    merged confidence being that posterior. The two queries contradict each other on
    5-18% of instances depending on model and protocol, and this rule turns such a
    contradiction into low confidence, which is what it means, instead of an arbitrary
    choice between the two answers.
    """
    groups = collections.defaultdict(list)
    for name, d in conds.items():
        groups[parse_cond(name)].append(d)
    out = {}
    for (g, proto), dicts in groups.items():
        name = f"{g}/{proto}"
        if len(dicts) == 1:
            out[name] = dicts[0]
            continue
        merged = {}
        for t in set().union(*(set(d) for d in dicts)):
            resp = [d[t] for d in dicts if t in d]
            if not resp:
                continue
            labels = sorted({l for l, _ in resp})
            P = collections.defaultdict(float)
            for l, c in resp:
                c = 0.5 if c is None else c
                others = [x for x in labels if x != l]
                P[l] += c
                for o in others:
                    P[o] += (1.0 - c) / len(others)
            for l in P:
                P[l] /= len(resp)
            best = max(sorted(P), key=lambda l: P[l])
            merged[t] = (best, P[best])
        out[name] = merged
    return out


def per_instance(conds, gold):
    """-> {task: (label, correct, {measure: u_raw})} over exactly these conditions."""
    tasks = collections.defaultdict(dict)
    for name, d in conds.items():
        for t, (lab, c) in d.items():
            tasks[t][name] = (lab, c)

    out = {}
    for t, per in tasks.items():
        if t not in gold:
            continue
        labs = [l for l, _ in per.values()]
        k = len(labs)
        cnt = collections.Counter(labs)
        top = max(cnt.values())
        label = sorted(l for l, v in cnt.items() if v == top)[0]

        cs = [c for _, c in per.values() if c is not None]
        u_c = 1.0 - sum(cs) / len(cs) if cs else None
        u_e = -sum((v / k) * math.log(v / k) for v in cnt.values())
        u_a = (1.0 - sum(v * (v - 1) for v in cnt.values()) / (k * (k - 1))
               if k >= 2 else None)
        out[t] = (label, int(label == gold[t]),
                  {"confidence": u_c, "entropy": u_e, "inter_rater": u_a}, k)
    return out


def ceiling(measure, k, n_classes):
    """Theoretical max of the raw measure, for normalising to [0,1]."""
    if measure == "entropy":
        m = min(k, n_classes)
        return math.log(m) if m > 1 else 0.0
    return 1.0            # confidence and inter_rater are already [0,1]


def ece(pairs, ceil, nbins=NBINS):
    """Expected Calibration Error over `nbins` equal-width bins of confidence=1-u_norm.

        ECE = sum_b (n_b/N) * |acc_b - mean_conf_b|

    For `confidence` this is textbook ECE: the model's own stated probability against
    how often it is right. For entropy/inter_rater the "confidence" is 1 - normalised
    dispersion, which is NOT a probability the model asserted -- it is a consistency
    score being read as one. Comparable across measures, but only the confidence row
    is ECE in the usual sense.
    """
    if not pairs:
        return None
    N = len(pairs)
    tot = 0.0
    for b in range(nbins):
        lo, hi = b / nbins, (b + 1) / nbins
        sel = [(1.0 - (u / ceil if ceil else 0.0), c) for u, c in pairs
               if (lo <= (u / ceil if ceil else 0.0) < hi)
               or (b == nbins - 1 and (u / ceil if ceil else 0.0) >= hi)]
        if not sel:
            continue
        acc = sum(c for _, c in sel) / len(sel)
        conf = sum(f for f, _ in sel) / len(sel)
        tot += len(sel) / N * abs(acc - conf)
    return round(tot, 4)


def auroc(pairs):
    """AUROC for using LOW uncertainty to predict CORRECT, tie-aware.

    Score = -u, so a well-behaved measure gives correct answers lower u. Computed by
    the rank form of Mann-Whitney U with MIDRANKS, which credits ties 0.5 -- essential
    here, since 60-80% of instances share u=0 and a naive pairwise count would silently
    score those as wins. 0.5 = no discrimination, 1.0 = perfect separation.
    """
    pos = [-u for u, c in pairs if c == 1]
    neg = [-u for u, c in pairs if c == 0]
    if not pos or not neg:
        return None
    allv = sorted(pos + neg)
    rank = {}
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1] == allv[i]:
            j += 1
        rank[allv[i]] = (i + j) / 2.0 + 1          # midrank for the tied block
        i = j + 1
    s = sum(rank[v] for v in pos)
    return round((s - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)), 4)


def bins_for(rows, measure, k, n_classes):
    """-> (status, [bin dicts]). Bin 1 = LOWEST uncertainty."""
    ceil = ceiling(measure, k, n_classes)
    vals = [(u[measure], corr) for _, corr, u, _ in rows if u[measure] is not None]
    if not vals:
        return "DEGENERATE (undefined at k=1: divides by k(k-1)=0)", []
    if ceil == 0:
        return "DEGENERATE (identically 0 at k=1: a single vote has no spread)", []
    if len({v for v, _ in vals}) == 1:
        return f"DEGENERATE (all {len(vals)} instances share u={vals[0][0]:.4f})", []

    out = []
    for b in range(NBINS):
        lo, hi = b / NBINS, (b + 1) / NBINS
        sel = [c for v, c in vals
               if (lo <= v / ceil < hi) or (b == NBINS - 1 and v / ceil >= hi)]
        out.append({"bin": b + 1, "u_lo": round(lo, 2), "u_hi": round(hi, 2),
                    "n": len(sel),
                    "accuracy": round(sum(sel) / len(sel), 4) if sel else ""})
    return "ok", out


def main(ds, models):
    gold = {r["task"]: r["true_label"]
            for r in csv.DictReader(open(LONG / f"{ds}_gold.csv"))}
    summary = []

    for model in models:
        conds_all = merge_variants(U.conditions(model, ds))
        if not conds_all:
            print(f"  {model}: no conditions found, skipped")
            continue
        print(f"\n=== {ds} / {model} ===")
        print(f"  conditions available: {len(conds_all)}  {sorted(conds_all)}")

        for skey, slabel, pred in SOURCES:
            conds = {c: v for c, v in conds_all.items() if pred(*parse_cond(c))}
            if not conds:
                print(f"  {skey}: no matching conditions, skipped")
                continue
            pi = per_instance(conds, gold)
            k = len(conds)
            n_classes = len({lab for lab, _, _, _ in pi.values()})
            overall = sum(c for _, c, _, _ in pi.values()) / len(pi)
            print(f"\n  [{skey}] {slabel}   k={k}  n={len(pi)}  overall acc={overall:.4f}")

            for meas in MEASURES:
                status, bs = bins_for(list(pi.values()), meas, k, n_classes)
                pairs = [(u[meas], corr) for _, corr, u, _ in pi.values()
                         if u[meas] is not None]
                ceil = ceiling(meas, k, n_classes)
                e = ece(pairs, ceil)
                a = auroc(pairs)
                if status != "ok":
                    print(f"     {meas:12s} ECE={_f(e)}  AUROC={_f(a)}   {status}")
                    summary.append({"dataset": ds, "model": model, "source": skey,
                                    "source_detail": slabel, "k": k,
                                    "measure": meas, "status": status,
                                    "overall_acc": round(overall, 4),
                                    "ECE": _f(e), "AUROC": _f(a), "slope": "",
                                    "acc_lowest_u": "", "acc_highest_u": ""})
                    continue
                pop = [b["n"] for b in bs]
                accs = [b["accuracy"] for b in bs]
                lo_a = next((a for a in accs if a != ""), "")
                hi_a = next((a for a in reversed(accs) if a != ""), "")
                slope = round(lo_a - hi_a, 4) if lo_a != "" and hi_a != "" else ""
                print(f"     {meas:12s} ECE={_f(e)}  AUROC={_f(a)}   "
                      f"n/bin={pop}  acc={accs}  drop={slope}")
                summary.append({"dataset": ds, "model": model, "source": skey,
                                "source_detail": slabel, "k": k,
                                "measure": meas, "status": "ok",
                                "overall_acc": round(overall, 4),
                                "ECE": _f(e), "AUROC": _f(a), "slope": slope,
                                "acc_lowest_u": lo_a, "acc_highest_u": hi_a})

    if summary:
        d = outdir(ds)
        d.mkdir(parents=True, exist_ok=True)
        f = d / "calibration_summary.csv"
        with open(f, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(summary[0]))
            w.writeheader()
            w.writerows(summary)
        print(f"\n  -> {f.relative_to(ROOT)}  ({len(summary)} rows)")
    return summary


if __name__ == "__main__":
    a = sys.argv[1:]
    todo = [a[0]] if a else DATASETS
    for _ds in todo:
        main(_ds, a[1:] or models_for(_ds))

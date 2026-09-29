#!/usr/bin/env python3
"""Per-dataset uncertainty for one model, over its (protocol x prompt-strategy) conditions.

    python eval/llm/uncertainty.py gpt-4o-mini

Three measures, each computed per instance i over the k conditions, then averaged:

  1. CONFIDENCE (self-evaluation)     u_i = 1 - (1/k) * sum_j P(a_ij | p_ij)
     P is the confidence the model reported, rescaled to [0,1].

  2. ENTROPY                          u_i = - sum_l f_l * ln f_l
     f_l is the FREQUENCY of label l among the k predictions for instance i
     (not the model's stated confidence). Max = ln(min(k, n_labels)).

  3. INTER-RATER AGREEMENT            each condition is a rater.
     Reported as mean pairwise percent agreement and Fleiss' kappa. Lower
     agreement = higher uncertainty, so 1 - agreement is the uncertainty analogue.

Measures 1 and 2 are complementary: 1 asks the model how sure it is, 2 measures how
much its answer actually moves when the prompt changes. They can disagree sharply --
a model can be confidently inconsistent.

Writes results/<dataset>/<model>_uncertainty_per_instance.csv
"""
import collections
import csv
import functools
import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
sys.path.insert(0, str(ROOT / "eval" / "llm"))
from common.paths import bin_rating                                  # noqa: E402
import score_llm as S                                                # noqa: E402

LONG = ROOT / "eval" / "data"
DATA = ROOT / "datasets_pass"
RES = ROOT / "results"
PROTOS = ["vanilla", "cot", "topk"]
GROUPS = {"basic_instruction": "basic", "control": "control", "customized": "customized"}
SOURCE = {"sentiment": "sentiment", "movie_reviews": "movie_reviews",
          "crowdtruth_cause": "crowdtruth", "crowdtruth_treat": "crowdtruth",
          "crowdtruth_pooled": "crowdtruth",
          "conll_ner_5k": "conll_ner", "pico_5k": "pico", "quiz": "quiz",
          "labelme": "labelme", "imagenet16h": "imagenet16h"}
NER_TAGS = ["O", "B-PER", "I-PER", "B-LOC", "I-LOC", "B-ORG", "I-ORG", "B-MISC", "I-MISC"]

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




def conf01(v):
    """Confidence -> [0,1]. Outputs are 0-100; tolerate a model that answers 0-1."""
    if not isinstance(v, (int, float)):
        return None
    v = float(v)
    if v > 1.0:
        v /= 100.0
    return min(max(v, 0.0), 1.0)


def _top(parsed, proto):
    return S.top_answer(parsed, proto)


def _conf_scalar(parsed, proto):
    if parsed is None:
        return None
    if proto == "topk":
        g = parsed.get("guesses") or []
        best = max((x for x in g if isinstance(x, dict)),
                   key=lambda x: x.get("probability", 0), default=None)
        return conf01(best.get("probability")) if best else None
    return conf01(parsed.get("confidence"))


# ------------------------------------------------------- per-dataset extraction
def ex_sentiment(recs, proto, group):
    out = {}
    for r in recs:
        p = r.get("parsed")
        a = _top(p, proto)
        c = _conf_scalar(p, proto)
        if group == "customized":
            tid = r["id"]
            if "#" not in tid or not isinstance(a, str):
                continue
            task, pol = tid.rsplit("#", 1)
            a = a.strip().lower()
            if a not in ("true", "false"):
                continue
            asserted = "pos" if pol == "positive" else "neg"
            lab = asserted if a == "true" else ("neg" if asserted == "pos" else "pos")
            out.setdefault(pol, {})[task] = (lab, c)
        else:
            if isinstance(a, str) and a.strip().lower() in ("pos", "neg"):
                out[r["id"]] = (a.strip().lower(), c)
    return out


def ex_movie_reviews(recs, proto, group):
    out = {}
    for r in recs:
        p = r.get("parsed")
        a = _top(p, proto)
        c = _conf_scalar(p, proto)
        if group == "customized":                      # reversed letters, A = 10 stars
            if not isinstance(a, str) or not a.strip():
                continue
            L = a.strip().upper()[0]
            if not ("A" <= L <= "K"):
                continue
            stars = 10 - (ord(L) - 65)
        else:
            try:
                stars = float(a)
            except (TypeError, ValueError):
                continue
            if not 0 <= stars <= 10:
                continue
        out[r["id"]] = (str(bin_rating([stars / 10.0])[0]), c)
    return out


def ex_crowdtruth(recs, proto, group, rel):
    """rel is "cause", "treat", or "pooled".

    "pooled" emits BOTH relations as separate `c`/`t`-namespaced instances, matching
    eval/data/crowdtruth_pooled_gold.csv. The confidence is the same scalar for both
    halves -- one multi-select response carries a single confidence, so a sentence's
    cause and treat instances necessarily share it. That is a real property of the
    pooled table, not an artefact here: it means u_confidence cannot distinguish the
    two subtasks, only the vote-based measures can.
    """
    if rel == "pooled":
        c_ = ex_crowdtruth(recs, proto, group, "cause")
        t_ = ex_crowdtruth(recs, proto, group, "treat")
        keep = _pooled_ids()
        out = {f"c{i}": v for i, v in c_.items() if f"c{i}" in keep}
        out.update({f"t{i}": v for i, v in t_.items() if f"t{i}" in keep})
        return out
    tag = "[CAUSES]" if rel == "cause" else "[TREATS]"
    out = {}
    for r in recs:
        p = r.get("parsed")
        a = _top(p, proto)
        c = _conf_scalar(p, proto)
        if isinstance(a, str):
            a = [a]
        if not isinstance(a, list):
            continue
        up = {str(x).strip().upper() for x in a}
        out[r["id"]] = ("yes" if tag in up else "no", c)
    return out


@functools.lru_cache(maxsize=1)
def _pooled_ids():
    f = LONG / "crowdtruth_pooled_gold.csv"
    return (frozenset(r["task"] for r in csv.DictReader(open(f)))
            if f.exists() else frozenset())


def ex_conll(recs, proto, group):
    out = {}
    if group == "customized":                          # per-token MCQ, one letter
        for r in recs:
            p = r.get("parsed")
            a = _top(p, proto)
            if not isinstance(a, str) or not a.strip():
                continue
            i = ord(a.strip().upper()[0]) - 65
            if 0 <= i < len(NER_TAGS):
                out[r["id"]] = (NER_TAGS[i], _conf_scalar(p, proto))
        return out
    want = collections.Counter()
    for t in (x["task"] for x in csv.DictReader(open(LONG / "conll_ner_5k_gold.csv"))):
        want[t.split("_")[0]] += 1
    for r in recs:
        p = r.get("parsed")
        if not isinstance(p, dict):
            continue
        if proto == "topk":
            g = p.get("guesses")
            if not isinstance(g, list):
                continue
            tags, confs = [], []
            for per in g:
                items = per if isinstance(per, list) else [per]
                best = max((x for x in items if isinstance(x, dict)),
                           key=lambda x: x.get("probability", 0), default=None)
                tags.append(best.get("answer") if best else None)
                confs.append(conf01(best.get("probability")) if best else None)
        else:
            tags = p.get("answer")
            confs = p.get("confidence")
            if not isinstance(confs, list):
                confs = [conf01(confs)] * (len(tags) if isinstance(tags, list) else 0)
            else:
                confs = [conf01(c) for c in confs]
        if not isinstance(tags, list) or len(tags) != want.get(r["id"], -1):
            continue
        for i, t in enumerate(tags):
            if isinstance(t, str):
                out[f"{r['id']}_t{i}"] = (t.strip(),
                                          confs[i] if i < len(confs) else None)
    return out


def ex_quiz(recs, proto, group):
    """Letter answer -> (label, confidence). Gold is a letter too, so no recast applies.

    Mirrors score_llm.map_quiz: an answer outside THAT item's option set is dropped, not
    kept. The subsets carry 4, 5, or 6 options, so "F" on a four-option question is a
    prompt-following failure and must not enter the label distribution -- it would inflate
    entropy with a choice the item never offered.

    The same extractor serves all three groups: the confirmation-bias prompt changes the
    framing, not the answer space.
    """
    import score_llm as _S
    opts = _S.quiz_options()
    out = {}
    for r in recs:
        p = r.get("parsed")
        a = _S._letter(_top(p, proto))
        if a is None or a not in opts.get(r["id"], ()):
            continue
        out[r["id"]] = (a, _conf_scalar(p, proto))
    return out


def ex_image(recs, proto, group, table):
    """Image datasets -> (category, confidence). NEVER DROPS AN INSTANCE.

    Delegates to score_llm's mappers so the uncertainty view and the accuracy view can
    never disagree about what a record answered. That matters here because the answer
    space CHANGES by group: basic/control return a category NAME, customized returns a
    LETTER. It also inherits both guards -- the alphanumeric fold that accepts
    "open country" for `opencountry`, and the rejection of out-of-range letters.

    A refusal ("none of the above") or any other invalid answer is mapped to
    score_llm.IMG_INVALID_LABEL by the mapper, NOT dropped -- it is a real vote (always
    wrong against gold) that participates in the label distribution like any other answer,
    the same policy as the accuracy scoring. Note gpt-4o-mini refuses at very different
    rates by group (2.3% basic vs 15.1% control) -- REFUSAL RATE ITSELF differs by
    condition even though every condition now has full n_scored=n_total coverage.

    CONFIDENCE: if the record reports one (even alongside an invalid answer -- a model can
    be confidently wrong), keep it. If the record reports none (parse failure, missing
    field), assign the LOWEST confidence observed anywhere in this same file -- i.e. this
    (model, group, protocol, dataset) run -- as a worst-case stand-in, so no instance is
    dropped for lack of a confidence value either. If NO record in the file reports any
    confidence, fall back to 0.0.
    """
    import score_llm as _S
    fn = _S.MAPPERS_BY_GROUP.get(group, {}).get(table, _S.MAPPERS[table])
    out_t = fn(recs, proto)
    pred = (out_t[0] if isinstance(out_t, tuple) else out_t)[table]
    conf = {r["id"]: _conf_scalar(r.get("parsed"), proto) for r in recs}
    observed = [c for c in conf.values() if c is not None]
    floor = min(observed) if observed else 0.0
    return {r["id"]: (pred[r["id"]], conf[r["id"]] if conf[r["id"]] is not None else floor)
            for r in recs if r["id"] in pred}


def ex_pico(recs, proto, group):
    keep = {t.rsplit("_", 1)[0]
            for t in (x["task"] for x in csv.DictReader(open(LONG / "pico_5k_gold.csv")))}
    out = {}
    for r in recs:
        if r["id"] not in keep:
            continue
        p = r.get("parsed")
        spans = _top(p, proto)
        c = _conf_scalar(p, proto)
        if isinstance(spans, str):
            spans = [spans]
        if not isinstance(spans, list):
            continue
        f = DATA / "pico_data" / "docs" / f"{r['id']}.txt"
        if not f.exists():
            continue
        text = f.read_text()
        mask = bytearray(len(text))
        for s in spans:
            if not isinstance(s, str):
                continue
            s = s.strip().strip("<>").strip()
            if not s:
                continue
            i = text.find(s)
            if i < 0:
                continue
            for j in range(i, min(i + len(s), len(text))):
                mask[j] = 1
        for i, mt in enumerate(re.finditer(r"\S+", text)):
            out[f"{r['id']}_{i}"] = ("in" if any(mask[mt.start():mt.end()]) else "out", c)
    return out


def conditions(model, table):
    """-> {condition: {task: (label, confidence)}}"""
    ds = SOURCE[table]
    out = {}
    for group, short in GROUPS.items():
        for proto in PROTOS:
            recs = S.read(model, group, ds, proto)
            if not recs:
                continue
            if ds == "sentiment":
                res = ex_sentiment(recs, proto, group)
                if res and isinstance(next(iter(res.values())), dict):
                    for pol, d in res.items():
                        out[f"{short}/{proto}[{pol}]"] = d
                    continue
                out[f"{short}/{proto}"] = res
            elif ds == "movie_reviews":
                out[f"{short}/{proto}"] = ex_movie_reviews(recs, proto, group)
            elif ds == "crowdtruth":
                rel = ("pooled" if table.endswith("pooled")
                       else "cause" if table.endswith("cause") else "treat")
                out[f"{short}/{proto}"] = ex_crowdtruth(recs, proto, group, rel)
            elif ds == "conll_ner":
                out[f"{short}/{proto}"] = ex_conll(recs, proto, group)
            elif ds == "quiz":
                out[f"{short}/{proto}"] = ex_quiz(recs, proto, group)
            elif ds in ("labelme", "imagenet16h"):
                out[f"{short}/{proto}"] = ex_image(recs, proto, group, ds)
            else:
                out[f"{short}/{proto}"] = ex_pico(recs, proto, group)
    return {k: v for k, v in out.items() if v}


# ------------------------------------------------------------------- measures
def fleiss_kappa(rows):
    """rows: list of Counter(label -> n_raters), items with the SAME rater count."""
    if not rows:
        return float("nan"), 0
    n = sum(rows[0].values())
    rows = [r for r in rows if sum(r.values()) == n]
    if not rows or n < 2:
        return float("nan"), 0
    N = len(rows)
    labels = sorted({l for r in rows for l in r})
    p_j = {l: sum(r.get(l, 0) for r in rows) / (N * n) for l in labels}
    P_i = [(sum(v * v for v in r.values()) - n) / (n * (n - 1)) for r in rows]
    P_bar = sum(P_i) / N
    P_e = sum(v * v for v in p_j.values())
    if abs(1 - P_e) < 1e-12:
        return float("nan"), N
    return (P_bar - P_e) / (1 - P_e), N


def per_instance(conds, gold):
    """One row per instance: the LLM-only label plus all three uncertainties.

    llm_label is the MAJORITY VOTE over the k conditions (ties -> alphabetically
    first, matching build_majority_vote.py), i.e. the aggregated LLM annotation.
    Measure 3 is per-instance pairwise agreement; Fleiss' kappa has no per-instance
    analogue and stays a dataset-level statistic.
    """
    tasks = collections.defaultdict(dict)
    for name, d in conds.items():
        for t, (lab, c) in d.items():
            tasks[t][name] = (lab, c)

    rows = []
    for t in sorted(tasks):
        # only score instances that HAVE a gold label: crowdtruth_treat covers 621 of
        # the 975 sentences, and keeping the rest would put the wrong denominator
        # under every downstream percentage.
        if t not in gold:
            continue
        per = tasks[t]
        labs = [l for l, _ in per.values()]
        k = len(labs)
        cnt = collections.Counter(labs)
        top = max(cnt.values())
        label = sorted(l for l, v in cnt.items() if v == top)[0]
        cs = [c for _, c in per.values() if c is not None]
        u_c = 1.0 - sum(cs) / len(cs) if cs else ""
        u_e = -sum((v / k) * math.log(v / k) for v in cnt.values())
        u_a = 1.0 - sum(v * (v - 1) for v in cnt.values()) / (k * (k - 1)) if k >= 2 else ""
        g = gold.get(t, "")
        rows.append({
            "task": t, "llm_label": label, "gold": g,
            "correct": "" if not g else int(label == g),
            "k_conditions": k, "n_distinct_labels": len(cnt),
            "u_confidence": "" if u_c == "" else round(u_c, 4),
            "u_entropy": round(u_e, 4),
            "u_agreement": "" if u_a == "" else round(u_a, 4),
            "unanimous": int(len(cnt) == 1),
        })
    return rows


def measure(conds):
    tasks = collections.defaultdict(dict)
    for name, d in conds.items():
        for t, (lab, c) in d.items():
            tasks[t][name] = (lab, c)

    u_conf, u_ent, pair_agree, counters = [], [], [], []
    for t, per in tasks.items():
        cs = [c for _, c in per.values() if c is not None]
        if cs:
            u_conf.append(1.0 - sum(cs) / len(cs))
        labs = [l for l, _ in per.values()]
        k = len(labs)
        cnt = collections.Counter(labs)
        counters.append(cnt)
        if k >= 1:
            u_ent.append(-sum((v / k) * math.log(v / k) for v in cnt.values()))
        if k >= 2:
            same = sum(v * (v - 1) for v in cnt.values())
            pair_agree.append(same / (k * (k - 1)))

    kappa, n_kappa = fleiss_kappa(counters)
    mean = lambda x: sum(x) / len(x) if x else float("nan")          # noqa: E731
    return {
        "n_instances": len(tasks),
        "k_conditions": len(conds),
        "u_confidence": mean(u_conf),
        "mean_confidence": 1 - mean(u_conf) if u_conf else float("nan"),
        "u_entropy": mean(u_ent),
        "u_entropy_norm": mean(u_ent) / math.log(len(conds)) if len(conds) > 1 else float("nan"),
        "pct_agreement": mean(pair_agree),
        "u_agreement": 1 - mean(pair_agree) if pair_agree else float("nan"),
        "fleiss_kappa": kappa,
        "n_kappa": n_kappa,
        "unanimous": mean([1.0 if len(c) == 1 else 0.0 for c in counters]),
    }


def main(model):
    for table in SOURCE:
        conds = conditions(model, table)
        if not conds:
            continue
        m = measure(conds)
        d = ddir(table)
        gold = {r["task"]: r["true_label"]
                for r in csv.DictReader(open(LONG / f"{table}_gold.csv"))}
        rows = per_instance(conds, gold)
        cols = ["task", "llm_label", "gold", "correct", "k_conditions",
                "n_distinct_labels", "u_confidence", "u_entropy", "u_agreement",
                "unanimous"]
        with open(mdir(table, model, d) / "uncertainty_per_instance.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        # NOTE: the dataset-level rollup was dropped on request -- only the
        # per-instance table is kept. Aggregate as needed from that CSV.
        print(f"  {table:18s} rows={len(rows):5,d}  k={m['k_conditions']:2d}  "
              f"u_conf={m['u_confidence']:.4f}  u_ent={m['u_entropy']:.4f}  "
              f"1-agree={m['u_agreement']:.4f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

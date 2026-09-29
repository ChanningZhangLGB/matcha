#!/usr/bin/env python3
"""Score an LLM as a SINGLE ANNOTATOR directly against ground truth.

    python eval/llm/score_llm.py <model_dir> [--group basic_instruction]

The model's raw output is put through the SAME recast that was applied to the human
labels, so the numbers sit on the same scale as results/<ds>/crowd_aggregation.md:

  sentiment      answer "pos"/"neg"                      -> as-is
  movie_reviews  answer 0-10 stars -> /10 -> bin_rating  -> poor/medium/good
  crowdtruth     answer [RELATION,...] multi-select      -> binary per relation
  conll_ner      answer [tag]*n_tokens                   -> one row per token
  pico           answer [verbatim span,...]              -> in/out per token

Top-K collapses to its highest-probability guess. That makes topk approach vanilla by
construction; the distribution it carries is discarded here and is only meaningful if
consumed as a distribution.

Writes results/<table>/llm/<group>/<model>.{md,csv}
"""
import argparse
import collections
import csv
import functools
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval"))
from common.metrics import categorical_metrics            # noqa: E402
from common.paths import bin_rating                       # noqa: E402

LONG = ROOT / "eval" / "data"
DATA = ROOT / "datasets_pass"
OUTPUT = ROOT / "llm_output"
RES = ROOT / "results"
PROTOCOLS = ["vanilla", "cot", "topk"]
GROUP_DIR = {"basic_instruction": "basic", "control": "control",
             "customized": "customized"}
POSITIVE = {"sentiment": "pos", "crowdtruth_cause": "yes",
            "crowdtruth_treat": "yes", "crowdtruth_pooled": "yes",
            "pico_5k": "in"}

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




def top_answer(parsed, protocol):
    """The hard label. For topk, the highest-probability guess."""
    if parsed is None:
        return None
    if protocol == "topk":
        g = parsed.get("guesses")
        if not isinstance(g, list) or not g:
            return None
        best = max((x for x in g if isinstance(x, dict)),
                   key=lambda x: x.get("probability", 0), default=None)
        return None if best is None else best.get("answer")
    return parsed.get("answer")


def confidence(parsed, protocol):
    if parsed is None:
        return None
    if protocol == "topk":
        g = parsed.get("guesses") or []
        # flat: [{answer,probability}, ...]   nested (conll): [[{...}, ...], ...]
        per_unit = []
        for x in g:
            items = x if isinstance(x, list) else [x]
            vals = [i.get("probability") for i in items if isinstance(i, dict)]
            vals = [v for v in vals if isinstance(v, (int, float))]
            if vals:
                per_unit.append(max(vals))
        if not per_unit:
            return None
        # flat -> the single top probability; nested -> mean of each token's top
        return per_unit[0] if not any(isinstance(x, list) for x in g) \
            else sum(per_unit) / len(per_unit)
    c = parsed.get("confidence")
    if isinstance(c, list):
        c = [v for v in c if isinstance(v, (int, float))]
        return sum(c) / len(c) if c else None
    return c if isinstance(c, (int, float)) else None


def read(model, group, dataset, protocol):
    p = OUTPUT / model / group / f"{dataset}_{protocol}.jsonl"
    if not p.exists():
        return None
    out = []
    for line in open(p):
        try:
            out.append(json.loads(line))
        except Exception:                                        # noqa: BLE001
            pass
    return out


# ------------------------------------------------------- per-dataset mapping
def map_sentiment(recs, proto):
    pred = {}
    for r in recs:
        a = top_answer(r.get("parsed"), proto)
        if isinstance(a, str) and a.strip().lower() in ("pos", "neg"):
            pred[r["id"]] = a.strip().lower()
    return {"sentiment": pred}


def map_movie_reviews(recs, proto):
    pred = {}
    for r in recs:
        a = top_answer(r.get("parsed"), proto)
        try:
            stars = float(a)
        except (TypeError, ValueError):
            continue
        if 0 <= stars <= 10:
            pred[r["id"]] = str(bin_rating([stars / 10.0])[0])
    return {"movie_reviews": pred}


def map_crowdtruth(recs, proto):
    """One multi-select response -> a binary label per relation.

    Also emits `crowdtruth_pooled`, the two relations concatenated as separate
    instances with `c`/`t`-namespaced ids (see eval/convert/build_crowdtruth_pooled.py).
    No extra generation is involved: the pooled prediction for `c<id>` IS the cause
    prediction for `<id>`, so the pooled table is a re-indexing of what is already
    scored, not a new inference.

    The pooled half is filtered to ids present in the pooled gold, because treat covers
    only 621 of the 975 sentences -- emitting `t<id>` for all 975 would invent 354
    instances the corpus never labelled.
    """
    cause, treat = {}, {}
    for r in recs:
        a = top_answer(r.get("parsed"), proto)
        if isinstance(a, str):
            a = [a]
        if not isinstance(a, list):
            continue
        up = {str(x).strip().upper() for x in a}
        cause[r["id"]] = "yes" if "[CAUSES]" in up else "no"
        treat[r["id"]] = "yes" if "[TREATS]" in up else "no"
    keep = _pooled_ids()
    pooled = {f"c{i}": v for i, v in cause.items() if f"c{i}" in keep}
    pooled.update({f"t{i}": v for i, v in treat.items() if f"t{i}" in keep})
    return {"crowdtruth_cause": cause, "crowdtruth_treat": treat,
            "crowdtruth_pooled": pooled}


@functools.lru_cache(maxsize=1)
def _pooled_ids():
    f = LONG / "crowdtruth_pooled_gold.csv"
    if not f.exists():
        return frozenset()
    return frozenset(r["task"] for r in csv.DictReader(open(f)))


def map_conll_ner(recs, proto):
    """Per-token. A length mismatch is REJECTED, never padded."""
    want = collections.Counter()
    for t in (r["task"] for r in csv.DictReader(open(LONG / "conll_ner_5k_gold.csv"))):
        want[t.split("_")[0]] += 1
    pred, dropped = {}, 0
    for r in recs:
        parsed = r.get("parsed")
        if not isinstance(parsed, dict):
            dropped += 1
            continue
        if proto == "topk":
            # CoNLL's top-k is NESTED: one ranked guess-list per token, unlike the
            # flat {"guesses":[{answer,probability}]} every other dataset returns.
            # Reduce each token's list to its highest-probability answer.
            g = parsed.get("guesses")
            if not isinstance(g, list):
                dropped += 1
                continue
            tags = []
            for per in g:
                if isinstance(per, list):
                    best = max((x for x in per if isinstance(x, dict)),
                               key=lambda x: x.get("probability", 0), default=None)
                    tags.append(best.get("answer") if best else None)
                elif isinstance(per, dict):          # already reduced by the model
                    tags.append(per.get("answer"))
                else:
                    tags.append(None)
        else:
            tags = parsed.get("answer")
        if not isinstance(tags, list):
            dropped += 1
            continue
        n = want.get(r["id"])
        if n is None or len(tags) != n:
            dropped += 1
            continue
        for i, t in enumerate(tags):
            if isinstance(t, str):
                pred[f"{r['id']}_t{i}"] = t.strip()   # gold ids are s<sent>_t<tok>
    return {"conll_ner_5k": pred}, dropped


def map_pico(recs, proto):
    """Spans -> per-token in/out by exact string search.

    Scored against pico_5k (22 documents). The generation runs covered all 191
    abstracts, and pico_5k is a strict subset, so records outside it are simply
    ignored -- no regeneration is needed.
    """
    keep = {t.rsplit("_", 1)[0]
            for t in (r["task"] for r in csv.DictReader(open(LONG / "pico_5k_gold.csv")))}
    pred, unmatched, total = {}, 0, 0
    for r in recs:
        if r["id"] not in keep:
            continue
        spans = top_answer(r.get("parsed"), proto)
        if isinstance(spans, str):
            spans = [spans]
        if not isinstance(spans, list):
            continue
        did = r["id"]
        f = DATA / "pico_data" / "docs" / f"{did}.txt"
        if not f.exists():
            continue
        text = f.read_text()
        mask = bytearray(len(text))
        for s in spans:
            if not isinstance(s, str):
                continue
            s = s.strip().strip("<>").strip()
            total += 1
            if not s:
                continue
            i = text.find(s)
            if i < 0:
                unmatched += 1
                continue
            for j in range(i, min(i + len(s), len(text))):
                mask[j] = 1
        for i, m in enumerate(re.finditer(r"\S+", text)):
            pred[f"{did}_{i}"] = "in" if any(mask[m.start():m.end()]) else "out"
    return {"pico_5k": pred}, unmatched, total


# ---------------------------------------------- customized-group decoders
NER_TAGS = ["O", "B-PER", "I-PER", "B-LOC", "I-LOC", "B-ORG", "I-ORG",
            "B-MISC", "I-MISC"]                      # option letters A..I


def _letter(a):
    a = str(a).strip().upper()
    return a[0] if a and a[0].isalpha() else None


def map_sentiment_true_false(recs, proto):
    """True/False variant. Ids carry the asserted polarity: <task>#positive.

    Each sentence was asked twice, so the two framings are scored as SEPARATE
    conditions -- collapsing them would hide exactly the acquiescence effect the
    counterbalancing exists to measure.
    """
    out = {}
    for r in recs:
        tid = r["id"]
        if "#" not in tid:
            continue
        task, polarity = tid.rsplit("#", 1)
        a = top_answer(r.get("parsed"), proto)
        if not isinstance(a, str):
            continue
        a = a.strip().lower()
        if a not in ("true", "false"):
            continue
        asserted = "pos" if polarity == "positive" else "neg"
        other = "neg" if asserted == "pos" else "pos"
        out.setdefault(polarity, {})[task] = asserted if a == "true" else other
    return {"sentiment": out}          # dict of condition -> {task: label}


def map_movie_reviews_mcq(recs, proto, reverse=True):
    """Sequence-swapping variant: the 11 options are listed 10 -> 0, so A = 10 stars.
    Pass reverse=False to decode the forward-ordered multiple-choice run."""
    pred = {}
    for r in recs:
        L = _letter(top_answer(r.get("parsed"), proto))
        if L is None:
            continue
        stars = (10 - (ord(L) - 65)) if reverse else (ord(L) - 65)
        if 0 <= stars <= 10:
            pred[r["id"]] = str(bin_rating([stars / 10.0])[0])
    return {"movie_reviews": pred}


def map_conll_ner_mcq(recs, proto):
    """Per-token MCQ: ids are already s<sent>_t<tok>, so no length alignment is
    needed -- this variant is immune to the tag/token mismatch that limits the
    sentence-level prompts."""
    pred, dropped = {}, 0
    for r in recs:
        L = _letter(top_answer(r.get("parsed"), proto))
        if L is None or not (0 <= ord(L) - 65 < len(NER_TAGS)):
            dropped += 1
            continue
        pred[r["id"]] = NER_TAGS[ord(L) - 65]
    return {"conll_ner_5k": pred}, dropped


QUIZ_SUBSETS = {"CHINESE": "chi", "ENGLISH": "eng", "ITMANAGE": "itm",
                "MEDICINE": "med", "POKEMON": "pok", "SCIENCE": "sci"}
_QUIZ_OPTS = None


def quiz_options():
    """{task: {valid letters}}, read positionally to match the gold ids.

    Cached: score() calls the mapper nine times per model.
    """
    global _QUIZ_OPTS
    if _QUIZ_OPTS is None:
        _QUIZ_OPTS = {}
        src = DATA / "quiz_crowd_li" / "Datasets"
        for sub, prefix in QUIZ_SUBSETS.items():
            with open(src / sub / "quiz.csv") as fh:
                for i, r in enumerate(csv.DictReader(fh), start=1):
                    _QUIZ_OPTS[f"{prefix}{i}"] = {
                        c for c in r if c and len(c) == 1 and c.isalpha()}
    return _QUIZ_OPTS


def map_quiz(recs, proto):
    """Letter answer, passed through -- gold is a letter too, so no recast applies.

    An answer OUTSIDE that item's option set is REJECTED rather than kept, the same
    way conll_ner rejects a tag/token length mismatch. This matters here because the
    subsets carry 4, 5, or 6 options: answering "F" on a four-option question is a
    failure to follow the prompt, and scoring it as a wrong-but-valid choice would
    quietly credit the model with an attempt it never legitimately made.

    The same mapper serves all three groups. The confirmation-bias prompt also
    returns a plain letter -- only the question framing changes, not the answer space.
    """
    opts = quiz_options()
    pred, dropped = {}, 0
    for r in recs:
        c = _letter(top_answer(r.get("parsed"), proto))
        if c is None or c not in opts.get(r["id"], ()):
            dropped += 1
            continue
        pred[r["id"]] = c
    return {"quiz": pred}, dropped


_IMG_CATS = {}


def image_cats(table):
    """Ordered category list for an image dataset, derived from its GOLD table.

    Not hard-coded and not imported from prompt/: the gold table is the single source of
    truth, so the scorer cannot drift from the data. sorted() reproduces the prompts'
    ordering exactly because both prompt groups list categories ALPHABETICALLY -- which is
    also what makes the letter mapping in the customized group well defined (A = first
    alphabetically). The count is asserted so a silent change in either would fail loudly.
    """
    if table not in _IMG_CATS:
        with open(LONG / f"{table}_gold.csv") as fh:
            cats = sorted({r["true_label"] for r in csv.DictReader(fh)})
        want = {"labelme": 8, "imagenet16h": 16}[table]
        if len(cats) != want:
            raise SystemExit(f"{table}: expected {want} categories, gold has {len(cats)}")
        _IMG_CATS[table] = cats
    return _IMG_CATS[table]


def _norm_cat(s):
    """Fold a category string for matching: lowercase, strip anything non-alphanumeric.

    Three LabelMe classes are concatenated words -- `opencountry`, `insidecity`,
    `tallbuilding` -- and a model naturally writes them spaced ("open country"). Matching
    on the raw string rejected those as invalid, which silently penalised the model for
    being RIGHT on 3 of 8 classes. Folding also absorbs hyphens, underscores and stray
    punctuation. It deliberately does NOT do synonym mapping: "city" and "bridge" are not
    categories we offered and stay rejected.
    """
    return "".join(ch for ch in str(s).lower() if ch.isalnum())


# IMAGE DATASETS ONLY (labelme, imagenet16h). Every text dataset's mapper (map_sentiment,
# map_conll_ner, map_pico, map_quiz, map_crowdtruth, map_movie_reviews and their MCQ/
# true_false variants) stays DROP-based, unchanged -- this sentinel-label / never-drop
# policy is scoped to _map_image_name / _map_image_letter only, per explicit instruction.
#
# A category name (or letter) that a model can never legitimately produce, so it can never
# collide with a real answer and always scores as wrong against any real gold label.
IMG_INVALID_LABEL = "__invalid__"


def _map_image_name(recs, proto, table):
    """basic_instruction / control: the model returns a category NAME.

    NEVER DROPS AN INSTANCE. An answer that is not a valid category (refusal, hallucinated
    out-of-vocabulary object, unparseable JSON) is mapped to IMG_INVALID_LABEL rather than
    excluded, so `pred` always has one entry per record in `recs` and n_scored == n_total.
    IMG_INVALID_LABEL never matches a real gold label, so these score as wrong in accuracy
    AND as a genuine (always-incorrect) vote in any crowd-kit aggregation run over the k
    conditions -- it is a real "worker" answer, not a missing one.

    `dropped`/`refused` are now diagnostic counts of how many were mapped to the sentinel
    (not how many were excluded -- nothing is excluded). `refused` isolates the "none of the
    above" pattern, a deliberate non-answer, from other invalid junk.
    """
    valid = {_norm_cat(c): c for c in image_cats(table)}
    refusals = {"noneoftheabove", "none", "unknown", "cannottell", "unclear", "notsure"}
    pred, dropped, refused = {}, 0, 0
    for r in recs:
        a = top_answer(r.get("parsed"), proto)
        key = _norm_cat(a) if a is not None else ""
        hit = valid.get(key)
        if hit is None:
            dropped += 1
            refused += key in refusals
            pred[r["id"]] = IMG_INVALID_LABEL
            continue
        pred[r["id"]] = hit
    return {table: pred}, dropped, refused


def _map_image_letter(recs, proto, table):
    """customized (multiple choice): the model returns a LETTER.

    NEVER DROPS AN INSTANCE, same policy as _map_image_name. An out-of-range letter
    (imagenet16h offers A-P, the widest answer space in the project) is mapped to
    IMG_INVALID_LABEL -- it still counts as an attempt the model made and gets scored as
    wrong, rather than being excluded as if the model never answered.
    """
    cats = image_cats(table)
    pred, dropped = {}, 0
    for r in recs:
        c = _letter(top_answer(r.get("parsed"), proto))
        i = (ord(c) - 65) if c else -1
        if not (0 <= i < len(cats)):
            dropped += 1
            pred[r["id"]] = IMG_INVALID_LABEL
            continue
        pred[r["id"]] = cats[i]
    return {table: pred}, dropped


def map_labelme(recs, proto):
    t, d, _ = _map_image_name(recs, proto, "labelme")
    return t, d


def map_imagenet16h(recs, proto):
    t, d, _ = _map_image_name(recs, proto, "imagenet16h")
    return t, d


def map_labelme_mcq(recs, proto):
    return _map_image_letter(recs, proto, "labelme")


def map_imagenet16h_mcq(recs, proto):
    return _map_image_letter(recs, proto, "imagenet16h")


MAPPERS = {"sentiment": map_sentiment, "movie_reviews": map_movie_reviews,
           "crowdtruth": map_crowdtruth, "conll_ner": map_conll_ner,
           "pico": map_pico, "quiz": map_quiz,
           "labelme": map_labelme, "imagenet16h": map_imagenet16h}

MAPPERS_BY_GROUP = {
    "customized": {"sentiment": map_sentiment_true_false,
                   "movie_reviews": map_movie_reviews_mcq,
                   "conll_ner": map_conll_ner_mcq,
                   # The image sets answer with a category NAME in basic/control but with
                   # a LETTER in customized, so only that group needs the override.
                   "labelme": map_labelme_mcq,
                   "imagenet16h": map_imagenet16h_mcq},
}


def score(model, group):
    gdir = GROUP_DIR[group]
    summary = collections.defaultdict(dict)
    notes = collections.defaultdict(dict)
    for dataset in MAPPERS:
        fn = MAPPERS_BY_GROUP.get(group, {}).get(dataset, MAPPERS[dataset])
        for proto in PROTOCOLS:
            recs = read(model, group, dataset, proto)
            if not recs:
                continue
            n_records = len(recs)
            extra = ""
            if dataset == "conll_ner":
                tables, dropped = fn(recs, proto)
                if dropped:
                    extra = f"{dropped} sentence(s) dropped on tag/token length mismatch"
            elif dataset in ("quiz", "labelme", "imagenet16h"):
                tables, dropped = fn(recs, proto)
                if dropped:
                    extra = f"{dropped} answer(s) dropped (not a valid category/letter)"
            elif dataset == "pico":
                tables, unmatched, tot = fn(recs, proto)
                if unmatched:
                    extra = f"{unmatched}/{tot} spans not found verbatim (dropped)"
            else:
                tables = fn(recs, proto)
            conf = [c for c in (confidence(r.get("parsed"), proto) for r in recs)
                    if c is not None]
            for table, pred in tables.items():
                gold = {r["task"]: r["true_label"]
                        for r in csv.DictReader(open(LONG / f"{table}_gold.csv"))}
                # a mapper may split into sub-conditions (e.g. asserted polarity)
                conds = pred if pred and isinstance(next(iter(pred.values())), dict) \
                    else {None: pred}
                for cond, cpred in conds.items():
                    ids = [i for i in gold if i in cpred]
                    if not ids:
                        continue
                    m = categorical_metrics([gold[i] for i in ids],
                                            [cpred[i] for i in ids],
                                            positive=POSITIVE.get(table))
                    m["coverage"] = len(ids) / len(gold)
                    m["n_scored"] = len(ids)
                    m["n_gold"] = len(gold)
                    m["mean_conf"] = sum(conf) / len(conf) if conf else float("nan")
                    key = proto if cond is None else f"{proto} [assert={cond}]"
                    summary[table][key] = m
                    notes[table][key] = extra or ""
                if len(conds) > 1:
                    a, b = list(conds.values())
                    both = set(a) & set(b)
                    agree = sum(1 for i in both if a[i] == b[i]) / max(len(both), 1)
                    notes[table][proto + " [agreement]"] = (
                        f"the two framings agree on {100*agree:.1f}% of {len(both):,} "
                        f"sentences; disagreement is acquiescence bias, not signal")
            _ = n_records
    return summary, notes


def write(model, group, summary, notes):
    gdir = GROUP_DIR[group]
    for table, byproto in summary.items():
        d = mdir(table, model) / "llm"
        d.mkdir(parents=True, exist_ok=True)
        pos = POSITIVE.get(table)
        cols = ["accuracy", "macro_f1", "weighted_f1"] + ([f"f1_{pos}"] if pos else [])
        with open(d / f"{gdir}.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["protocol"] + cols + ["coverage", "n_scored", "n_gold", "mean_conf"])
            for proto in sorted(byproto):
                if True:
                    m = byproto[proto]
                    w.writerow([proto] + [f"{m.get(c, float('nan')):.4f}" for c in cols]
                               + [f"{m['coverage']:.4f}", m["n_scored"], m["n_gold"],
                                  f"{m['mean_conf']:.1f}"])
        # crowd baseline for context
        best = None
        cf = ddir(table) / "crowd_aggregation.csv"
        if cf.exists():
            rows = list(csv.DictReader(open(cf)))
            best = max(rows, key=lambda r: float(r["macro_f1"]))
        L = [f"# {table} - {model} as a single annotator ({gdir} prompts)", "",
             "Scored directly against ground truth, after the same recast applied to the",
             "human labels. Top-K uses its highest-probability guess.", "",
             "| Protocol | " + " | ".join(c.replace('_', '-') for c in cols)
             + " | coverage | n | mean conf |",
             "|---|" + "--:|" * (len(cols) + 3)]
        for proto in sorted(byproto):
            m = byproto[proto]
            cells = " | ".join(f"{m.get(c, float('nan')):.4f}" for c in cols)
            L.append(f"| {proto} | {cells} | {100*m['coverage']:.1f}% | "
                     f"{m['n_scored']:,}/{m['n_gold']:,} | {m['mean_conf']:.0f} |")
        if best:
            L += ["", f"**Crowd baseline** (best of 8 aggregators): "
                      f"{best['method']} macro-F1 {float(best['macro_f1']):.4f}"]
            bp = max(byproto, key=lambda p: byproto[p]["macro_f1"])
            d_ = byproto[bp]["macro_f1"] - float(best["macro_f1"])
            L.append(f"**Best LLM protocol**: {bp} macro-F1 {byproto[bp]['macro_f1']:.4f} "
                     f"({d_:+.4f} vs crowd)")
        ns = [f"- `{p}`: {n}" for p, n in notes[table].items() if n]
        if ns:
            L += ["", "**Notes**", ""] + ns
        (d / f"{gdir}.md").write_text("\n".join(L) + "\n")
        print(f"  results/{table}/model_analysis/{model}/llm/{gdir}.{{md,csv}}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("--group", default="basic_instruction", choices=sorted(GROUP_DIR))
    a = ap.parse_args()
    s, n = score(a.model, a.group)
    write(a.model, a.group, s, n)

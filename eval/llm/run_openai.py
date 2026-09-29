#!/usr/bin/env python3
"""Run gpt-4o-mini over one dataset x all basic_instruction protocols.

    python eval/llm/run_openai.py <dataset> [--limit N] [--protocols vanilla,cot,topk]

Each dataset uses its own API key (OPENAI_API_KEY_<i> from config.env) so the five
can run concurrently without sharing a rate limit.

Output: llm_output/gpt-4o-mini/basic_instruction/<dataset>_<protocol>.jsonl
One JSON object per line, appended as it completes -- rerunning skips ids already
present, so a run can be resumed after an interruption.
"""
import argparse
import base64
import csv
import hashlib
import json
import os
import pathlib
import random
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets_pass"
LONG = ROOT / "eval" / "data"
PROMPTS = ROOT / "prompt"

# <group>/<protocol>/<template>.txt -- customized files carry the manipulation name
TEMPLATE = {
    "basic_instruction": {d: d for d in
                          ["sentiment", "movie_reviews", "crowdtruth", "conll_ner",
                           "pico", "quiz", "labelme", "imagenet16h"]},
    "control": {"sentiment": "sentiment_paraphrase",
                "movie_reviews": "movie_reviews_paraphrase",
                "crowdtruth": "crowdtruth_paraphrase",
                "conll_ner": "conll_ner_paraphrase",
                "pico": "pico_paraphrase",
                "quiz": "quiz_paraphrase",
                "labelme": "labelme_paraphrase",
                "imagenet16h": "imagenet16h_paraphrase"},
    "customized": {"sentiment": "sentiment_true_false",
                   "movie_reviews": "movie_reviews_sequence_swapping",
                   "crowdtruth": "crowdtruth_sequence_swapping",
                   "conll_ner": "conll_ner_multiple_choice",
                   "pico": "pico_question_answering",
                   "quiz": "quiz_confirmation_bias",
                   "labelme": "labelme_multiple_choice",
                   "imagenet16h": "imagenet16h_multiple_choice"},
}

# Datasets whose stimulus is an IMAGE. Their loaders emit an `_image` key holding an
# absolute path; work() pops it and sends the bytes in the request payload rather than
# interpolating anything into the prompt text (their templates take no placeholder).
IMAGE_DATASETS = {"labelme", "imagenet16h"}

MODEL = "gpt-4o-mini-2024-07-18"        # pinned snapshot, not the moving alias
TEMPERATURE, TOP_P, SEED = 0, 1.0, 42
ENDPOINT = "https://api.openai.com/v1/chat/completions"

# dataset -> OPENAI_API_KEY_<i>
# config.env only defines keys 0-4, so quiz shares key 0. It is by far the smallest
# dataset (155 items = 465 calls per group), so it adds little to that key's rate
# budget -- but do NOT run quiz and sentiment concurrently. Add OPENAI_API_KEY_5 and
# bump this to 5 if you want them fully parallel.
KEY_INDEX = {"sentiment": 0, "movie_reviews": 1, "crowdtruth": 2,
             "conll_ner": 3, "pico": 4, "quiz": 0,
             # The text generation runs are all complete, so the image datasets reuse
             # conll_ner's and pico's keys. Don't run an image dataset concurrently with
             # the text dataset that shares its key.
             "labelme": 3, "imagenet16h": 4}

# Budgets sized from the JSON the model must emit, not from the input length.
# conll_ner writes TWO parallel arrays over up to 60 tokens (tags + per-token
# confidence), so ~60*7 + 60*3 tokens for vanilla, and 3x the tag cost for topk.
# Under-budgeting truncates mid-array and the record fails to parse -- and it fails
# preferentially on the LONGEST sentences, which biases the surviving sample.
# customized/conll_ner is per-TOKEN multiple choice, so its output is tiny
MAX_TOKENS_CUSTOM = {"conll_ner": {"vanilla": 100, "cot": 400, "topk": 250}}

MAX_TOKENS = {
    "sentiment":     {"vanilla": 100, "cot": 400, "topk": 200},
    "movie_reviews": {"vanilla": 100, "cot": 700, "topk": 250},
    "crowdtruth":    {"vanilla": 150, "cot": 500, "topk": 400},
    "conll_ner":     {"vanilla": 1400, "cot": 1800, "topk": 4000},
    "pico":          {"vanilla": 600, "cot": 900, "topk": 2500},
    # quiz emits a single letter plus a confidence, so the JSON is tiny. Budgets are
    # UNIFORM across the three prompt groups and sized to ~5x the measured p99, not to
    # the observed max: truncation is silent and clips the LONGEST generations first,
    # so a tight cap biases the surviving sample toward the easy items.
    #   measured over all 1,395 records per protocol (3 models x 3 groups x 155):
    #     vanilla  median 13  p99  17  ->  100  (5.9x p99, max seen 17)
    #     cot      median 72  p99 175  -> 1200  (6.9x p99)
    #     topk     median 44  p99  76  ->  400  (5.3x p99, max seen 89)
    # cot needs the headroom because five of six subsets are Japanese, and reasoning
    # written in Japanese costs materially more tokens per sentence than the English
    # budgets elsewhere assume. cot was 600 on the first pass and clipped 4 of 4,185
    # records on itm/pok. Nothing ever reached the vanilla or topk caps.
    "quiz":          {"vanilla": 100, "cot": 1200, "topk": 400},
    # Image datasets answer with a category name (basic/control) or a letter (customized)
    # plus a confidence, so the JSON is small; cot carries the only real text. These are
    # PROVISIONAL -- sized generously per the uniform rule, to be re-checked against
    # measured p99 after the pilot rather than tuned down by eye.
    "labelme":       {"vanilla": 150, "cot": 1200, "topk": 400},
    "imagenet16h":   {"vanilla": 150, "cot": 1200, "topk": 400},
}


def load_env():
    """Keys from the process environment, overridden by config.env when present."""
    env = dict(os.environ)
    if not (ROOT / "config.env").is_file():
        return env
    for line in open(ROOT / "config.env", encoding="utf-8-sig"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


# --------------------------------------------------------------- instances
def gold_ids(name):
    with open(LONG / f"{name}_gold.csv") as fh:
        return [r["task"] for r in csv.DictReader(fh)]


def load_sentiment():
    want, seen, out = set(gold_ids("sentiment")), set(), []
    with open(DATA / "sentiment_polarity_ma_lr" / "mturk_answers.csv") as fh:
        for r in csv.DictReader(fh):
            i = r["Input.id"]
            if i in want and i not in seen:
                seen.add(i)
                out.append((i, {"sentence": r["Input.original_sentence"].strip()}))
    return out


def load_movie_reviews():
    texts = [l.strip() for l in open(DATA / "movie_reviews_crowd" / "texts_train.txt")]
    want = set(gold_ids("movie_reviews"))
    return [(f"mr{i}", {"text": t}) for i, t in enumerate(texts) if f"mr{i}" in want]


def load_crowdtruth():
    out, seen = [], set()
    with open(DATA / "crowdtruth_medical_re" / "ground_truth_cause.csv") as fh:
        for r in csv.DictReader(fh):
            if r["SID"] in seen:
                continue
            seen.add(r["SID"])
            out.append((r["SID"], {"sentence": r["sentence"].strip(),
                                   "term1": r["term1"], "term2": r["term2"]}))
    return out


def load_conll_ner():
    """Sentence-level: tokens come from column 0 of answers.txt, sampled sentences only."""
    want = {t.split("_")[0] for t in gold_ids("conll_ner_5k")}
    sents, cur, idx = {}, [], 0
    for line in open(DATA / "conll2003_ner_crowd" / "answers.txt"):
        if not line.strip():
            if cur:
                sents[f"s{idx}"] = cur
                idx, cur = idx + 1, []
            continue
        cur.append(line.split()[0])
    if cur:
        sents[f"s{idx}"] = cur
    return [(s, {"tokens": json.dumps(t)}) for s, t in sents.items() if s in want]


def load_pico():
    # pico_5k: 22 of the 191 gold abstracts (seed 42), matching the crowd baseline
    docs = sorted({t.rsplit("_", 1)[0] for t in gold_ids("pico_5k")})
    return [(d, {"text": (DATA / "pico_data" / "docs" / f"{d}.txt").read_text().strip()})
            for d in docs]


def load_sentiment_true_false():
    """True/False variant: each sentence asked TWICE, counterbalanced over the
    asserted polarity, so we measure the manipulation and not acquiescence bias.
    Ids get a #positive / #negative suffix; the scorer maps the True/False answer
    back to pos/neg using the suffix."""
    out = []
    for tid, kw in load_sentiment():
        for pol in ("positive", "negative"):
            out.append((f"{tid}#{pol}", {**kw, "polarity": pol}))
    return out


def load_conll_ner_tokens():
    """Multiple-choice variant: one call PER TOKEN, so the prompt unit equals the
    scoring unit. Ids are s<sent>_t<tok>, matching the gold table directly."""
    out = []
    for sid, kw in load_conll_ner():
        toks = json.loads(kw["tokens"])
        sent = " ".join(toks)
        for i, t in enumerate(toks):
            out.append((f"{sid}_t{i}", {"sentence": sent, "index": i, "token": t}))
    return out


QUIZ_SUBSETS = {"CHINESE": "chi", "ENGLISH": "eng", "ITMANAGE": "itm",
                "MEDICINE": "med", "POKEMON": "pok", "SCIENCE": "sci"}


def _quiz_rows():
    """[(task, question, {letter: text}, [letters])] across the six subsets.

    Rows map to task ids POSITIONALLY, not by question_id: ENGLISH/quiz.csv keeps the
    original source ids (1,2,3,4,6,7,...,59) while its truth.csv and answer.csv were
    renumbered 1..30, so an id join misplaces 25 of its 30 rows. This mirrors how
    eval/convert/build_quiz.py assigns the gold ids, so the two stay joinable.

    Option letters are read per row rather than fixed: subsets carry 4, 5, or 6.
    """
    src = DATA / "quiz_crowd_li" / "Datasets"
    out = []
    for sub, prefix in QUIZ_SUBSETS.items():
        with open(src / sub / "quiz.csv") as fh:
            for i, r in enumerate(csv.DictReader(fh), start=1):
                letters = sorted(c for c in r if c and len(c) == 1 and c.isalpha())
                out.append((f"{prefix}{i}", r["question"].strip(),
                            {c: (r[c] or "").strip() for c in letters}, letters))
    return out


def _quiz_kwargs(question, opts, letters):
    return {"question": question,
            "options": "\n".join(f"{c}. {opts[c]}" for c in letters),
            "letters": ", ".join(letters)}


def load_quiz():
    want = set(gold_ids("quiz"))
    return [(t, _quiz_kwargs(q, opts, letters))
            for t, q, opts, letters in _quiz_rows() if t in want]


def load_quiz_confirmation_bias():
    """Confirmation-bias variant: a suggested answer is planted before the question.

    The planted option is drawn INDEPENDENTLY OF GOLD -- reading the answer key at
    prompt-build time is the same leak that keeps GoldMajorityVote out of the
    aggregator set. About 1/k of items therefore land on the correct option by
    chance, which is what makes the planted-right vs planted-wrong split meaningful.

    One `random.Random(42)` stream is consumed over the canonically sorted task list,
    matching the project's seeding convention. Because the draw happens once at
    map-build time rather than inside the generation loop, retries and partial
    re-runs cannot shift which option any question gets.
    """
    want = set(gold_ids("quiz"))
    rows = [r for r in _quiz_rows() if r[0] in want]
    order = sorted(rows, key=lambda r: (r[0][:3], int(r[0][3:])))
    rng = random.Random(42)
    plant = {t: rng.choice(letters) for t, _, _, letters in order}
    out = []
    for t, q, opts, letters in rows:
        c = plant[t]
        out.append((t, {**_quiz_kwargs(q, opts, letters),
                        "suggestion": f"({c}) {opts[c]}"}))
    return out


def load_labelme():
    """Scene images. Task id is the file stem, matching labelme_gold.csv.

    Only the 1,000 TRAIN images have crowd labels, and datasets_pass holds only those.
    The class subdirectory is recovered from the gold table rather than guessed from the
    filename prefix -- `street_hexp30.jpg` happens to encode its class, but relying on that
    would break silently if a filename ever did not.
    """
    root = DATA / "labelme_crowd" / "train"
    gold = {}
    with open(LONG / "labelme_gold.csv") as fh:
        for r in csv.DictReader(fh):
            gold[r["task"]] = r["true_label"]
    out = []
    for t, cls in gold.items():
        p = root / cls / f"{t}.jpg"
        if p.exists():
            out.append((t, {"_image": str(p)}))
    return out


def load_imagenet16h():
    """Noise-degraded object images. Task id is `<image>_n<level>`, per imagenet16h_gold.csv.

    The stimulus is the SAME phase-noise-degraded image the crowd saw, not the clean
    original: the instance unit is (image x noise level), and datasets_pass deliberately
    excludes the noiseless copies because no human ever judged them. Showing the model a
    cleaner image than the humans got would make any "AI beats crowd" result an artefact of
    stimulus mismatch rather than a finding about annotators.
    """
    root = DATA / "imagenet16h" / "images"
    out = []
    with open(LONG / "imagenet16h_gold.csv") as fh:
        for r in csv.DictReader(fh):
            name, lvl = r["task"].rsplit("_n", 1)
            p = root / f"phase_noise_{lvl}" / f"{name}.png"
            if p.exists():
                out.append((r["task"], {"_image": str(p)}))
    return out


LOADERS = {"sentiment": load_sentiment, "movie_reviews": load_movie_reviews,
           "crowdtruth": load_crowdtruth, "conll_ner": load_conll_ner,
           "pico": load_pico, "quiz": load_quiz,
           "labelme": load_labelme, "imagenet16h": load_imagenet16h}

# group-specific overrides; anything absent falls back to LOADERS
LOADERS_BY_GROUP = {"customized": {"sentiment": load_sentiment_true_false,
                                   "conll_ner": load_conll_ner_tokens,
                                   "quiz": load_quiz_confirmation_bias}}


# ------------------------------------------------------------------ client
def encode_image(path):
    """-> (base64 payload, mime subtype). Shared by both runners."""
    p = pathlib.Path(path)
    sub = {".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png"}.get(p.suffix.lower())
    if sub is None:
        raise ValueError(f"unsupported image type: {p.suffix}")
    return base64.b64encode(p.read_bytes()).decode(), sub


def call(api_key, prompt, max_tokens, retries=6, image=None):
    # With an image the content becomes a block list. Order is TEXT THEN IMAGE, fixed --
    # swapping those two blocks is itself a prompt manipulation (the taxonomy's Sequence
    # Swapping), so it must not vary silently between runs.
    if image is None:
        content = prompt
    else:
        b64, sub = encode_image(image)
        content = [{"type": "text", "text": prompt},
                   {"type": "image_url",
                    "image_url": {"url": f"data:image/{sub};base64,{b64}"}}]
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": content}],
        "temperature": TEMPERATURE, "top_p": TOP_P, "seed": SEED, "n": 1,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }).encode()
    last = None
    for a in range(retries):
        try:
            req = urllib.request.Request(ENDPOINT, body, {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:200].decode(errors='ignore')}"
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(min(60, 2 ** a) + random.random())
                continue
            break
        except Exception as e:                                   # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
            time.sleep(min(60, 2 ** a) + random.random())
    raise RuntimeError(last)


def extract(raw):
    try:
        return json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
    except Exception:                                            # noqa: BLE001
        return None


def run(dataset, protocols, limit, workers, group="basic_instruction"):
    env = load_env()
    key = env.get(f"OPENAI_API_KEY_{KEY_INDEX[dataset]}") or env["OPENAI_API_KEY"]
    loader = LOADERS_BY_GROUP.get(group, {}).get(dataset, LOADERS[dataset])
    items = loader()
    if limit:
        items = items[:limit]
    out_dir = ROOT / "llm_output" / "gpt-4o-mini" / group
    out_dir.mkdir(parents=True, exist_ok=True)
    budget = (MAX_TOKENS_CUSTOM.get(dataset, MAX_TOKENS[dataset])
              if group == "customized" else MAX_TOKENS[dataset])

    for proto in protocols:
        tmpl = (PROMPTS / group / proto / f"{TEMPLATE[group][dataset]}.txt").read_text()
        path = out_dir / f"{dataset}_{proto}.jsonl"
        done = set()
        if path.exists():
            for line in open(path):
                try:
                    done.add(json.loads(line)["id"])
                except Exception:                                # noqa: BLE001
                    pass
        todo = [(i, kw) for i, kw in items if i not in done]
        print(f"[{dataset}/{proto}] {len(todo)} to do "
              f"({len(done)} already present of {len(items)})", flush=True)
        if not todo:
            continue

        lock, fh = threading.Lock(), open(path, "a")
        n_ok = n_err = 0
        mt = budget[proto]

        def work(item):
            nonlocal n_ok, n_err
            tid, kw = item
            # NOTE: read with .get and filter -- do NOT pop. `items` is built ONCE before
            # the protocol loop, so the same kwargs dicts are reused for vanilla, cot and
            # topk. Popping removed the image after the FIRST protocol, and cot/topk then
            # ran with no image at all (they scored at chance while vanilla scored 0.80).
            img = kw.get("_image")
            prompt = tmpl.format(**{k: v for k, v in kw.items() if k != "_image"})
            rec = {"id": tid, "dataset": dataset, "protocol": proto, "model": MODEL,
                   "group": group,
                   "prompt_sha1": hashlib.sha1(prompt.encode()).hexdigest()[:12]}
            try:
                resp = call(key, prompt, mt, image=img)
                raw = resp["choices"][0]["message"]["content"]
                rec.update(raw=raw, parsed=extract(raw),
                           finish_reason=resp["choices"][0].get("finish_reason"),
                           system_fingerprint=resp.get("system_fingerprint"),
                           usage=resp.get("usage"))
            except Exception as e:                               # noqa: BLE001
                rec.update(error=str(e)[:300], parsed=None)
            with lock:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                if rec.get("error") or rec.get("parsed") is None:
                    n_err += 1
                else:
                    n_ok += 1
                t = n_ok + n_err
                if t % 100 == 0 or t == len(todo):
                    print(f"[{dataset}/{proto}] {t}/{len(todo)}  ok={n_ok} bad={n_err}",
                          flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, todo))
        fh.close()
        print(f"[{dataset}/{proto}] DONE ok={n_ok} bad={n_err} -> {path}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset", choices=sorted(LOADERS))
    ap.add_argument("--protocols", default="vanilla,cot,topk")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--group", default="basic_instruction",
                    choices=["basic_instruction", "control", "customized"])
    a = ap.parse_args()
    run(a.dataset, a.protocols.split(","), a.limit, a.workers, a.group)
    print("ALL_DONE", flush=True)

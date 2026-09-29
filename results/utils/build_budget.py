#!/usr/bin/env python3
"""Annotation effort: how many human judgments each dataset costs, and what
routing saves.

    python results/utils/build_budget.py [model]

EFFORT IS COUNTED IN JUDGMENTS, NOT MONEY. A judgment is one annotator labelling one
instance once. Dollar figures were removed deliberately: annotator expertise is not
uniform across these corpora -- crowdtruth and pico use medical/clinical judgement,
sentiment and labelme use open crowds -- so no single hourly rate is defensible, and
the seconds-per-judgment it would multiply was an ASSUMPTION on 5 of the 8 datasets.
Judgment counts rest on neither.

A judgment is counted as a DISTINCT (effort, worker) pair, not a row:
  - crowdtruth_pooled namespaces one sentence into c<id>/t<id>, but a single
    CrowdFlower HIT answered both relation questions, so its rows overstate human
    effort by 64% (24,530 rows vs 14,920 real HITs);
  - imagenet16h contains 6 rows where one worker labelled the same image twice.

LLM token volumes are still recorded -- they are a factual measure of machine work --
but are not converted to currency.

ROUTING. The LLM must label every instance to rank them, but contributes ZERO human
judgments at any budget. So the effort saved by routing X% to humans is exactly the
judgments the crowd did not have to make. The exact per-budget count is computed in
build_allocation_best.py from splits.csv; the judgments_at_X* columns here prorate by
instance share and are indicative only.

Writes results/budget_<model>.csv
"""
import collections
import csv
import datetime
import glob
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RES = ROOT / "results"
DATA = ROOT / "datasets_pass"
LONG = ROOT / "eval" / "data"


# Recorded for provenance only -- nothing here is priced. Kept so llm_hosting can
# distinguish machine work done on owned GPUs from work sent to a hosted API.
LOCAL_MODELS = {"llama3.1-8b-instruct-q8_0", "qwen2.5-7b-instruct-q8_0",
                # image arm: both VLMs run on the owned GPUs via ollama, same as the
                # text open models. Only gpt-4o-mini is actually billed per token.
                "minicpm-v-8b-2.6-q8_0", "qwen2.5vl-7b-q8_0"}

# eval table -> generation dataset
SOURCE = {"sentiment": "sentiment", "movie_reviews": "movie_reviews",
          "crowdtruth_cause": "crowdtruth", "crowdtruth_treat": "crowdtruth",
          "crowdtruth_pooled": "crowdtruth",
          "conll_ner_5k": "conll_ner", "pico_5k": "pico", "quiz": "quiz",
          "labelme": "labelme", "imagenet16h": "imagenet16h"}


def ddir(ds):
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def llm_cost(model):
    """Exact $ per dataset for the 9 majority-vote conditions (basic_instruction).

    Local models bill nothing: tokens are still counted (so the volume is on record)
    but priced at zero, since the GPUs are owned rather than rented.
    """
    tot = collections.defaultdict(lambda: [0, 0, 0])
    for ds in set(SOURCE.values()):
        for p in ("vanilla", "cot", "topk"):
            f = ROOT / "llm_output" / model / "basic_instruction" / f"{ds}_{p}.jsonl"
            if not f.exists():
                continue
            for line in open(f):
                try:
                    u = (json.loads(line).get("usage") or {})
                except Exception:                                # noqa: BLE001
                    continue
                tot[ds][0] += u.get("prompt_tokens") or 0
                tot[ds][1] += u.get("completion_tokens") or 0
                tot[ds][2] += 1
    return tot


def main(model):
    llm = llm_cost(model)
    rows = []
    for table, src in SOURCE.items():
        gold = list(csv.DictReader(open(LONG / f"{table}_gold.csv")))
        crowd = list(csv.DictReader(open(LONG / f"{table}_crowd.csv")))
        n_inst = len(gold)
        # Human effort = DISTINCT (effort, worker) pairs. crowdtruth_pooled splits one
        # sentence into c<id>/t<id>, but a single HIT answered both relation questions,
        # so its rows overstate effort by 64%; imagenet16h has 6 duplicate rows where a
        # worker labelled an image twice. Both are collapsed here.
        _key = (lambda t: t[1:]) if table == "crowdtruth_pooled" else (lambda t: t)
        n_judg = len({(_key(r["task"]), r["worker"]) for r in crowd})

        # Token volumes for the 9 majority-vote conditions. crowdtruth_cause,
        # crowdtruth_treat and crowdtruth_pooled all read the SAME generation, so their
        # token counts are identical and must never be summed -- pooled is an
        # alternative view of the other two, not extra work.
        i, o, _n_rec = llm[src]

        rows.append({
            "dataset": table, "instances": n_inst, "human_judgments": n_judg,
            "judgments_per_instance": f"{n_judg / n_inst:.2f}",
            "llm_tokens_in": i, "llm_tokens_out": o,
            "llm_hosting": "local" if model in LOCAL_MODELS else "hosted API",
            **{f"judgments_at_X{x}": round(n_judg * x / 100)
               for x in (5, 10, 25, 50, 75)},
            **{f"effort_saved_at_X{x}": f"{100 - x}.0%"
               for x in (5, 10, 25, 50, 75)},
        })

    out = RES / f"budget_{model}.csv"
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"  {r['dataset']:18s} {r['instances']:>6,} instances  "
              f"{r['human_judgments']:>7,} judgments  "
              f"{r['judgments_per_instance']:>5s}/inst  "
              f"save@25% {r['effort_saved_at_X25']:>6s}")
    print(f"\n  {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "gpt-4o-mini")

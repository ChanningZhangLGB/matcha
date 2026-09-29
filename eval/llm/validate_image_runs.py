#!/usr/bin/env python3
"""Health gate for the IMAGE arm (labelme, imagenet16h). Run it during and after generation.

    python eval/llm/validate_image_runs.py            # check everything present
    python eval/llm/validate_image_runs.py --strict   # exit 1 on WARN as well as FAIL

Exists because a silent defect nearly reached the analysis: `work()` popped `_image` out of
the kwargs dict, which is built ONCE and reused across protocols, so `vanilla` consumed the
image and `cot`/`topk` ran with none. Accuracy collapsed to chance while `vanilla` scored
0.80, and the raw output still looked perfectly well-formed. Every check below is aimed at
catching that class of failure -- output that parses cleanly but is not what it claims.

FAIL = the data is invalid and must be regenerated.
WARN = behaviour worth a human decision, not necessarily wrong.
"""
import argparse
import collections
import csv
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "eval" / "llm"))
import run_openai as R                                          # noqa: E402
import score_llm as S                                           # noqa: E402

OUT = ROOT / "llm_output"
LONG = ROOT / "eval" / "data"
DATASETS = {"labelme": 8, "imagenet16h": 16}
PROTOCOLS = ["vanilla", "cot", "topk"]
GROUPS = ["basic_instruction", "control", "customized"]
fails, warns = [], []


def gold_of(ds):
    with open(LONG / f"{ds}_gold.csv") as fh:
        return {r["task"]: r["true_label"] for r in csv.DictReader(fh)}


def recs_of(m, g, ds, p):
    f = OUT / m / g / f"{ds}_{p}.jsonl"
    if not f.exists():
        return None
    return [json.loads(l) for l in open(f)]


def check_loaders():
    """Every task id must resolve to the file it claims -- right class / noise / name."""
    bad = [t for t, kw in R.load_labelme()
           if pathlib.Path(kw["_image"]).parent.name != gold_of("labelme")[t]]
    if bad:
        fails.append(f"labelme loader: {len(bad)} ids map to the wrong class dir")
    bad = [t for t, kw in R.load_imagenet16h()
           if pathlib.Path(kw["_image"]).parent.name != "phase_noise_" + t.rsplit("_n", 1)[1]
           or pathlib.Path(kw["_image"]).stem != t.rsplit("_n", 1)[0]]
    if bad:
        fails.append(f"imagenet16h loader: {len(bad)} ids map to the wrong stimulus")
    print(f"  loaders: labelme + imagenet16h id->file mapping "
          f"{'OK' if not fails else 'FAILED'}")


def check_one(m, g, ds):
    gold = gold_of(ds)
    chance = 1.0 / DATASETS[ds]
    med = {}
    for p in PROTOCOLS:
        rs = recs_of(m, g, ds, p)
        if not rs:
            continue
        tag = f"{m}/{g}/{ds}_{p}"

        # -- prompt_sha1 must be constant: image templates carry no placeholder, so the
        #    image is the only thing that varies between records.
        if len({r.get("prompt_sha1") for r in rs}) != 1:
            fails.append(f"{tag}: prompt_sha1 varies -- template is not fixed")

        tok = [(r.get("usage") or {}).get("prompt_tokens") for r in rs]
        tok = [t for t in tok if t]
        if tok:
            med[p] = statistics.median(tok)

        # -- accuracy: blind guessing sits at chance while a sighted run is far above it
        fn = S.MAPPERS_BY_GROUP.get(g, {}).get(ds, S.MAPPERS[ds])
        out = fn(rs, p)
        pred = (out[0] if isinstance(out, tuple) else out)[ds]
        dropped = out[1] if isinstance(out, tuple) else 0
        ids = [i for i in pred if i in gold]
        acc = sum(pred[i] == gold[i] for i in ids) / max(len(ids), 1)
        if len(ids) >= 100 and acc < 2 * chance:
            fails.append(f"{tag}: acc={acc:.4f} at chance ({chance:.3f}) on {len(ids)} items "
                         f"-- model is answering blind, image probably missing")
        if dropped:
            warns.append(f"{tag}: {dropped} answers dropped (invalid category/letter)")

        # -- top-k structure
        if p == "topk":
            ks = collections.Counter()
            topprob = []
            for r in rs:
                gs = (r.get("parsed") or {}).get("guesses")
                if not isinstance(gs, list):
                    continue
                ks[len(gs)] += 1
                pr = [x.get("probability") for x in gs if isinstance(x, dict)]
                pr = [x for x in pr if isinstance(x, (int, float))]
                if pr:
                    topprob.append(pr[0])
                    if pr != sorted(pr, reverse=True):
                        warns.append(f"{tag}: probabilities not descending")
            off = sum(v for k, v in ks.items() if k != 3)
            if off:
                warns.append(f"{tag}: {off}/{sum(ks.values())} records returned k!={3} "
                             f"(k dist {dict(sorted(ks.items()))})")
            if topprob and len(set(topprob)) < 3:
                warns.append(f"{tag}: top probability takes only {len(set(topprob))} distinct "
                             f"value(s) {sorted(set(topprob))} -- u_confidence from topk "
                             f"cannot rank instances on this dataset")

    # -- image-presence signature: a protocol missing its image loses most of its prompt
    if "vanilla" in med:
        for p, v in med.items():
            if p != "vanilla" and v < 0.5 * med["vanilla"]:
                fails.append(f"{m}/{g}/{ds}: {p} median prompt={v:.0f} vs vanilla "
                             f"{med['vanilla']:.0f} -- image missing from {p}")
    if med:
        print(f"  {m:22s} {g:18s} {ds:12s} median prompt tokens: "
              + "  ".join(f"{p}={med[p]:.0f}" for p in PROTOCOLS if p in med))


def main(strict):
    print("=== IMAGE ARM HEALTH GATE ===")
    check_loaders()
    for m in sorted(p.name for p in OUT.iterdir() if p.is_dir() and p.name != "logs"):
        for g in GROUPS:
            for ds in DATASETS:
                if (OUT / m / g).exists():
                    check_one(m, g, ds)
    print(f"\nFAIL ({len(fails)}):")
    for x in fails:
        print("  ✗", x)
    print(f"WARN ({len(warns)}):")
    for x in warns:
        print("  !", x)
    if not fails and not warns:
        print("  (none) — image arm healthy")
    return 1 if (fails or (strict and warns)) else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    sys.exit(main(ap.parse_args().strict))

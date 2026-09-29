#!/usr/bin/env python3
"""Strip failed records from the llm_output JSONL, then re-run exactly those ids.

The runners resume by id, so a record that failed is still "present" and would be
skipped forever. This removes the failed lines first; a rerun then regenerates
precisely the missing ids under the corrected MAX_TOKENS budgets.

    python eval/llm/patch_failures.py            # report only
    python eval/llm/patch_failures.py --strip    # remove failed lines
    python eval/llm/patch_failures.py --strip --rerun
"""
import argparse
import collections
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "llm_output"
PY = sys.executable

OLLAMA_TAG = {"llama3.1-8b-instruct-q8_0": "llama3.1:8b-instruct-q8_0",
              "qwen2.5-7b-instruct-q8_0": "qwen2.5:7b-instruct-q8_0"}


def is_bad(r):
    return bool(r.get("error")) or r.get("parsed") is None


GROUPS = ("basic_instruction", "control", "customized")


def scan(only_model=None):
    """-> {(model, group, dataset, protocol): (path, n_total, n_bad, reasons)}"""
    found = {}
    for p in sorted(OUT.glob("*/*/*.jsonl")):
        group = p.parent.name
        if group not in GROUPS:
            continue
        model = p.parent.parent.name
        if only_model and model != only_model:
            continue
        stem = p.stem
        for proto in ("vanilla", "cot", "topk"):
            if stem.endswith("_" + proto):
                dataset = stem[: -len(proto) - 1]
                break
        else:
            continue
        n = bad = 0
        reasons = collections.Counter()
        for line in open(p):
            try:
                r = json.loads(line)
            except Exception:                                    # noqa: BLE001
                continue
            n += 1
            if is_bad(r):
                bad += 1
                reasons[r.get("finish_reason") or r.get("done_reason")
                        or (r.get("error") or "?")[:40]] += 1
        if bad:
            found[(model, group, dataset, proto)] = (p, n, bad, reasons)
    return found


def strip(path):
    keep = []
    removed = 0
    for line in open(path):
        try:
            r = json.loads(line)
        except Exception:                                        # noqa: BLE001
            removed += 1                                         # truncated last line
            continue
        if is_bad(r):
            removed += 1
        else:
            keep.append(line if line.endswith("\n") else line + "\n")
    tmp = path.with_suffix(".jsonl.tmp")
    tmp.write_text("".join(keep))
    tmp.replace(path)
    return removed


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--strip", action="store_true")
    ap.add_argument("--rerun", action="store_true")
    ap.add_argument("--model", default=None,
                    help="restrict to one model dir (avoid touching files being written)")
    a = ap.parse_args()

    found = scan(a.model)
    if not found:
        print("no failed records found")
        sys.exit(0)

    total = 0
    for (model, group, ds, proto), (p, n, bad, reasons) in sorted(found.items()):
        total += bad
        print(f"  {model:26s} {group:18s} {ds}_{proto:8s} {bad:4d}/{n:5d}  "
              f"{dict(reasons)}")
    print(f"\n{total} failed records across {len(found)} files")

    if not a.strip:
        print("\n(dry run - pass --strip to remove, --strip --rerun to regenerate)")
        sys.exit(0)

    for key, (p, *_rest) in sorted(found.items()):
        print(f"stripped {strip(p):4d} from {p.relative_to(OUT)}")

    if not a.rerun:
        sys.exit(0)

    jobs = collections.defaultdict(list)
    for (model, group, ds, proto) in found:
        jobs[(model, group, ds)].append(proto)
    for (model, group, ds), protos in sorted(jobs.items()):
        protos = ",".join(sorted(set(protos), key=["vanilla", "cot", "topk"].index))
        if model == "gpt-4o-mini":
            cmd = [PY, "-u", str(ROOT / "eval/llm/run_openai.py"), ds,
                   "--group", group, "--protocols", protos, "--workers", "8"]
        else:
            cmd = [PY, "-u", str(ROOT / "eval/llm/run_ollama.py"), OLLAMA_TAG[model], ds,
                   "--group", group, "--protocols", protos, "--workers", "2"]
        print("RUN:", " ".join(cmd), flush=True)
        subprocess.run(cmd, check=False)
    print("PATCH_COMPLETE", flush=True)

#!/usr/bin/env python3
"""Run a local ollama model over one dataset x all basic_instruction protocols.

    python eval/llm/run_ollama.py <model_tag> <dataset> [--limit N] [--workers K]

Shares the dataset loaders and the resume-by-id behaviour with run_openai.py, so
the two model families produce directly comparable JSONL.

Sampling is pinned to match the OpenAI side (temperature 0, top_p 1.0, seed 42).
Three ollama-specific defaults are overridden because they would silently corrupt
these runs:

  repeat_penalty  default 1.1 -> 1.0   penalising repeats mangles CoNLL tag arrays,
                                       which are legitimately mostly repeated "O"
  top_k           default 40  -> 0     OpenAI has no equivalent; disable it
  num_ctx         small default -> 8192  an over-long prompt is silently TRUNCATED
                                       FROM THE LEFT, cutting off the instruction
"""
import argparse
import hashlib
import json
import os
import pathlib
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from run_openai import (LOADERS, LOADERS_BY_GROUP, MAX_TOKENS,   # noqa: E402
                        MAX_TOKENS_CUSTOM, PROMPTS, ROOT, TEMPLATE,
                        encode_image)

HOST = os.environ.get("OLLAMA_HOST", "127.0.0.1:11435")
ENDPOINT = f"http://{HOST}/api/generate"
TEMPERATURE, TOP_P, SEED = 0, 1.0, 42
NUM_CTX = 8192

SAFE = {"llama3.1:8b-instruct-q8_0": "llama3.1-8b-instruct-q8_0",
        "qwen2.5:7b-instruct-q8_0": "qwen2.5-7b-instruct-q8_0"}


def call(model, prompt, num_predict, retries=5, image=None):
    # ollama's /api/generate takes images as a list of bare base64 strings (no data: URI
    # and no mime prefix -- that form is the OpenAI content-block convention, not this one).
    payload = {
        "model": model, "prompt": prompt, "stream": False, "format": "json",
        "keep_alive": "60m",
        "options": {
            "temperature": TEMPERATURE, "top_p": TOP_P, "top_k": 0,
            "repeat_penalty": 1.0, "seed": SEED,
            "num_ctx": NUM_CTX, "num_predict": num_predict,
        },
    }
    if image is not None:
        payload["images"] = [encode_image(image)[0]]
    body = json.dumps(payload).encode()
    last = None
    for a in range(retries):
        try:
            req = urllib.request.Request(ENDPOINT, body, {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=900) as r:
                return json.load(r)
        except Exception as e:                                   # noqa: BLE001
            last = f"{type(e).__name__}: {str(e)[:200]}"
            time.sleep(min(30, 2 ** a))
    raise RuntimeError(last)


def extract(raw):
    try:
        return json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
    except Exception:                                            # noqa: BLE001
        return None


def run(model, dataset, protocols, limit, workers, group="basic_instruction"):
    out_dir = ROOT / "llm_output" / SAFE.get(model, model.replace(":", "-")) / group
    out_dir.mkdir(parents=True, exist_ok=True)
    loader = LOADERS_BY_GROUP.get(group, {}).get(dataset, LOADERS[dataset])
    items = loader()
    if limit:
        items = items[:limit]
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
        print(f"[{model}|{dataset}/{proto}] {len(todo)} to do "
              f"({len(done)} present of {len(items)})", flush=True)
        if not todo:
            continue

        lock, fh = threading.Lock(), open(path, "a")
        n_ok = n_err = 0
        np_ = budget[proto]

        def work(item):
            nonlocal n_ok, n_err
            tid, kw = item
            # NOTE: read with .get and filter -- do NOT pop. `items` is built ONCE before
            # the protocol loop, so the same kwargs dicts are reused for vanilla, cot and
            # topk. Popping removed the image after the FIRST protocol, and cot/topk then
            # ran with no image at all (they scored at chance while vanilla scored 0.80).
            img = kw.get("_image")
            prompt = tmpl.format(**{k: v for k, v in kw.items() if k != "_image"})
            rec = {"id": tid, "dataset": dataset, "protocol": proto, "model": model,
                   "group": group,
                   "prompt_sha1": hashlib.sha1(prompt.encode()).hexdigest()[:12]}
            try:
                resp = call(model, prompt, np_, image=img)
                raw = resp.get("response", "")
                rec.update(raw=raw, parsed=extract(raw),
                           done_reason=resp.get("done_reason"),
                           usage={"prompt_tokens": resp.get("prompt_eval_count"),
                                  "completion_tokens": resp.get("eval_count")})
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
                    print(f"[{model}|{dataset}/{proto}] {t}/{len(todo)} "
                          f"ok={n_ok} bad={n_err}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, todo))
        fh.close()
        print(f"[{model}|{dataset}/{proto}] DONE ok={n_ok} bad={n_err} -> {path}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("dataset", choices=sorted(LOADERS))
    ap.add_argument("--protocols", default="vanilla,cot,topk")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--group", default="basic_instruction",
                    choices=["basic_instruction", "control", "customized"])
    a = ap.parse_args()
    run(a.model, a.dataset, a.protocols.split(","), a.limit, a.workers, a.group)
    print("ALL_DONE", flush=True)

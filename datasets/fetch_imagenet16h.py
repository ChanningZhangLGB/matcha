import json, os, sys, time, urllib.request
ROOT = "https://files.osf.io/v1/resources/2ntrf/providers/osfstorage/"
DST  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenet16h")
n_f = n_b = n_skip = 0

def get(url, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(url, timeout=120).read()
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))

def walk(path="", rel=""):
    global n_f, n_b, n_skip
    data = json.loads(get(ROOT + path))["data"]
    for f in data:
        a = f["attributes"]
        out = os.path.join(DST, rel, a["name"])
        if a["kind"] == "folder":
            os.makedirs(out, exist_ok=True)
            walk(a["path"].lstrip("/") + "/", os.path.join(rel, a["name"]))
        else:
            sz = a.get("size") or 0
            if os.path.exists(out) and os.path.getsize(out) == sz:
                n_skip += 1
                continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "wb") as fh:
                fh.write(get(a["links"]["download"] if "links" in a else
                             f"https://osf.io/download/{f['id'].split('/')[-1]}/"))
            n_f += 1; n_b += sz
            if n_f % 250 == 0:
                print(f"  {n_f} files, {n_b/1e6:,.0f} MB", flush=True)

os.makedirs(DST, exist_ok=True)
walk()
print(f"DONE: {n_f} downloaded ({n_b/1e6:,.1f} MB), {n_skip} already present")

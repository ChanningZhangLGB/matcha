#!/usr/bin/env python3
"""Build datasets_pass/ from datasets/.

Four datasets are copied whole (every instance already has gold + per-annotator labels).
Two are filtered down to the gold-labelled subset:

  crowdtruth_medical_re -> the 975 sentences with a non-NA `expert` column, plus the
                           per-worker judgments in raw/ that join to them (base SID =
                           sent_id up to the first '-').
  pico_data            -> the acl17-test split (191 docs), the only one with professional
                           (expert) annotations.

`quiz_crowd_li` is copied whole but is NOT comparable in scale to the other five: 155
multiple-choice items over 6 subsets, against 18,128 instances elsewhere. See its entry
in datasets_pass/README.md for the caveats that govern how it may be used.
"""
import csv, glob, json, os, shutil, sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets_pass")

FULL = ["sentiment_polarity_ma_lr", "movie_reviews_crowd", "conll2003_ner_crowd",
        "quiz_crowd_li"]


def copy_full():
    for d in FULL:
        s, t = f"{SRC}/{d}", f"{DST}/{d}"
        if os.path.exists(t):
            shutil.rmtree(t)
        shutil.copytree(s, t)
        print(f"[full] {d}")


def filter_crowdtruth():
    s, t = f"{SRC}/crowdtruth_medical_re", f"{DST}/crowdtruth_medical_re"
    if os.path.exists(t):
        shutil.rmtree(t)
    os.makedirs(f"{t}/raw", exist_ok=True)

    gold = set()
    for f in ["ground_truth_cause.csv", "ground_truth_treat.csv"]:
        rows = list(csv.DictReader(open(f"{s}/{f}")))
        keep = [r for r in rows if r["expert"] not in ("NA", "")]
        gold |= {r["SID"] for r in keep}
        with open(f"{t}/{f}", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(keep)
        print(f"[crowdtruth] {f}: {len(rows)} -> {len(keep)} expert-labelled")

    for task in ["RelEx", "RelDir", "FactSpan"]:
        os.makedirs(f"{t}/raw/{task}", exist_ok=True)
        n = kept = 0
        for f in sorted(glob.glob(f"{s}/raw/{task}/*.csv")):
            rows = list(csv.DictReader(open(f)))
            n += len(rows)
            sel = [r for r in rows if str(r.get("sent_id", "")).split("-")[0] in gold]
            kept += len(sel)
            if sel:
                with open(f"{t}/raw/{task}/{os.path.basename(f)}", "w", newline="") as fh:
                    w = csv.DictWriter(fh, fieldnames=rows[0].keys())
                    w.writeheader()
                    w.writerows(sel)
        print(f"[crowdtruth] raw/{task}: {n} -> {kept} worker judgments")

    for f in ["README.md", "ground_truth.csv-metadata.json"]:
        shutil.copy2(f"{s}/{f}", f"{t}/{f}")
    shutil.copytree(f"{s}/templates", f"{t}/templates")
    shutil.copytree(f"{s}/train_dev_test", f"{t}/train_dev_test")
    return gold


def filter_pico():
    s, t = f"{SRC}/pico_data", f"{DST}/pico_data"
    if os.path.exists(t):
        shutil.rmtree(t)
    os.makedirs(f"{t}/annotations/acl17-test", exist_ok=True)
    os.makedirs(f"{t}/docs", exist_ok=True)

    docids = set()
    for f in ["PICO-annos-crowdsourcing.json", "PICO-annos-crowdsourcing-agg.json",
              "PICO-annos-professional.json"]:
        p = f"{s}/annotations/acl17-test/{f}"
        lines = open(p).read().splitlines()
        docids |= {json.loads(l)["docid"] for l in lines if l.strip()}
        shutil.copy2(p, f"{t}/annotations/acl17-test/{f}")
    print(f"[pico] acl17-test: {len(docids)} docs with professional gold")

    miss = 0
    for d in sorted(docids):
        p = f"{s}/docs/{d}.txt"
        if os.path.exists(p):
            shutil.copy2(p, f"{t}/docs/{d}.txt")
        else:
            miss += 1
    print(f"[pico] docs copied: {len(docids) - miss} (missing {miss})")

    shutil.copy2(f"{s}/README.md", f"{t}/README.md")
    shutil.copytree(f"{s}/src", f"{t}/src")


def filter_labelme():
    """LabelMe -> the 1,000 TRAIN images only.

    Crowd labels exist ONLY for the train split: `answers.txt` is 1,000 x 77 and the
    valid (500) / test (1,188) splits ship gold but no per-annotator labels. Since the
    working set is defined by "instances that have crowd labels", those two splits are
    dropped. 18 of the 77 worker columns are entirely empty -- they are kept here (the
    file is copied verbatim) and dropped at melt time by the converter, because an
    annotator with zero observations breaks per-worker parameter estimation.
    """
    s, t = f"{SRC}/labelme_crowd", f"{DST}/labelme_crowd"
    if os.path.exists(t):
        shutil.rmtree(t)
    os.makedirs(t, exist_ok=True)
    shutil.copytree(f"{s}/train", f"{t}/train")
    for f in ["answers.txt", "labels_train.txt", "filenames_train.txt",
              "labels_train_names.txt", "answers_mv.txt", "answers_DS.txt"]:
        if os.path.exists(f"{s}/{f}"):
            shutil.copy2(f"{s}/{f}", f"{t}/{f}")
    n = sum(len(fs) for _, _, fs in os.walk(f"{t}/train"))
    print(f"[labelme] {n} train images (valid/test dropped: no crowd labels)")


def filter_imagenet16h():
    """ImageNet-16H -> the 4 phase-noise levels only (4,800 instances).

    The instance unit is (image x noise level), not image: each variant was judged
    separately. All 28,997 human judgments are phase-noise trials at levels 80/95/110/125,
    so the 1,200 `original` (noiseless) images carry gold but NO crowd labels and are
    dropped. The Machine Classifier Predictions and fine-tuned model weights stay in
    ../datasets/ -- they are the source paper's CNN, several GB, and we substitute our
    own VLM annotators.
    """
    s, t = f"{SRC}/imagenet16h", f"{DST}/imagenet16h"
    if os.path.exists(t):
        shutil.rmtree(t)
    os.makedirs(f"{t}/images", exist_ok=True)
    for d in sorted(glob.glob(f"{s}/Noisy Images/phase_noise_*")):
        shutil.copytree(d, f"{t}/images/{os.path.basename(d)}")
    os.makedirs(f"{t}/behavioral", exist_ok=True)
    for f in glob.glob(f"{s}/Behavioral Data/*.csv") + \
             glob.glob(f"{s}/Behavioral Data/Preprocessed/*.csv"):
        shutil.copy2(f, f"{t}/behavioral/{os.path.basename(f)}")
    n = len(glob.glob(f"{t}/images/*/*.png"))
    print(f"[imagenet16h] {n} images = 1,200 x 4 noise levels "
          f"(`original` dropped: no crowd labels)")


def filter_lidc_idri():
    """LIDC-IDRI -> the 38 nodules where an annotator-INDEPENDENT diagnosis is linkable.

    The corpus has 2,749 clustered nodules with 4 independent radiologist reads, but the TCIA
    diagnosis file (biopsy / resection / 2-yr stability / progression) is mostly PATIENT-level,
    and 78 of the 116 diagnosed patients in our index have more than one nodule -- a patient
    diagnosis does not say which nodule is malignant. The nodule-level entries identify the
    nodule only as an ordinal with no coordinates. 38 is the subset where the patient has
    exactly one nodule, so the diagnosis provably belongs to it.

    Deriving gold from the readers instead (>=3-of-4 consensus, or median malignancy) would be
    circular: crowd and gold from the same four people.

    Images are rendered with the LUNG window (WC -600 / WW 1500). The DICOM headers store
    WC 40 / WW 400 (soft tissue), which blacks out the parenchyma and hides the nodule.
    """
    s, t = f"{SRC}/lidc_idri", f"{DST}/lidc_idri"
    if not os.path.exists(s):
        print("[lidc_idri] source not present - skipped")
        return
    os.makedirs(f"{t}/images", exist_ok=True)
    for f in glob.glob(f"{s}/images/*.png"):
        shutil.copy2(f, f"{t}/images/{os.path.basename(f)}")
    for f in ["image_index.csv"]:
        if os.path.exists(f"{s}/{f}"):
            shutil.copy2(f"{s}/{f}", f"{t}/{f}")
    n = len(glob.glob(f"{t}/images/*.png"))
    print(f"[lidc_idri] {n} PNGs (38 nodule crops + 38 full slices); "
          f"annotations_per_reader.csv and gold.csv are built by the LIDC parse")


if __name__ == "__main__":
    os.makedirs(DST, exist_ok=True)
    copy_full()
    filter_crowdtruth()
    filter_pico()
    filter_labelme()
    filter_imagenet16h()
    filter_lidc_idri()
    print("done ->", DST)

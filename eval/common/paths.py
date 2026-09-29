"""Shared paths and constants."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets_pass"
EVAL = ROOT / "eval"
LONG = EVAL / "data"        # generated long-form task/worker/label tables
RESULTS = EVAL / "results"

# MovieReviews: -1 marks a MISSING answer. Note -0.1 and 1.1 are VALID ratings,
# so never filter with `> 0` / `>= 0`.
MR_MISSING = -1.0

# Rating -> class. Explicit cascade, not pd.cut: worker answers include -0.1 and
# 1.1, which fall outside [0, 1] and would become NaN under pd.cut(bins=[0,.35,.65,1]).
MR_BINS = ((0.35, "poor"), (0.65, "medium"), (float("inf"), "good"))


def bin_rating(x):
    """Map a rating to poor/medium/good. Handles values outside [0, 1]."""
    import numpy as np

    x = np.asarray(x, dtype=float)
    out = np.full(x.shape, "good", dtype=object)
    out[x < 0.65] = "medium"
    out[x < 0.35] = "poor"
    return out

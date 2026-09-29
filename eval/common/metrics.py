"""Metrics shared by the two evaluation tracks."""
import numpy as np
from sklearn.metrics import accuracy_score, f1_score


def categorical_metrics(y_true, y_pred, positive=None):
    """Accuracy + macro/weighted F1. `positive` adds binary F1 for that class."""
    out = {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
    }
    if positive is not None and positive in set(y_true):
        out["f1_" + str(positive)] = f1_score(
            y_true, y_pred, pos_label=positive, average="binary", zero_division=0
        )
    return out


def regression_metrics(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    err = y_pred - y_true
    ss_res = float((err ** 2).sum())
    ss_tot = float(((y_true - y_true.mean()) ** 2).sum())
    return {
        "MAE": float(np.abs(err).mean()),
        "RMSE": float(np.sqrt((err ** 2).mean())),
        "R2": 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan"),
        "pearson_r": float(np.corrcoef(y_pred, y_true)[0, 1]),
    }

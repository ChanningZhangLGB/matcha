"""Where results live.

    results/<dataset>/
    ├── crowd_aggregation.{csv,md}      human-only, shared
    ├── summary_table.{csv,md}          integrated, all models
    ├── allocation/<measure>/<route>/   routing (model in the filename)
    └── model_analysis/<model>/         everything specific to one model
        ├── prompt_comparison.{csv,md}
        ├── majority_vote.{csv,md}
        ├── uncertainty_per_instance.csv
        ├── uncertainty_cdf.png
        ├── combined_aggregation.{csv,md}   (or combined_regression on the regression side)
        └── llm/{basic,control,customized}.{csv,md}

movie_reviews carries two framings, so its dataset dir is movie_reviews/categorical
(and movie_reviews/regression for the continuous track).
"""
import pathlib

RES = pathlib.Path(__file__).resolve().parents[2] / "results"


def ddir(ds):
    """Dataset directory."""
    d = RES / ds
    return d / "categorical" if ds == "movie_reviews" else d


def mdir(ds, model, base=None):
    """Per-model directory inside a dataset, created on demand."""
    d = (base or ddir(ds)) / "model_analysis" / model
    d.mkdir(parents=True, exist_ok=True)
    return d

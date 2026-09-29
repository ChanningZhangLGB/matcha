# movie_reviews - regression aggregation vs ground truth

Second framing of the same dataset: the continuous ratings are aggregated directly,
with no binning. Not comparable to `crowd_aggregation.md`, which scores the 3-class recast.

| | |
|---|---|
| Instances | **1,498** reviews |
| Annotators | 135 |
| Judgments | 7,430 (4.96 per review) |
| Target | continuous rating, [0,1] |
| Ground truth | the review author's own rating |

## Aggregators

| Method | MAE | RMSE | R2 | r | note |
|---|--:|--:|--:|--:|---|
| Mean | 0.0607 | 0.0755 | 0.8299 | 0.9283 | paper's DL (Mean) target |
| EMBias | 0.0492 | 0.0587 | 0.8969 | 0.9672 | ours; paper's 'B' annotator model, fit by EM |
| shipped_DS | 0.0436 | 0.0535 | 0.9143 | 0.9736 | reference only; not a method in the paper |

**Mean** reproduces the shipped `ratings_train_mean.txt` to 1.1e-16 and is the only
aggregation Rodrigues & Pereira (AAAI-18) used for this dataset (Table 2, `DL (Mean)`).

**EMBias** is ours, not theirs: it adopts the paper's best crowd-layer variant `"B"`
(`f_r(mu) = mu + b_r`) but fits it by EM on the answer matrix alone, where they trained it
end-to-end inside a CNN. Learned annotator biases have sd 0.114, range [-0.287, +0.433].

**shipped_DS** is a reference column only - `ratings_train_DS.txt` corresponds to no method
in the paper (Table 2 has no Dawid & Skene row; DS appears only for classification).

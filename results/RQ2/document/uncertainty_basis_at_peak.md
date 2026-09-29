# Which uncertainty basis does MATCHA peak on?

Source: `results/RQ2/document/uncertainty_basis_at_peak.csv`, regenerated from
`results/<dataset>/allocation/<model>/<measure>/<route>/routing.csv` after the
GLAD/MACE backfill completed (all 8 aggregators present on every dataset).

For each (dataset, model) the table records the peak accuracy reached under each of the
three uncertainty bases — each already maximised over aggregator x budget x route — and
which basis produced the overall peak. `random` is the control and is excluded.

## Headline

- **Vote dispersion wins 18 of 24 cells; stated confidence wins 6.**
- **Entropy and inter-rater agreement are numerically identical in 19 of 24 cells.**
  Where they tie, the reported winner is `entropy` only because the code iterates the
  measures in that order and keeps the first maximum. The defensible claim is that the
  *vote-dispersion family* wins, **not** that entropy specifically beats inter-rater.
  The `entropy_eq_inter_rater` column flags every such cell.

## The three datasets asked about

| Dataset | Model | Peak | Basis | Aggregator | Route | X | conf | entropy | inter-rater |
|---|---|--:|---|---|---|--:|--:|--:|--:|
| QUIZ | GPT-4o-mini | 0.8774 | entropy | OneCoinDawidSkene | h-human_llm | 10 | 0.8581 | 0.8774 | 0.8710 |
| QUIZ | Llama3.1-8B | 0.8000 | entropy* | MACE | h-human | 55 | 0.7290 | 0.8000 | 0.8000 |
| QUIZ | Qwen2.5-7B | 0.8129 | entropy* | MMSR | h-human_llm | 45 | 0.7613 | 0.8129 | 0.8129 |
| Sentiment Polarity | GPT-4o-mini | 0.9370 | entropy* | OneCoinDawidSkene | h-human_llm | 55 | 0.9270 | 0.9370 | 0.9370 |
| Sentiment Polarity | Llama3.1-8B | 0.9302 | entropy* | OneCoinDawidSkene | h-human_llm | 65 | 0.9276 | 0.9302 | 0.9302 |
| Sentiment Polarity | Qwen2.5-7B | 0.9296 | entropy* | MACE | h-human_llm | 20 | 0.9266 | 0.9296 | 0.9296 |
| LabelMe | GPT-4o-mini | 0.8320 | entropy* | MMSR | h-human | 35 | 0.8300 | 0.8320 | 0.8320 |
| LabelMe | MiniCPM-V-8B | **0.8200** | **confidence** | DawidSkene | h-human | 70 | 0.8200 | 0.8170 | 0.8170 |
| LabelMe | Qwen2.5VL-7B | 0.8280 | entropy* | DawidSkene | h-human | 70 | 0.8170 | 0.8280 | 0.8280 |

`*` entropy and inter-rater tie exactly; the label is arbitrary between the two.

## Caveats to carry

1. **The margin over confidence is not uniform.** On QUIZ it is decisive (Llama +0.0710,
   Qwen +0.0516, GPT +0.0193). On Sentiment Polarity it is ~0.003, roughly 15 instances
   out of 4,999 — a marginal claim, not a strong one.
2. **Entropy and inter-rater are the same ranking on 3 of 8 datasets** (Sentiment
   Polarity, CrowdTruth RelEx, PICO), verified instance by instance. On the other five
   they differ, so they are not interchangeable in general — only on those three.
3. **Route splits by modality here.** All six text cells in the table above peak on
   `h-human_llm` (LLM retained in the annotator pool); all three LabelMe cells peak on
   `h-human` (LLM label discarded on routed instances).
4. Peaks are maxima over aggregator x budget x route, taken on the scoring gold, so they
   are upper bounds rather than what a fixed configuration would deliver.

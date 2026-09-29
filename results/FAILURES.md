# Failure cases: causes and resolution

All generation failures shared one symptom — `finish_reason = "length"`, an unparseable
truncated JSON — but had **three distinct causes** requiring different fixes.

## 1. Under-budgeted `max_tokens` (the large majority)

Budgets were first sized from the *input* length rather than from the JSON the model has to
emit. `conll_ner` writes **two parallel arrays** over up to 60 tokens (tags + per-token
confidence): ~60x7 + 60x3 tokens for `vanilla`, and three times the tag cost for `topk`.
The original 500 / 800 / 1800 was far too small.

This failure is **not random** — it hits the longest sentences, i.e. the ones with the most
entities, so silently dropping the failures would bias the surviving sample toward short,
easy inputs.

| | original | corrected |
|---|--:|--:|
| conll_ner vanilla / cot / topk | 500 / 800 / 1800 | **1400 / 1800 / 4000** |
| movie_reviews cot | 500 | **700** |
| pico topk | 1500 | **2500** |

*Resolution:* raise the budget, strip the failed records, regenerate.

## 2. Degenerate repetition loops (budget-proof)

A minority are not truncation at all. The model enters a repetition loop and burns the whole
budget regardless of its size:

| id | sentence tokens | tokens emitted | budget |
|---|--:|--:|--:|
| `s4020` | 30 | 1,400 | 1,400 |
| `s4020` (cot) | 30 | 1,800 | 1,800 |
| `s5113` | 26 | 4,000 | 4,000 |

A 30-token sentence needs ~300 tokens; emitting 1,800 of `"O", "O", "O", ...` is degeneracy.
Raising the ceiling only buys a longer loop. This is why `control` still failed **after** the
corrected budgets were already in force.

*Resolution:* retry (see below); accept whatever persists as a genuine model failure.

## 3. Tag/token length mismatch (a scoring-time drop, not a generation failure)

Separately, sentence-level `conll_ner` prompts return a tag array whose length does not match
the token count — the model silently re-tokenises. These records parse fine but cannot be
aligned, and are **rejected rather than padded**, since padding would misalign every
subsequent tag and corrupt the labels. This capped basic-group CoNLL coverage at 19-39%.

*Resolution:* the `customized` per-token multiple-choice prompt sidesteps it entirely — ids
are already `s<sent>_t<tok>`, so there is nothing to align. Coverage rose to **94-100%** while
macro-F1 barely moved (0.5872 -> 0.5896), which retrospectively shows the dropped sentences
were not systematically harder.

## Retrying works on the API, not locally

`control/conll_ner_topk` went **6 failures -> 0** on a re-run with an *unchanged* 4000 budget
and identical settings. That is only possible because **OpenAI's `seed` is best-effort, not a
determinism guarantee**. The local models honour the seed strictly, so the same retry strategy
will *not* rescue llama/qwen failures — those need budget increases or acceptance.

## Outcome (gpt-4o-mini, all three groups)

| Round | Failures |
|---|--:|
| initial | 34 |
| after budget fix + retry 1 | 17 |
| retry 2 | 11 |
| retries 3-6 | **1** |

**1 failure in 100,295 records (0.001%).** The survivor is `s4020` in
`basic/conll_ner_cot` — a stable degenerate loop that resisted five independent retries. It is
reported as a genuine model failure rather than retried further; changing its seed would buy
0.001% at the cost of the `seed=42` claim.

## Tooling

`eval/llm/patch_failures.py` — strips failed records (they would otherwise be skipped forever
by resume-by-id), then regenerates exactly those ids under current budgets.

```bash
python eval/llm/patch_failures.py --model gpt-4o-mini              # report
python eval/llm/patch_failures.py --model gpt-4o-mini --strip --rerun
```

`--model` scopes the run so files being written by other in-flight jobs are never touched.
It scans **all three prompt groups**; an earlier version scanned only `basic_instruction` and
would have silently missed every `control` failure.

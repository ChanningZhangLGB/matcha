# LLM annotation prompts — 5 datasets × 3 protocols

Models: `gpt-4o-mini` (API), `llama3.1:8b-instruct-q8_0`, `qwen2.5:7b-instruct-q8_0` (ollama).
**Set `temperature` explicitly on all three** — defaults differ (OpenAI 1.0, ollama 0.8).

Protocols, all producing answer + confidence:

| | |
|---|---|
| **Vanilla** | Read the question, provide your answer, and your confidence in this answer. |
| **CoT** | Read the question, analyze step by step, provide your answer and your confidence. |
| **Top-K** | Provide your K best guesses and the probability that each is correct (0%–100%). |

## Common output contract

One schema across every dataset, so a single parser works:

```json
Vanilla : {"answer": <A>, "confidence": <int 0-100>}
CoT     : {"reasoning": "<brief>", "answer": <A>, "confidence": <int 0-100>}
Top-K   : {"guesses": [{"answer": <A>, "probability": <int 0-100>}, ...]}
```

Every prompt ends with: `Respond with ONLY a JSON object, no other text.`
Parser must be **case-insensitive** and strip whitespace — at temp 1.0 we already observed
`'Medium'` vs `'medium'` drift on Llama.

**Alignment key:** 🟢 worker instructions disclosed verbatim · 🟡 partially disclosed ·
🔴 reconstructed from task attributes.

---

# 1. crowdtruth 🟢 (full CML template)

Wording taken from `templates/RelEx/RelEx.cml`. The template told workers to *"HOVER MOUSE over each
relation name to see the DEFINITION and an EXAMPLE"* — an LLM cannot hover, so **all 14 definitions
are inlined verbatim**; otherwise the model gets less information than the workers had.
Use the **value** spelling `[DIAGNOSE_BY_TEST_OR_DRUG]` (no "D"), which is what the data stores.
STEP 2a/2b are dropped — only STEP 1 is scored. This is a deviation: workers had to justify.

**Shared block `{RELATIONS}`:**
```
[TREATS] — Therapeutic use of an ingredient or a drug, e.g. penicillin cures infection.
[PREVENTS] — Preventative use of an ingredient or a drug, e.g. vitamin C reduces the risk of influenza.
[DIAGNOSE_BY_TEST_OR_DRUG] — Diagnostic use of an ingredient, test or a drug, e.g. RINNE test is used for determining hearing loss.
[CAUSES] — The underlying reason for a symptom or a disease, e.g. fever induces dizziness.
[LOCATION] — Body part or anatomical structure in which disease or disorder is observed, e.g. leukimia is found in the circulatory system.
[SYMPTOM] — Deviation from normal function indicating the presence of disease or abnormality, e.g. pain is a symptom of a broken arm.
[MANIFESTATION] — Links disorders to the observations that are closely associated with them, e.g. abdominal distension is a manifestation of liver failure.
[CONTRAINDICATES] — A condition that indicates that drug or treatment SHOULD NOT BE USED, e.g. patients with obesity should avoid using danazol.
[ASSOCIATED_WITH] — Signs, symptoms or findings that often appear together, e.g. patients who smoke often have yellow teeth.
[SIDE_EFFECT] — A secondary condition or symptom that results from a drug or treatment, e.g. use of antidepressants causes dryness in the eyes.
[IS_A] — A relation that indicates that one of the terms is more specific variation of the other, e.g. migraine is a kind of headache.
[PART_OF] — An anatomical or structural sub-component, e.g. the left ventrical is part of the heart.
[OTHER] — The words are related, but not by any of the above relations.
[NONE] — There is no relation between those words in this sentence.
```

### Vanilla
```
In this sentence: {sentence}

Is  {term1}  ----related-to----  {term2}?

STEP 1: Select the valid RELATION(s).
It is important that you understand what the different relation types mean.
The definitions and examples are:
{RELATIONS}

You may select more than one relation. Select [NONE] only if no relation holds.
Provide your answer and your confidence in this answer.

Respond with ONLY a JSON object:
{"answer": ["[RELATION]", ...], "confidence": <0-100>}
```

### CoT
```
... (identical through the definitions block) ...

Analyze the sentence step by step: first identify what is stated about {term1} and {term2},
then decide which relation(s) that statement expresses. Then give your answer and confidence.

Respond with ONLY a JSON object:
{"reasoning": "<2-3 sentences>", "answer": ["[RELATION]", ...], "confidence": <0-100>}
```

### Top-K (K=3)
```
... (identical through the definitions block) ...

Provide your 3 best guesses for the correct set of relation(s), and the probability that each
guess is correct (0% to 100%). Each guess is a complete selection, which may contain more
than one relation. Order from most to least likely.

Respond with ONLY a JSON object:
{"guesses": [{"answer": ["[RELATION]", ...], "probability": <0-100>}, ...]}
```

---

# 2. movie_reviews 🟡 (HIT title/description disclosed, widget not)

Verbatim from `Batch_results_AMT.csv`: Title *"Rate movies based on their review"*, Description
*"Given a short review text, predict the number of stars (from 0 to 10) that the movie got from
that reviewer."*

**Ask for stars 0–10, exactly as workers were asked — do NOT ask for poor/medium/good.** Then
normalize `/10` and apply `bin_rating()`, the identical recast applied to the human answers. Asking
the model directly for the 3-way class would give it an easier task than the humans had.

### Vanilla
```
Rate movies based on their review.

Given a short review text, predict the number of stars (from 0 to 10) that the movie got from
that reviewer. Judge what rating the reviewer gave, not your own opinion of the movie.

Review: {text}

Provide your answer and your confidence in this answer.
Respond with ONLY a JSON object:
{"answer": <integer 0-10>, "confidence": <0-100>}
```

### CoT
```
... (identical framing) ...

Analyze the review step by step: identify the positive and negative statements the reviewer makes
and how strongly they are worded, then infer the star rating they gave. Then give your answer
and confidence.

Respond with ONLY a JSON object:
{"reasoning": "<2-3 sentences>", "answer": <integer 0-10>, "confidence": <0-100>}
```

### Top-K (K=3)
```
... (identical framing) ...

Provide your 3 best guesses for the star rating, and the probability that each is correct
(0% to 100%). Order from most to least likely.

Respond with ONLY a JSON object:
{"guesses": [{"answer": <integer 0-10>, "probability": <0-100>}, ...]}
```

---

# 3. sentiment 🔴 (nothing disclosed — reconstructed)

No HIT metadata, no template, no README. Reconstructed from the answer space
(`Answer.sent ∈ {pos, neg}`) and Rodrigues (2013). Forced binary — **no neutral option**, which is
the one structural fact the data does establish.

### Vanilla
```
Read the sentence below, taken from a movie review, and decide whether the sentiment it
expresses is positive or negative. You must choose one; there is no neutral option.

Sentence: {sentence}

Provide your answer and your confidence in this answer.
Respond with ONLY a JSON object:
{"answer": "pos" | "neg", "confidence": <0-100>}
```

### CoT
```
... (identical framing) ...

Analyze the sentence step by step: identify the sentiment-bearing words and any negation or
contrast, then decide the overall polarity. Then give your answer and confidence.

Respond with ONLY a JSON object:
{"reasoning": "<1-2 sentences>", "answer": "pos" | "neg", "confidence": <0-100>}
```

### Top-K (K=2)
```
... (identical framing) ...

Provide your 2 best guesses and the probability that each is correct (0% to 100%).

Respond with ONLY a JSON object:
{"guesses": [{"answer": "pos"|"neg", "probability": <0-100>}, ...]}
```
⚠️ K=2 exhausts a binary label space, so Top-K here degenerates into a probability distribution
rather than a ranked shortlist. Report it as such; it is not comparable to Top-K on the other sets.

---

# 4. conll_ner 🔴 (nothing disclosed — reconstructed)

Paper only paraphrases: *"identify the named entities in the sentence and classify them as persons,
locations, organizations or miscellaneous."* Prompt at **sentence level** (the worker's unit), emit
one tag per token, then score per token — the same recast applied to the human columns.

### Vanilla
```
Identify the named entities in the sentence below and classify each as a person (PER),
location (LOC), organization (ORG), or miscellaneous (MISC). Miscellaneous covers named
entities that are not persons, locations, or organizations, such as nationalities and events.

Label every token using BIO tags: B-PER, I-PER, B-LOC, I-LOC, B-ORG, I-ORG, B-MISC, I-MISC,
or O for tokens that are not part of any named entity.

Tokens: {json_list_of_tokens}

Return one tag per token, in the same order, and your confidence for each tag.
Respond with ONLY a JSON object:
{"answer": ["<tag>", ...], "confidence": [<0-100>, ...]}
```

### CoT
```
... (identical framing) ...

First identify the entity spans in the sentence and their types, then convert them to per-token
BIO tags. Then give your tags and per-tag confidence.

Respond with ONLY a JSON object:
{"reasoning": "<brief>", "answer": ["<tag>", ...], "confidence": [<0-100>, ...]}
```

### Top-K (K=3)
```
... (identical framing) ...

For EACH token, provide your 3 best guesses for its tag and the probability that each is
correct (0% to 100%).

Respond with ONLY a JSON object:
{"guesses": [[{"answer": "<tag>", "probability": <0-100>}, ...], ...]}
```
⚠️ Output length is `n_tokens × K`. Expect strain on the 8B models and mis-aligned array lengths.
**Reject any response whose array length ≠ token count** rather than silently padding.

---

# 5. pico 🔴 (nothing disclosed — reconstructed)

README documents the dataset, not the task. Reconstructed from Nguyen et al. (ACL 2017): workers
highlight the spans describing the trial **Participants**. Prompt at abstract level, return spans,
then tokenize with the same code path used for the human spans.

### Vanilla
```
Below is the abstract of a medical clinical-trial article. Highlight the text spans that
describe the PARTICIPANTS of the trial — that is, the population who took part: their number,
condition, age, sex, or other characteristics that identify who was studied.

Copy the spans exactly as they appear in the text. Do not paraphrase. If no span describes the
participants, return an empty list.

Abstract: {text}

Provide your answer and your confidence in this answer.
Respond with ONLY a JSON object:
{"answer": ["<exact span>", ...], "confidence": <0-100>}
```

### CoT
```
... (identical framing) ...

Analyze the abstract step by step: locate where the study population is described, then extract
the exact spans. Then give your answer and confidence.

Respond with ONLY a JSON object:
{"reasoning": "<2-3 sentences>", "answer": ["<exact span>", ...], "confidence": <0-100>}
```

### Top-K (K=3)
```
... (identical framing) ...

Provide your 3 best guesses for the complete set of participant spans, and the probability that
each guess is correct (0% to 100%). Order from most to least likely.

Respond with ONLY a JSON object:
{"guesses": [{"answer": ["<exact span>", ...], "probability": <0-100>}, ...]}
```
⚠️ Spans must be matched back to character offsets by exact string search. Log any span that does
not occur verbatim in the abstract as a parse failure — do not fuzzy-match.

---

# Open decisions

1. **How many LLM annotators?** One call at temp 0 = one annotator, and the 8 aggregators need
   ≥2. Either run N calls at temp > 0 (temperature becomes an experimental variable), or treat the
   3 models × 3 protocols as 9 distinct "annotators".
2. **What is confidence for?** It is not consumed by any of the 8 crowd-kit aggregators, which take
   only hard labels. It is either (a) reported separately as calibration, or (b) fed to a
   confidence-weighted aggregator outside the 8. Decide before running.
3. **Top-K → hard label.** Taking argmax makes Top-K collapse toward Vanilla. If Top-K is meant to
   be distinct, its distribution must be used, not just its top entry.
4. **Cost.** conll_ner_5k is 392 sentences and pico is 191 abstracts — cheap. sentiment is 4,999
   calls per model per protocol; 3 models × 3 protocols = ~45k calls on that set alone.

#!/usr/bin/env python3
"""Emit the 24 prompt templates: prompt/<strategy>/<dataset>.txt

Strategies: vanilla, cot, topk.  Datasets: crowdtruth, movie_reviews, sentiment,
conll_ner, pico, quiz, imagenet16h, labelme.  Each file is a complete, standalone template with {placeholders}
to be .format()-ed at call time.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "basic_instruction"
STRATEGIES = ["vanilla", "cot", "topk"]

JSON_ONLY = "Respond with ONLY a JSON object, no other text."

# --------------------------------------------------------------- crowdtruth
RELATIONS = """[TREATS] - Therapeutic use of an ingredient or a drug, e.g. penicillin cures infection.
[PREVENTS] - Preventative use of an ingredient or a drug, e.g. vitamin C reduces the risk of influenza.
[DIAGNOSE_BY_TEST_OR_DRUG] - Diagnostic use of an ingredient, test or a drug, e.g. RINNE test is used for determining hearing loss.
[CAUSES] - The underlying reason for a symptom or a disease, e.g. fever induces dizziness.
[LOCATION] - Body part or anatomical structure in which disease or disorder is observed, e.g. leukimia is found in the circulatory system.
[SYMPTOM] - Deviation from normal function indicating the presence of disease or abnormality, e.g. pain is a symptom of a broken arm.
[MANIFESTATION] - Links disorders to the observations that are closely associated with them, e.g. abdominal distension is a manifestation of liver failure.
[CONTRAINDICATES] - A condition that indicates that drug or treatment SHOULD NOT BE USED, e.g. patients with obesity should avoid using danazol.
[ASSOCIATED_WITH] - Signs, symptoms or findings that often appear together, e.g. patients who smoke often have yellow teeth.
[SIDE_EFFECT] - A secondary condition or symptom that results from a drug or treatment, e.g. use of antidepressants causes dryness in the eyes.
[IS_A] - A relation that indicates that one of the terms is more specific variation of the other, e.g. migraine is a kind of headache.
[PART_OF] - An anatomical or structural sub-component, e.g. the left ventrical is part of the heart.
[OTHER] - The words are related, but not by any of the above relations.
[NONE] - There is no relation between those words in this sentence."""

CT_HEAD = f"""In this sentence: {{sentence}}

Is  {{term1}}  ----related-to----  {{term2}}?

STEP 1: Select the valid RELATION(s).
It is important that you understand what the different relation types mean.
The definitions and examples are:
{RELATIONS}

You may select more than one relation. Select [NONE] only if no relation holds."""

# ------------------------------------------------------------ movie_reviews
MR_HEAD = """Rate movies based on their review.

Given a short review text, predict the number of stars (from 0 to 10) that the movie got from
that reviewer. Judge what rating the reviewer gave, not your own opinion of the movie.

Review: {text}"""

# ---------------------------------------------------------------- sentiment
SENT_HEAD = """Read the sentence below, taken from a movie review, and decide whether the sentiment it
expresses is positive or negative. You must choose one; there is no neutral option.

Sentence: {sentence}"""

# ---------------------------------------------------------------- conll_ner
NER_HEAD = """Identify the named entities in the sentence below and classify each as a person (PER),
location (LOC), organization (ORG), or miscellaneous (MISC). Miscellaneous covers named
entities that are not persons, locations, or organizations, such as nationalities and events.

Label every token using BIO tags: B-PER, I-PER, B-LOC, I-LOC, B-ORG, I-ORG, B-MISC, I-MISC,
or O for tokens that are not part of any named entity.

Tokens: {tokens}"""

# --------------------------------------------------------------------- pico
PICO_HEAD = """Below is the abstract of a medical clinical-trial article. Highlight the text spans that
describe the PARTICIPANTS of the trial - that is, the population who took part: their number,
condition, age, sex, or other characteristics that identify who was studied.

Copy the spans exactly as they appear in the text. Do not paraphrase. If no span describes the
participants, return an empty list.

Abstract: {text}"""

# --------------------------------------------------------------------- quiz
# The option list is rendered per item rather than fixed in the template: subsets carry
# 4, 5, or 6 options, so {options} supplies the labelled lines and {letters} the valid
# letter set for that specific question. Four of the six subsets are Japanese and one is
# Chinese-to-Japanese, hence the explicit language note -- without it a model is liable to
# translate first and answer the translation.
QUIZ_HEAD = """Answer the multiple-choice question below by choosing exactly one option.

The question comes from a crowdsourced quiz. It may be written in English, Japanese, or
Chinese; answer it as written rather than translating it first.

Question: {question}

Options:
{options}

Reply with the LETTER of the option you choose, one of: {letters}."""


# ============================================================ IMAGE DATASETS
# These carry NO {placeholder}: the stimulus is an image passed out-of-band in the request
# payload, not interpolated into the prompt text.

# ------------------------------------------------------------------ imagenet16h
# Modelled on the ORIGINAL crowdsourcing interface shipped with the corpus
# (Wiki images/noisy_image_classification_task.png). Faithful to it in four respects:
#   * the same 16 categories, in the same ALPHABETICAL order as the 4x4 icon grid
#   * FORCED choice -- the interface offers no "none of the above" and no skip
#   * the stimulus is described as noise-degraded, which the workers plainly saw
#   * one image per task, judged in isolation
# DEVIATION, deliberate: the interface collected confidence as a 3-point ordinal
# (Low/Medium/High). We ask for 0-100 instead, because every other dataset in this project
# does and because score_llm.confidence() / uncertainty._conf_scalar() consume a number.
# Human confidence is not used anywhere in our pipeline (the crowd table is strictly
# task/worker/label), so nothing is lost; if a direct human-vs-LLM confidence comparison is
# ever wanted, it lives in datasets_pass/imagenet16h/behavioral/.
IN16H_CATS = ["airplane", "bear", "bicycle", "bird", "boat", "bottle", "car", "cat",
              "chair", "clock", "dog", "elephant", "keyboard", "knife", "oven", "truck"]

IN16H_HEAD = f"""Look at the image and decide which object it shows.

The photograph is in greyscale and has been degraded with visual noise, so it may be hard
to make out. Judge it as best you can.

Choose exactly one of these {len(IN16H_CATS)} categories:
{", ".join(IN16H_CATS)}

You must pick one; there is no "none of the above" option."""

# ---------------------------------------------------------------------- labelme
# The LabelMe crowd release (Rodrigues & Pereira, AAAI-18) ships DATA ONLY -- no HIT
# template, no worker instructions. This is therefore a clean draft, written to the same
# standard as a crowdsourcing query: state the task plainly, enumerate the exact answer set,
# force a single choice, and use neutral wording.
# Categories are listed ALPHABETICALLY, matching the neutral presentation order the
# imagenet16h interface used, so neither prompt encodes a hint about which answer is likely.
# NOTE, deliberately minimal: the eight class names are given WITHOUT definitions or
# disambiguation, even though several are confusable (opencountry vs coast, insidecity vs
# street vs tallbuilding). The AMT workers labelled from the bare class names; supplying the
# model with written definitions they never had would hand it an advantage and make any
# "LLM beats crowd" result an artefact of the prompt rather than of the annotator.
LM_CATS = ["coast", "forest", "highway", "insidecity", "mountain", "opencountry",
           "street", "tallbuilding"]

LM_HEAD = f"""Look at the image and decide which kind of scene it shows.

Choose exactly one of these {len(LM_CATS)} categories:
{", ".join(LM_CATS)}

You must pick one; there is no "none of the above" option."""


def block(head, task, schema):
    return f"{head}\n\n{task}\n\n{JSON_ONLY}\n{schema}\n"


PROMPTS = {
    "crowdtruth": {
        "vanilla": block(
            CT_HEAD,
            "Provide your answer and your confidence in this answer.",
            '{{"answer": ["[RELATION]", ...], "confidence": <integer 0-100>}}'),
        "cot": block(
            CT_HEAD,
            "Analyze the sentence step by step: first identify what is stated about the two terms,\n"
            "then decide which relation(s) that statement expresses. Then provide your answer and\n"
            "your confidence in this answer.",
            '{{"reasoning": "<2-3 sentences>", "answer": ["[RELATION]", ...], "confidence": <integer 0-100>}}'),
        "topk": block(
            CT_HEAD,
            "Provide your 3 best guesses for the correct set of relation(s), and the probability that\n"
            "each guess is correct (0% to 100%). Each guess is a complete selection, which may contain\n"
            "more than one relation. Order from most to least likely.",
            '{{"guesses": [{{"answer": ["[RELATION]", ...], "probability": <integer 0-100>}}, ...]}}'),
    },
    "movie_reviews": {
        "vanilla": block(
            MR_HEAD,
            "Provide your answer and your confidence in this answer.",
            '{{"answer": <integer 0-10>, "confidence": <integer 0-100>}}'),
        "cot": block(
            MR_HEAD,
            "Analyze the review step by step: identify the positive and negative statements the reviewer\n"
            "makes and how strongly they are worded, then infer the star rating they gave. Then provide\n"
            "your answer and your confidence in this answer.",
            '{{"reasoning": "<2-3 sentences>", "answer": <integer 0-10>, "confidence": <integer 0-100>}}'),
        "topk": block(
            MR_HEAD,
            "Provide your 3 best guesses for the star rating, and the probability that each is correct\n"
            "(0% to 100%). Order from most to least likely.",
            '{{"guesses": [{{"answer": <integer 0-10>, "probability": <integer 0-100>}}, ...]}}'),
    },
    "sentiment": {
        "vanilla": block(
            SENT_HEAD,
            "Provide your answer and your confidence in this answer.",
            '{{"answer": "pos" or "neg", "confidence": <integer 0-100>}}'),
        "cot": block(
            SENT_HEAD,
            "Analyze the sentence step by step: identify the sentiment-bearing words and any negation or\n"
            "contrast, then decide the overall polarity. Then provide your answer and your confidence in\n"
            "this answer.",
            '{{"reasoning": "<1-2 sentences>", "answer": "pos" or "neg", "confidence": <integer 0-100>}}'),
        "topk": block(
            SENT_HEAD,
            "Provide your 2 best guesses and the probability that each is correct (0% to 100%).",
            '{{"guesses": [{{"answer": "pos" or "neg", "probability": <integer 0-100>}}, ...]}}'),
    },
    "conll_ner": {
        "vanilla": block(
            NER_HEAD,
            "Return one tag per token, in the same order and the same number as the tokens above,\n"
            "and your confidence for each tag.",
            '{{"answer": ["<tag>", ...], "confidence": [<integer 0-100>, ...]}}'),
        "cot": block(
            NER_HEAD,
            "First identify the entity spans in the sentence and their types, then convert them to\n"
            "per-token BIO tags. Return one tag per token, in the same order and the same number as the\n"
            "tokens above, and your confidence for each tag.",
            '{{"reasoning": "<brief>", "answer": ["<tag>", ...], "confidence": [<integer 0-100>, ...]}}'),
        "topk": block(
            NER_HEAD,
            "For EACH token, provide your 3 best guesses for its tag and the probability that each is\n"
            "correct (0% to 100%). Return one list of guesses per token, in the same order and the same\n"
            "number as the tokens above.",
            '{{"guesses": [[{{"answer": "<tag>", "probability": <integer 0-100>}}, ...], ...]}}'),
    },
    "pico": {
        "vanilla": block(
            PICO_HEAD,
            "Provide your answer and your confidence in this answer.",
            '{{"answer": ["<exact span>", ...], "confidence": <integer 0-100>}}'),
        "cot": block(
            PICO_HEAD,
            "Analyze the abstract step by step: locate where the study population is described, then\n"
            "extract the exact spans. Then provide your answer and your confidence in this answer.",
            '{{"reasoning": "<2-3 sentences>", "answer": ["<exact span>", ...], "confidence": <integer 0-100>}}'),
        "topk": block(
            PICO_HEAD,
            "Provide your 3 best guesses for the complete set of participant spans, and the probability\n"
            "that each guess is correct (0% to 100%). Order from most to least likely.",
            '{{"guesses": [{{"answer": ["<exact span>", ...], "probability": <integer 0-100>}}, ...]}}'),
    },
    "quiz": {
        "vanilla": block(
            QUIZ_HEAD,
            "Provide your answer and your confidence in this answer.",
            '{{"answer": "<letter>", "confidence": <integer 0-100>}}'),
        "cot": block(
            QUIZ_HEAD,
            "Analyze the question step by step: establish what is being asked, rule out the options\n"
            "that cannot be correct, then choose the best of those remaining. Then provide your\n"
            "answer and your confidence in this answer.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<letter>", "confidence": <integer 0-100>}}'),
        "topk": block(
            QUIZ_HEAD,
            "Provide your 3 best guesses and the probability that each is correct (0% to 100%).\n"
            "Order from most to least likely.",
            '{{"guesses": [{{"answer": "<letter>", "probability": <integer 0-100>}}, ...]}}'),
    },
    "imagenet16h": {
        "vanilla": block(
            IN16H_HEAD,
            "Provide your answer and your confidence in this answer.",
            '{{"answer": "<category>", "confidence": <integer 0-100>}}'),
        "cot": block(
            IN16H_HEAD,
            "Analyze the image step by step: describe the shapes and textures you can make out\n"
            "through the noise, then decide which category best fits them. Then provide your\n"
            "answer and your confidence in this answer.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<category>", "confidence": <integer 0-100>}}'),
        "topk": block(
            IN16H_HEAD,
            "Provide your 3 best guesses and the probability that each is correct (0% to 100%).\n"
            "Order from most to least likely.",
            '{{"guesses": [{{"answer": "<category>", "probability": <integer 0-100>}}, ...]}}'),
    },
    "labelme": {
        "vanilla": block(
            LM_HEAD,
            "Provide your answer and your confidence in this answer.",
            '{{"answer": "<category>", "confidence": <integer 0-100>}}'),
        "cot": block(
            LM_HEAD,
            "Analyze the image step by step: note the main elements you can see and how the scene\n"
            "is laid out, then decide which category best fits it. Then provide your answer and\n"
            "your confidence in this answer.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<category>", "confidence": <integer 0-100>}}'),
        "topk": block(
            LM_HEAD,
            "Provide your 3 best guesses and the probability that each is correct (0% to 100%).\n"
            "Order from most to least likely.",
            '{{"guesses": [{{"answer": "<category>", "probability": <integer 0-100>}}, ...]}}'),
    },
}

if __name__ == "__main__":
    n = 0
    for strat in STRATEGIES:
        (OUT / strat).mkdir(parents=True, exist_ok=True)
        for ds, byst in PROMPTS.items():
            p = OUT / strat / f"{ds}.txt"
            p.write_text(byst[strat])
            n += 1
            print(f"  {p.relative_to(OUT)}  ({len(byst[strat])} chars)")
    print(f"\nwrote {n} prompt templates to {OUT}")

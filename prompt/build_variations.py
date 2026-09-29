#!/usr/bin/env python3
"""Emit prompt variations: prompt/<group>/<strategy>/<dataset>.txt

Two groups:

  control/     PARAPHRASE - the instruction is reworded, everything else held fixed:
               same label vocabulary, same option ORDER, same output schema, same
               placeholders. This is the baseline that makes the customized group
               interpretable; without it you cannot tell "this model is prompt-sensitive
               in general" from "this manipulation moved it".

  customized/  the task-fitted manipulation, one per dataset:
               crowdtruth    Sequence Swapping  (14 relations listed in reverse order)
               sentiment     True/False         (binary -> verification)
               movie_reviews Sequence Swapping  (11 options listed 10 -> 0)
               conll_ner     Multiple Choice    (per-token, 9 lettered options)
               pico          Question Answering ("who were the participants?")
               quiz          Question with Confirmation Bias (planted suggestion, seed 42)
               imagenet16h   Multiple Choice    (16 lettered options, alphabetical)
               labelme       Multiple Choice    (8 lettered options, alphabetical)

NOTE the customized group changes placeholders / answer spaces for three datasets --
see PLACEHOLDERS at the bottom of this file and VARIATIONS.md.
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
STRATEGIES = ["vanilla", "cot", "topk"]
JSON_ONLY = "Respond with ONLY a JSON object, no other text."

# Category lists are imported, not re-declared: the control group must present the SAME
# options in the SAME order as basic_instruction, and a second copy would eventually drift.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_prompts import IN16H_CATS, LM_CATS       # noqa: E402

REL = [
    ("[TREATS]", "Therapeutic use of an ingredient or a drug, e.g. penicillin cures infection."),
    ("[PREVENTS]", "Preventative use of an ingredient or a drug, e.g. vitamin C reduces the risk of influenza."),
    ("[DIAGNOSE_BY_TEST_OR_DRUG]", "Diagnostic use of an ingredient, test or a drug, e.g. RINNE test is used for determining hearing loss."),
    ("[CAUSES]", "The underlying reason for a symptom or a disease, e.g. fever induces dizziness."),
    ("[LOCATION]", "Body part or anatomical structure in which disease or disorder is observed, e.g. leukimia is found in the circulatory system."),
    ("[SYMPTOM]", "Deviation from normal function indicating the presence of disease or abnormality, e.g. pain is a symptom of a broken arm."),
    ("[MANIFESTATION]", "Links disorders to the observations that are closely associated with them, e.g. abdominal distension is a manifestation of liver failure."),
    ("[CONTRAINDICATES]", "A condition that indicates that drug or treatment SHOULD NOT BE USED, e.g. patients with obesity should avoid using danazol."),
    ("[ASSOCIATED_WITH]", "Signs, symptoms or findings that often appear together, e.g. patients who smoke often have yellow teeth."),
    ("[SIDE_EFFECT]", "A secondary condition or symptom that results from a drug or treatment, e.g. use of antidepressants causes dryness in the eyes."),
    ("[IS_A]", "A relation that indicates that one of the terms is more specific variation of the other, e.g. migraine is a kind of headache."),
    ("[PART_OF]", "An anatomical or structural sub-component, e.g. the left ventrical is part of the heart."),
    ("[OTHER]", "The words are related, but not by any of the above relations."),
    ("[NONE]", "There is no relation between those words in this sentence."),
]
FWD = "\n".join(f"{k} - {v}" for k, v in REL)
REV = "\n".join(f"{k} - {v}" for k, v in reversed(REL))

NER_TAGS = ["O", "B-PER", "I-PER", "B-LOC", "I-LOC", "B-ORG", "I-ORG", "B-MISC", "I-MISC"]
NER_OPTS = "\n".join(f"{chr(65+i)}) {t}" for i, t in enumerate(NER_TAGS))

# ============================================================ CONTROL heads
C_CT = f"""Consider the sentence below.

Sentence: {{sentence}}

Question: what relationship, if any, does this sentence express between {{term1}} and {{term2}}?

Choose every relation type that applies. Make sure you are familiar with what each relation
type means; the list below gives a definition and an example for each:
{FWD}

More than one relation may apply. Choose [NONE] only when none of the others hold."""

C_MR = """Below is a short excerpt from a movie review. Work out how many stars, on a scale from
0 to 10, the reviewer awarded the film. Base this on what the reviewer's own verdict appears
to be, rather than on how you would rate the movie yourself.

Review: {text}"""

C_SENT = """The sentence below comes from a movie review. Judge whether the opinion it conveys is
favourable or unfavourable. One of the two must be chosen - a neutral verdict is not available."""

C_SENT_FULL = C_SENT + "\n\nSentence: {sentence}"

C_NER = f"""The sentence below may mention named entities. Find them and assign each to one of four
categories: people (PER), places (LOC), organizations (ORG), or miscellaneous (MISC), the last
covering named things that fit none of the first three, such as nationalities and events.

Give every token a BIO tag, one of: {", ".join(NER_TAGS[1:])}, or O when the token belongs to
no named entity.

Tokens: {{tokens}}"""

C_PICO = """The text below is an abstract from a clinical-trial paper. Mark the passages that
characterise the trial's PARTICIPANTS - the people enrolled in the study, including how many
there were, what condition they had, their age or sex, or anything else identifying who was
studied.

Reproduce each passage word for word as it appears. Do not reword it. Return an empty list if
the abstract describes no participants.

Abstract: {text}"""

C_QUIZ = """Below is a question offering several possible answers. Exactly one of them is correct;
identify it.

The question is drawn from a crowdsourced quiz and may be in English, Japanese, or Chinese.
Work with it in whichever language it is written; do not translate it first.

Question: {question}

Options:
{options}

State your choice as the LETTER that identifies that option, drawn from: {letters}."""

# ---------------------------------------------------------------- IMAGE datasets
# Type 3 (Paraphrase) applied to the two image sets. The instruction is reworded; the
# CATEGORY LIST AND ITS ORDER ARE UNCHANGED, as is the forced-choice constraint and the
# JSON schema. These heads carry no {placeholder} -- the stimulus is an image sent in the
# request payload, not interpolated text.
C_IN16H = f"""The picture below shows a single object. Identify it.

The photo is greyscale and has had visual noise added to it, which may make it difficult to
read. Do the best you can with it.

Exactly one of the following {len(IN16H_CATS)} categories applies:
{", ".join(IN16H_CATS)}

A choice is required; "none of the above" is not available."""

C_LM = f"""The picture below shows a scene of one particular kind. Work out which kind.

Exactly one of the following {len(LM_CATS)} categories applies:
{", ".join(LM_CATS)}

A choice is required; "none of the above" is not available."""

# ========================================================= CUSTOMIZED heads
X_CT = f"""In this sentence: {{sentence}}

Is  {{term1}}  ----related-to----  {{term2}}?

STEP 1: Select the valid RELATION(s).
It is important that you understand what the different relation types mean.
The definitions and examples are:
{REV}

You may select more than one relation. Select [NONE] only if no relation holds."""

X_SENT = """Read the sentence below, taken from a movie review.

Sentence: {sentence}

Statement: The sentiment expressed in this sentence is {polarity}.

Is this statement true or false? You must answer True or False."""

# SEQUENCE SWAPPING for movie_reviews: the 11 rating options are enumerated exactly
# as in the multiple-choice form, but listed in REVERSE (10 stars first, 0 last).
# Wording is otherwise identical, so a difference against the forward-ordered run
# isolates option ORDER alone -- the same design used for crowdtruth.
MR_OPTS = "\n".join(
    f"{chr(65+i)}) {10-i} star" + ("" if 10-i == 1 else "s") for i in range(11))

X_MR = f"""Rate movies based on their review.

Given a short review text, predict the number of stars that the movie got from that reviewer.
Judge what rating the reviewer gave, not your own opinion of the movie.

Review: {{text}}

Which rating did the reviewer give? Choose exactly one:
{MR_OPTS}"""

X_NER = f"""Sentence: {{sentence}}

In the sentence above, consider the token at position {{index}}: "{{token}}".

Which BIO tag applies to this token? Choose exactly one:
{NER_OPTS}

Tags mark named entities as person (PER), location (LOC), organization (ORG) or
miscellaneous (MISC); B- begins an entity, I- continues one, and O marks a token that
belongs to no named entity."""

# QUESTION WITH CONFIRMATION BIAS - the only type in the taxonomy no other dataset uses.
# A suggested answer is planted before the question, and the model is asked whether it agrees.
#
# {suggestion} is rendered by the loader as "(B) <option text>" and is drawn UNIFORMLY AT
# RANDOM from that item's options with seed 42, INDEPENDENT OF GOLD. Planting the correct
# option (or deliberately planting a wrong one) would consume ground truth at prompt-build
# time -- the same leak that excludes GoldMajorityVote from the aggregator set. Because the
# draw ignores gold, roughly 1/k of items happen to be planted correctly, and results split
# post hoc into planted-right vs planted-wrong without anything leaking into generation.
#
# The answer space stays a LETTER rather than agree/disagree: a bare yes/no yields no label
# to aggregate over 4-6 options, so the model is told to return the planted letter if it
# agrees and the letter it prefers if it does not. Scoring is therefore unchanged.
X_QUIZ = """I think the answer to the following question is {suggestion}. Do you agree?

Question: {question}

Options:
{options}

If you agree, give that same letter as your answer. If you disagree, give the LETTER of the
option you believe is correct instead. Either way, your answer must be one of: {letters}."""

# MULTIPLE CHOICE for the two image sets. The answer space moves from PRODUCING a category
# name to SELECTING a letter, which separates visual discrimination from label naming: a
# model that recognises the scene but is unsure whether we call it `insidecity` or `street`
# behaves differently under the two framings. Same recast movie_reviews got (0-10 -> A-K).
#
# For imagenet16h this is also the closest match to the ORIGINAL instrument: the workers saw
# a 4x4 grid of 16 icons and clicked one, which is a multiple-choice interface.
#
# OPTION ORDER IS ALPHABETICAL, identical to basic_instruction. Only ONE thing changes here
# (name -> letter). Combining a lettered recast with a reordered list is what makes
# movie_reviews' customized prompt uninterpretable -- don't repeat it.
IN16H_OPTS = "\n".join(f"{chr(65+i)}) {c}" for i, c in enumerate(IN16H_CATS))
LM_OPTS = "\n".join(f"{chr(65+i)}) {c}" for i, c in enumerate(LM_CATS))

X_IN16H = f"""Look at the image and decide which object it shows.

The photograph is in greyscale and has been degraded with visual noise, so it may be hard
to make out. Judge it as best you can.

Which category does the image show? Choose exactly one:
{IN16H_OPTS}

You must pick one; there is no "none of the above" option."""

X_LM = f"""Look at the image and decide which kind of scene it shows.

Which category does the image show? Choose exactly one:
{LM_OPTS}

You must pick one; there is no "none of the above" option."""

X_PICO = """Below is the abstract of a medical clinical-trial article.

Abstract: {text}

Question: Who were the participants in this trial?

Answer by quoting, word for word, every passage of the abstract that describes them - their
number, condition, age, sex, or any other characteristic identifying who was studied. Do not
paraphrase. Return an empty list if the abstract does not say."""


def block(head, task, schema):
    return f"{head}\n\n{task}\n\n{JSON_ONLY}\n{schema}\n"


V = "Provide your answer and your confidence in this answer."


def trio(head, schema_a, cot_task, topk_task, schema_cot, schema_topk):
    return {
        "vanilla": block(head, V, schema_a),
        "cot": block(head, cot_task, schema_cot),
        "topk": block(head, topk_task, schema_topk),
    }


PROMPTS = {
    "control": {
        "crowdtruth": trio(
            C_CT,
            '{{"answer": ["[RELATION]", ...], "confidence": <integer 0-100>}}',
            "Work through the sentence step by step: establish what it asserts about the two terms,\n"
            "then determine which relation type(s) that assertion corresponds to. Then provide your\n"
            "answer and your confidence in this answer.",
            "Give your 3 most likely answers for the correct set of relation(s), together with the\n"
            "probability that each one is right (0% to 100%). Every answer is a complete selection and\n"
            "may list several relations. List them from most to least likely.",
            '{{"reasoning": "<2-3 sentences>", "answer": ["[RELATION]", ...], "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": ["[RELATION]", ...], "probability": <integer 0-100>}}, ...]}}'),
        "movie_reviews": trio(
            C_MR,
            '{{"answer": <integer 0-10>, "confidence": <integer 0-100>}}',
            "Work through the review step by step: note which remarks are favourable and which are\n"
            "critical, and how emphatic each is, then deduce the score the reviewer gave. Then provide\n"
            "your answer and your confidence in this answer.",
            "Give your 3 most likely answers for the star rating, together with the probability that\n"
            "each one is right (0% to 100%). List them from most to least likely.",
            '{{"reasoning": "<2-3 sentences>", "answer": <integer 0-10>, "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": <integer 0-10>, "probability": <integer 0-100>}}, ...]}}'),
        "sentiment": trio(
            C_SENT_FULL,
            '{{"answer": "pos" or "neg", "confidence": <integer 0-100>}}',
            "Work through the sentence step by step: note the words carrying opinion and any negation\n"
            "or contrast that flips them, then settle on the overall polarity. Then provide your answer\n"
            "and your confidence in this answer.",
            "Give your 2 most likely answers together with the probability that each one is right\n"
            "(0% to 100%).",
            '{{"reasoning": "<1-2 sentences>", "answer": "pos" or "neg", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "pos" or "neg", "probability": <integer 0-100>}}, ...]}}'),
        "conll_ner": trio(
            C_NER,
            '{{"answer": ["<tag>", ...], "confidence": [<integer 0-100>, ...]}}',
            "Begin by locating the entity spans and deciding their categories, then translate those\n"
            "spans into a tag for each token. Return exactly as many tags as there are tokens, in the\n"
            "same order, with a confidence for each.",
            "For EVERY token, give your 3 most likely tags together with the probability that each one\n"
            "is right (0% to 100%). Return exactly as many guess-lists as there are tokens, in order.",
            '{{"reasoning": "<brief>", "answer": ["<tag>", ...], "confidence": [<integer 0-100>, ...]}}',
            '{{"guesses": [[{{"answer": "<tag>", "probability": <integer 0-100>}}, ...], ...]}}'),
        "pico": trio(
            C_PICO,
            '{{"answer": ["<exact span>", ...], "confidence": <integer 0-100>}}',
            "Work through the abstract step by step: find where it introduces the people studied, then\n"
            "copy out those passages verbatim. Then provide your answer and your confidence in this\n"
            "answer.",
            "Give your 3 most likely answers for the full set of participant passages, together with\n"
            "the probability that each one is right (0% to 100%). List them from most to least likely.",
            '{{"reasoning": "<2-3 sentences>", "answer": ["<exact span>", ...], "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": ["<exact span>", ...], "probability": <integer 0-100>}}, ...]}}'),
        "quiz": trio(
            C_QUIZ,
            '{{"answer": "<letter>", "confidence": <integer 0-100>}}',
            "Work through the question step by step: settle what is actually being asked, discard the\n"
            "options that can be ruled out, then take the strongest of those that remain. Then provide\n"
            "your answer and your confidence in this answer.",
            "Give your 3 most likely answers together with the probability that each one is right\n"
            "(0% to 100%). List them from most to least likely.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<letter>", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "<letter>", "probability": <integer 0-100>}}, ...]}}'),
        "imagenet16h": trio(
            C_IN16H,
            '{{"answer": "<category>", "confidence": <integer 0-100>}}',
            "Work through the image step by step: set out what shapes and textures survive the\n"
            "noise, then settle on the category they best match. Then provide your answer and\n"
            "your confidence in this answer.",
            "Give your 3 most likely answers together with the probability that each one is right\n"
            "(0% to 100%). List them from most to least likely.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<category>", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "<category>", "probability": <integer 0-100>}}, ...]}}'),
        "labelme": trio(
            C_LM,
            '{{"answer": "<category>", "confidence": <integer 0-100>}}',
            "Work through the image step by step: set out the main things visible and how the\n"
            "scene is arranged, then settle on the category it best matches. Then provide your\n"
            "answer and your confidence in this answer.",
            "Give your 3 most likely answers together with the probability that each one is right\n"
            "(0% to 100%). List them from most to least likely.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<category>", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "<category>", "probability": <integer 0-100>}}, ...]}}'),
    },
    "customized": {
        # SEQUENCE SWAPPING - wording identical to basic, relation order reversed
        "crowdtruth": trio(
            X_CT,
            '{{"answer": ["[RELATION]", ...], "confidence": <integer 0-100>}}',
            "Analyze the sentence step by step: first identify what is stated about the two terms,\n"
            "then decide which relation(s) that statement expresses. Then provide your answer and\n"
            "your confidence in this answer.",
            "Provide your 3 best guesses for the correct set of relation(s), and the probability that\n"
            "each guess is correct (0% to 100%). Each guess is a complete selection, which may contain\n"
            "more than one relation. Order from most to least likely.",
            '{{"reasoning": "<2-3 sentences>", "answer": ["[RELATION]", ...], "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": ["[RELATION]", ...], "probability": <integer 0-100>}}, ...]}}'),
        # TRUE/FALSE - counterbalance {polarity} over positive/negative
        "sentiment": trio(
            X_SENT,
            '{{"answer": "True" or "False", "confidence": <integer 0-100>}}',
            "Analyze the sentence step by step: identify the sentiment-bearing words and any negation\n"
            "or contrast, then decide whether the statement above holds. Then provide your answer and\n"
            "your confidence in this answer.",
            "Provide your 2 best guesses and the probability that each is correct (0% to 100%).",
            '{{"reasoning": "<1-2 sentences>", "answer": "True" or "False", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "True" or "False", "probability": <integer 0-100>}}, ...]}}'),
        # SEQUENCE SWAPPING - same 11 options, reversed order (A=10 stars)
        "movie_reviews": trio(
            X_MR,
            '{{"answer": "<letter A-K>", "confidence": <integer 0-100>}}',
            "Analyze the review step by step: identify the positive and negative statements the\n"
            "reviewer makes and how strongly they are worded, then infer the star rating they gave.\n"
            "Then provide your answer and your confidence in this answer.",
            "Provide your 3 best guesses and the probability that each is correct (0% to 100%).\n"
            "Order from most to least likely.",
            '{{"reasoning": "<2-3 sentences>", "answer": "<letter A-K>", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "<letter A-K>", "probability": <integer 0-100>}}, ...]}}'),
        # MULTIPLE CHOICE - one call per token
        "conll_ner": trio(
            X_NER,
            '{{"answer": "<letter A-I>", "confidence": <integer 0-100>}}',
            "Analyze step by step: decide whether this token is part of a named entity, which category\n"
            "it belongs to, and whether it begins or continues that entity. Then provide your answer\n"
            "and your confidence in this answer.",
            "Provide your 3 best guesses and the probability that each is correct (0% to 100%).\n"
            "Order from most to least likely.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<letter A-I>", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "<letter A-I>", "probability": <integer 0-100>}}, ...]}}'),
        # QUESTION ANSWERING
        "pico": trio(
            X_PICO,
            '{{"answer": ["<exact span>", ...], "confidence": <integer 0-100>}}',
            "Analyze the abstract step by step: locate the sentence or sentences that introduce the\n"
            "people studied, then quote them exactly. Then provide your answer and your confidence in\n"
            "this answer.",
            "Provide your 3 best guesses for the complete answer, and the probability that each is\n"
            "correct (0% to 100%). Order from most to least likely.",
            '{{"reasoning": "<2-3 sentences>", "answer": ["<exact span>", ...], "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": ["<exact span>", ...], "probability": <integer 0-100>}}, ...]}}'),
        # MULTIPLE CHOICE - 16 lettered options, alphabetical (matches the 4x4 icon grid)
        "imagenet16h": trio(
            X_IN16H,
            '{{"answer": "<letter A-P>", "confidence": <integer 0-100>}}',
            "Analyze the image step by step: describe the shapes and textures you can make out\n"
            "through the noise, then decide which category best fits them. Then provide your\n"
            "answer and your confidence in this answer.",
            "Provide your 3 best guesses and the probability that each is correct (0% to 100%).\n"
            "Order from most to least likely.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<letter A-P>", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "<letter A-P>", "probability": <integer 0-100>}}, ...]}}'),
        # MULTIPLE CHOICE - 8 lettered options, alphabetical
        "labelme": trio(
            X_LM,
            '{{"answer": "<letter A-H>", "confidence": <integer 0-100>}}',
            "Analyze the image step by step: note the main elements you can see and how the scene\n"
            "is laid out, then decide which category best fits it. Then provide your answer and\n"
            "your confidence in this answer.",
            "Provide your 3 best guesses and the probability that each is correct (0% to 100%).\n"
            "Order from most to least likely.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<letter A-H>", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "<letter A-H>", "probability": <integer 0-100>}}, ...]}}'),
        # QUESTION WITH CONFIRMATION BIAS - planted suggestion, gold-independent (seed 42)
        "quiz": trio(
            X_QUIZ,
            '{{"answer": "<letter>", "confidence": <integer 0-100>}}',
            "Analyze the question step by step: establish what is being asked, rule out the options\n"
            "that cannot be correct, then choose the best of those remaining. Then provide your\n"
            "answer and your confidence in this answer.",
            "Provide your 3 best guesses and the probability that each is correct (0% to 100%).\n"
            "Order from most to least likely.",
            '{{"reasoning": "<1-2 sentences>", "answer": "<letter>", "confidence": <integer 0-100>}}',
            '{{"guesses": [{{"answer": "<letter>", "probability": <integer 0-100>}}, ...]}}'),
    },
}

# Which variation each dataset receives, per group. Used to name the files so the
# manipulation is visible without opening them.
VARIATION = {
    "control": {  # paraphrase is the shared control across all five
        "crowdtruth": "paraphrase",
        "movie_reviews": "paraphrase",
        "sentiment": "paraphrase",
        "conll_ner": "paraphrase",
        "pico": "paraphrase",
        "quiz": "paraphrase",
        "imagenet16h": "paraphrase",
        "labelme": "paraphrase",
    },
    "customized": {  # task-fitted, one manipulation per dataset
        "crowdtruth": "sequence_swapping",
        "sentiment": "true_false",
        "movie_reviews": "sequence_swapping",
        "conll_ner": "multiple_choice",
        "pico": "question_answering",
        "quiz": "confirmation_bias",
        "imagenet16h": "multiple_choice",
        "labelme": "multiple_choice",
    },
}

PLACEHOLDERS = {
    ("control", "crowdtruth"): {"sentence", "term1", "term2"},
    ("control", "movie_reviews"): {"text"},
    ("control", "sentiment"): {"sentence"},
    ("control", "conll_ner"): {"tokens"},
    ("control", "pico"): {"text"},
    ("control", "quiz"): {"question", "options", "letters"},
    # image datasets take NO placeholder -- the stimulus rides in the request payload
    ("control", "imagenet16h"): set(),
    ("control", "labelme"): set(),
    ("customized", "crowdtruth"): {"sentence", "term1", "term2"},
    ("customized", "movie_reviews"): {"text"},
    ("customized", "sentiment"): {"sentence", "polarity"},
    ("customized", "conll_ner"): {"sentence", "index", "token"},
    ("customized", "pico"): {"text"},
    ("customized", "quiz"): {"question", "options", "letters", "suggestion"},
    ("customized", "imagenet16h"): set(),
    ("customized", "labelme"): set(),
}

if __name__ == "__main__":
    n = 0
    for group, byds in PROMPTS.items():
        for strat in STRATEGIES:
            (OUT / group / strat).mkdir(parents=True, exist_ok=True)
            for ds, byst in byds.items():
                p = OUT / group / strat / f"{ds}_{VARIATION[group][ds]}.txt"
                p.write_text(byst[strat])
                n += 1
    print(f"wrote {n} variation templates under {OUT}\n")
    for g in PROMPTS:
        for ds in PROMPTS[g]:
            print(f"  {g:10s} {ds}_{VARIATION[g][ds]:18s} "
                  f"placeholders: {sorted(PLACEHOLDERS[(g, ds)])}")

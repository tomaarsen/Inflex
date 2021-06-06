#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

# This module implements A/AN inflexion for nouns

# Special cases of A/AN
ix = re.IGNORECASE | re.VERBOSE
xms = re.VERBOSE | re.MULTILINE | re.DOTALL
ORDINAL_AN = re.compile(r"\A [aefhilmnorsx]   -?th \Z", flags=ix)
ORDINAL_A = re.compile(r"\A [bcdgjkpqtuvwyz] -?th \Z", flags=ix)
EXPLICIT_AN = re.compile(
    r"\A (?: euler | hour(?!i) | heir | honest | hono )", flags=ix)
SINGLE_AN = re.compile(r"\A [aefhilmnorsx]   \Z", flags=ix)
SINGLE_A = re.compile(r"\A [bcdgjkpqtuvwyz] \Z", flags=ix)

# This pattern matches strings of capitals (i.e. abbreviations) that
# start with a "vowel-sound" consonant followed by another consonant,
# and which are not likely to be real words

ABBREV_AN = re.compile(r"""
    \A
    (?! FJO | [HLMNS]Y.  | RY[EO] | SQU
    |   ( F[LR]? | [HL] | MN? | N | RH? | S[CHKLMNPTVW]? | X(YL)?) [AEIOU]
    )
    [FHLMNRSX][A-Z]
""", flags=xms)

# This pattern codes the beginnings of all english words beginning with a
# 'Y' followed by a consonant. Any other Y-consonant prefix therefore
# implies an abbreviation...

INITIAL_Y_AN = re.compile(
    r"\A y (?: b[lor] | cl[ea] | fere | gg | p[ios] | rou | tt)", flags=ix)


def prepend_indefinite_article(word: str) -> str:
    """Prepend the indefinite article ("a" or "an") to `word`.

    Args:
        word (str): Input word or collocation.

    Returns:
        str: `word` prepended by "a" or "an".
    """
    return f"{select_indefinite_article(word)} {word}"


def select_indefinite_article(word: str) -> str:
    """Return the correct indefinite article ("a" or "an") for `word`.

    Args:
        word (str): Input word or collocation.

    Returns:
        str: Either "a" or "an".
    """
    # Handle ordinal forms: Single character followed by "-th" or "th", eg "A-th" -> "an A-th".
    if ORDINAL_A.match(word):
        return "a"
    if ORDINAL_AN.match(word):
        return "an"

    # Handle special cases: Special words (honest) or a single character, eg "a" -> "an a"
    if EXPLICIT_AN.match(word):
        return "an"
    if SINGLE_AN.match(word):
        return "an"
    if SINGLE_A.match(word):
        return "a"

    # Handle abbreviations
    if ABBREV_AN.match(word):
        return "an"
    if re.match(r"\A [aefhilmnorsx][.-]", word, flags=ix):
        return "an"
    if re.match(r"\A [a-z][.-]", word, flags=ix):
        return "a"

    # Handle consonants
    if re.match(r"\A [^aeiouy]", word, flags=ix):
        return "a"

    # Handle special vowel forms
    if re.match(r"\A e [uw]", word, flags=ix):
        return "a"
    if re.match(r"\A onc?e \b ", word, flags=ix):
        return "a"
    if re.match(r"\A uni (?: [^nmd] | mo)", word, flags=ix):
        return "a"
    if re.match(r"\A ut[th]", word, flags=ix):
        return "an"
    if re.match(r"\A u [bcfhjkqrst] [aeiou]", word, flags=ix):
        return "a"

    # Handle special capitals
    if re.match(r"\A U [NK] [AIEO]?", word, flags=re.X):
        return "a"

    # Handle vowels
    if re.match(r"\A [aeiou]", word, flags=ix):
        return "an"

    # Handle Y... (before certain consonants implies (unnaturalized) "I.." sound)
    if INITIAL_Y_AN.match(word):
        return "an"

    # Otherwise, guess "a"
    return "a"

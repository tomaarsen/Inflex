#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Optional
import prosodic

# import context

from inflexion.term import Term
from inflexion.adjective_core import (
    is_singular,
    is_plural,
    convert_to_singular,
    convert_to_plural,
)
from inflexion.noun import Noun


class Adjective(Term):

    _stem_regexes = {
        re.compile(r"([aiou])y\Z"): lambda match: f"{match.group(1)}y",
        re.compile(r"ey\Z"): lambda match: "i",
        re.compile(r"y\Z"): lambda match: "i",
        re.compile(r"e\Z"): lambda match: "",
        # re.compile(r"([dbmnt])\Z"): lambda match: match.group(1) * 2,
    }

    _stem_double_regex = re.compile(r"((?:[^aeiou]|^)[aeiouy]([bcdlgkmnprstvz]))\Z")

    def __init__(self, term: str):
        super().__init__(term)

        self._possessive_regex = re.compile(
            r"\A(.*)'s?\Z", flags=re.IGNORECASE | re.MULTILINE | re.DOTALL
        )
        self._possessive_inflexion = {
            # Term           0TH      1ST      2ND      3RD
            "my": {
                "singular": ["my",    "my",    "your",  "its"],
                "plural":   ["our",   "our",   "your",  "their"],
            },
            "your": {
                "singular": ["your",  "my",    "your",  "its"],
                "plural":   ["your",  "our",   "your",  "their"],
            },
            "her": {
                "singular": ["her",   "my",    "your",  "her"],
                "plural":   ["their", "our",   "your",  "their"],
            },
            "his": {
                "singular": ["his",   "my",    "your",  "his"],
                "plural":   ["their", "our",   "your",  "their"],
            },
            "its": {
                "singular": ["its",   "my",    "your",  "its"],
                "plural":   ["their", "our",   "your",  "their"],
            },
            "our": {
                "singular": ["my",    "my",    "your",  "its"],
                "plural":   ["our",   "our",   "your",  "their"],
            },
            "their": {
                "singular": ["their", "my",    "your",  "its"],
                "plural":   ["their", "our",   "your",  "their"],
            },
        }

        self._comparative_conversions = {
            "good": "better",
            "well": "better",
            
            "bad": "worse",
            "badly": "worse",
            "ill": "worse",

            "far": "further",
            # "little": "less", # Could also be "littler", e.g. "little book" -> "even littler book"
            "many": "more",
            "much": "more",
        }

        self._superlative_conversions = {
            "good": "best",
            "well": "best",
            
            "bad": "worst",
            "badly": "worst",
            "ill": "worst",

            "far": "furthest",
            # "little": "least", # We opt for littlest
            "many": "most",
            "much": "most",
        }

    """
    Override default methods from Term    
    """

    def is_adj(self) -> bool:
        return True

    def is_singular(self) -> bool:
        return is_singular(self.term)

    def is_plural(self) -> bool:
        return is_plural(self.term)

    def singular(self, person: Optional[int] = 0) -> str:
        # Is it possessive form?
        match = self._possessive_regex.match(self.term)
        if match:
            return self._reapply_whitespace(Noun(match.group(1)).singular() + "'s")
        
        if self.term.lower() in self._possessive_inflexion:
            return self._encase(self._possessive_inflexion[self.term.lower()]["singular"][person])
        
        return self._encase(convert_to_singular(self.term))

    def plural(self, person: Optional[int] = 0) -> str:
        # Is it possessive form?
        match = self._possessive_regex.match(self.term)
        if match:
            n = Noun(match.group(1)).plural() + "'s"
            return self._reapply_whitespace(re.sub(r"s's\Z", "s'", n, flags=re.MULTILINE | re.DOTALL))
        
        if self.term.lower() in self._possessive_inflexion:
            return self._encase(self._possessive_inflexion[self.term.lower()]["plural"][person])
        
        return self._encase(convert_to_plural(self.term))

    def is_one_syllable(self, term: str):
        converted = ''.join("V" if char in "aeiou" else "C" for char in term.lower())
        while "CC" in converted:
            converted = converted.replace("CC", "C")
        return "VCV" not in converted

    def _stem(self, term: str) -> str:
        # Utility method that adjusts final consonants when they need to be doubled in inflexions...
        # Apply the first relevant transform...
        for regex in Adjective._stem_regexes:
            match = regex.search(term)
            if match:
                # Adding `term[match.end():]` is unnecessary for now, but allows for more complex regexes.
                return term[:match.start()] + Adjective._stem_regexes[regex](match) + term[match.end():]

        # Get a prosodic Word object to find the stress
        word = prosodic.Word(term)
        
        # Duplicate last letter if:
        if  (
            len(word.children) == 1                                     # The word is certainly just one syllable, or
            or (not word.children and self.is_one_syllable(term))       # The word is just one syllable, or
            or (word.children and word.children[-1].stressed)           # The last syllable is stressed
            ) and Adjective._stem_double_regex.search(term):            # AND the word ends in (roughly) CVC
            return term + term[-1]

        return term

    def comparative(self) -> str:
        if self.term.lower() in self._comparative_conversions:
            return self._comparative_conversions[self.term.lower()]

        pattern = re.compile(r"-| ")
        match = pattern.search(self.term)
        if match:
            term, remainder = self.term[:match.start()], self.term[match.end():]
            output_format = f"{{}}{match.group()}{{}}"
            return output_format.format(Adjective(term).comparative(), remainder)

        return self._stem(self.term) + "er"

    def superlative(self) -> str:
        """
        NOTE: "little" or "far" will fail due to having multiple options
          little (kid)  -> littlest (kid)
          little (food) -> least (food)
        and 
          far -> furthest
          far -> farthest
        NOTE: Fails on e.g. "boring" or "famous"
          We convert these to "boringest" and "famousest".
          In reality they should be "most boring" and "most famous"
        """
        if self.term.lower() in self._superlative_conversions:
            return self._superlative_conversions[self.term.lower()]

        pattern = re.compile(r"-| ")
        match = pattern.search(self.term)
        if match:
            term, remainder = self.term[:match.start()], self.term[match.end():]
            output_format = f"{{}}{match.group()}{{}}"
            return output_format.format(Adjective(term).superlative(), remainder)

        return self._stem(self.term) + "est"
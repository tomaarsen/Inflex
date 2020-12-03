#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Optional

# import context

from inflexion.term import Term
from inflexion.verb_core import (
    is_plural,
    is_singular,
    is_past,
    is_pres_part,
    is_past_part,
    convert_to_singular,
    convert_to_plural,
    convert_to_past,
    convert_to_pres_part,
    convert_to_past_part,
)

class Verb(Term):
    def __init__(self, term: str):
        super().__init__(term)

        self._term_regexes = {
            re.compile(r"ie\Z"): lambda match: "y",
            re.compile(r"ue\Z"): lambda match: "u",
            re.compile(r"([auy])e\Z"): lambda match: match.group(1),
            re.compile(r"ski\Z"): lambda match: "ski",
            re.compile(r"[^b]i\Z"): lambda match: "",
            re.compile(r"([^e])e\Z"): lambda match: match.group(1),
            re.compile(r".*er\Z"): lambda match: match.group(),
            re.compile(r"(.[bdghklmnprstz][o]([n]))\Z"): lambda match: match.group(1),
            re.compile(r"([^aeiou][aeiouy]([bcdlgmnprstv]))\Z"): lambda match: match.group(1) + match.group(2),
            re.compile(r"e\Z"): lambda match: "",
        }

    """
    Override default methods from Term    
    """
    def is_verb(self) -> bool:
        return True

    def is_singular(self) -> bool:
        return is_singular(self.term)

    def is_plural(self) -> bool:
        return is_plural(self.term)

    def singular(self, person:Optional[int] = 0) -> str:
        # TODO: Ensure valid person

        # "To be" is special
        if self.term.lower() in ["is", "am", "are"]:
            if person == 0:
                return self._reapply_whitespace(self.term)
            if person == 2 or not self.is_singular():
                return self._encase("are")
            if person == 1:
                return self._encase("am")
            return self._encase("is")

        # Third person uses the "notational" singular inflection
        if person == 3 or person == 0:
            known = convert_to_singular(self.term)
            if known != "_":
                return self._encase(known)
            return self._reapply_whitespace(self.term)

        # First and second person always use the uninflected (i.e. "notational plural" form)
        return self.plural()

    def plural(self, person:Optional[int] = 0) -> str:
        # Problems: "using" -> "using"
        known = convert_to_plural(self.term)
        if known != "_":
            return self._encase(known)
        return self._reapply_whitespace(self.term)
    
    def as_regex(self) -> re.Pattern:
        return re.compile("|".join(sorted(map(re.escape, {self.singular(),
                                                          self.plural(),
                                                          self.past(),
                                                          self.past_part(),
                                                          self.classical().pres_part()}), reverse=True)), flags=re.I)

    """
    Methods exclusively for Verb
    """

    def _stem(self, term: str) -> str:
        # Utility method that adjusts final consonants when they need to be doubled in inflexions...
        # Apply the first relevant transform...
        for regex in self._term_regexes:
            match = regex.search(term)
            if match:
                return regex.sub(self._term_regexes[regex](match), term)
        return term

    def past(self) -> str:
        # Problems: "using" -> "usinged"
        root = self.plural()
        known = convert_to_past(self.term)
        # print(f"Known past of term: {known}")
        if known == "_":
            known = convert_to_past(root)
            # print(f"Known past of root: {known}")

        # Otherwise use the standard pattern
        if known == "_":
            known = self._stem(root) + "ed"
            # print(f"Standard pattern past: {known}")

        return self._encase(known)

    def pres_part(self) -> str:
        # Problems: "using" -> "usinging"
        root = self.plural()
        # known = convert_to_pres_part(self.term)
        # print(f"Known pres_part of term: {known}")
        # if known == "_":
        known = convert_to_pres_part(root)
        # print(f"Known pres_part of root: {known}")

        # Otherwise use the standard pattern
        if known == "_":
            known = self._stem(root) + "ing"
            # print(f"Standard pattern pres_part: {known}")

        return self._encase(known)

    def past_part(self) -> str:
        # Problems: "using" -> "usinged"
        root = self.plural()
        # known = convert_to_past_part(self.term)
        # print(f"Known past_part of term: {known}")
        # if known == "_":
        known = convert_to_past_part(root)
        # print(f"Known past_part of root: {known}")

        # Otherwise use the standard pattern
        if known == "_":
            known = self._stem(root) + "ed"
            # print(f"Standard pattern past_part: {known}")

        return self._encase(known)
    
    def is_past(self) -> str:
        return is_past(self.term)

    def is_pres_part(self) -> str:
        return is_pres_part(self.term)

    def is_past_part(self) -> str:
        return is_past_part(self.term)

    def indefinite(self, count:Optional[int] = 1) -> str:
        if count == 1:
            return self.singular()
        return self.plural()

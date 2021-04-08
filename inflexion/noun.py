#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Optional, Tuple


from inflexion.term import Term
from inflexion.noun_core import (
    is_singular,
    is_plural,
    convert_to_classical_plural,
    convert_to_modern_plural,
    convert_to_singular,
)
from inflexion.indefinite_core import (
    select_indefinite_article,
    prepend_indefinite_article,
)


class Noun(Term):

    _noun_inflection = {
        # CASE 
        #   TERM             0TH            1ST             2ND             3RD
        "nominative": {
            "i": {
                "number": "singular",
                "person": 1,
                "singular": ["I",           "I",            "you",          "it"],
                "plural":   ["we",          "we",           "you",          "they"],
            },
            "you": {
                "number": "singular",
                "person": 2,
                "singular": ["you",         "I",            "you",          "it"],
                "plural":   ["you",         "we",           "you",          "they"],
            },
            "she": {
                "number": "singular",
                "person": 3,
                "singular": ["she",         "I",            "you",          "she"],
                "plural":   ["they",        "we",           "you",          "they"],
            },
            "he": {
                "number": "singular",
                "person": 3,
                "singular": ["he",          "I",            "you",          "he"],
                "plural":   ["they",        "we",           "you",          "they"],
            },
            "it": {
                "number": "singular",
                "person": 3,
                "singular": ["it",          "I",            "you",          "it"],
                "plural":   ["they",        "we",           "you",          "they"],
            },
            "we": {
                "number": "plural",
                "person": 1,
                "singular": ["I",           "I",            "you",          "it"],
                "plural":   ["we",          "we",           "you",          "they"],
            },
            "they": {
                "number": "plural",
                "person": 3,
                "singular": ["it",          "I",            "you",          "it"],
                "plural":   ["they",        "we",           "you",          "they"],
            },
            "one": {
                "number": "singular",
                "person": 3,
                "singular": ["one",         "I",            "you",          "one"],
                "plural":   ["some",        "we",           "you",          "some"],
            },
            "this": {
                "number": "singular",
                "person": 3,
                "singular": ["this",        "this",         "this",         "this"],
                "plural":   ["these",       "these",        "these",        "these"],
            },
            "that": {
                "number": "singular",
                "person": 3,
                "singular": ["that",        "that",         "that",         "that"],
                "plural":   ["those",       "those",        "those",        "those"],
            },
            "these": {
                "number": "plural",
                "person": 3,
                "singular": ["this",        "this",         "this",         "this"],
                "plural":   ["these",       "these",        "these",        "these"],
            },
            "those": {
                "number": "plural",
                "person": 3,
                "singular": ["that",		"that",			"that",			"that"],
                "plural": ["those", "those", "those", "those"],
            },
            "who": {
                "number": "singular",
                "person": 3,
                "singular": ["who",         "who",          "who",          "who"],
                "plural":   ["who",         "who",          "who",          "who"],
            },
            "whoever": {
                "number": "singular",
                "person": 3,
                "singular": ["whoever",     "whoever",      "whoever",      "whoever"],
                "plural":   ["whoever",     "whoever",      "whoever",      "whoever"],
            },
            "whosoever": {
                "number": "singular",
                "person": 3,
                "singular": ["whosoever",   "whosoever",    "whosoever",    "whosoever"],
                "plural":   ["whosoever",   "whosoever",    "whosoever",    "whosoever"],
            },
        },
        # CASE
        #   TERM             0TH            1ST             2ND             3RD
        "objective": {
            "me": {
                "number": "singular",
                "person": 1,
                "singular": ["me",          "me",           "you",          "it"],
                "plural":   ["us",          "us",           "you",          "them"],
            },
            "you": {
                "number": "singular",
                "person": 2,
                "singular": ["you",         "me",           "you",          "it"],
                "plural":   ["you",         "us",           "you",          "them"],
            },
            "her": {
                "number": "singular",
                "person": 3,
                "singular": ["her",         "me",           "you",          "her"],
                "plural":   ["them",        "us",           "you",          "them"],
            },
            "him": {
                "number": "singular",
                "person": 3,
                "singular": ["him",         "me",           "you",          "him"],
                "plural":   ["them",        "us",           "you",          "them"],
            },
            "it": {
                "number": "singular",
                "person": 3,
                "singular": ["it",          "me",           "you",          "it"],
                "plural":   ["them",        "us",           "you",          "them"],
            },
            "one": {
                "number": "singular",
                "person": 3,
                "singular": ["one",         "me",           "you",          "one"],
                "plural":   ["some",        "us",           "you",          "some"],
            },
            "us": {
                "number": "plural",
                "person": 1,
                "singular": ["me",          "me",           "you",          "it"],
                "plural":   ["us",          "us",           "you",          "them"],
            },
            "them": {
                "number": "plural",
                "person": 3,
                "singular": ["it",          "me",           "you",          "it"],
                "plural":   ["them",        "us",           "you",          "them"],
            },
            "this": {
                "number": "singular",
                "person": 3,
                "singular": ["this",        "this",         "this",         "this"],
                "plural":   ["these",       "these",        "these",        "these"],
            },
            "that": {
                "number": "singular",
                "person": 3,
                "singular": ["that",        "that",         "that",         "that"],
                "plural":   ["those",       "those",        "those",        "those"],
            },
            "these": {
                "number": "plural",
                "person": 3,
                "singular": ["this",        "this",         "this",         "this"],
                "plural":   ["these",       "these",        "these",        "these"],
            },
            "those": {
                "number": "plural",
                "person": 3,
                "singular": ["that",        "that",         "that",         "that"],
                "plural":   ["those",       "those",        "those",        "those"],
            },
            "whom": {
                "number": "singular",
                "person": 3,
                "singular": ["whom",        "whom",         "whom",         "whom"],
                "plural":   ["whom",        "whom",         "whom",         "whom"],
            },
            "whomever": {
                "number": "singular",
                "person": 3,
                "singular": ["whomever",    "whomever",     "whomever",     "whomever"],
                "plural":   ["whomever",    "whomever",     "whomever",     "whomever"],
            },
            "whomsoever": {
                "number": "singular",
                "person": 3,
                "singular": ["whomsoever",  "whomsoever",   "whomsoever",   "whomsoever"],
                "plural":   ["whomsoever",  "whomsoever",   "whomsoever",   "whomsoever"],
            },
        },
        # CASE
        #   TERM              0TH            1ST             2ND             3RD
        "possessive": {
            "mine": {
                "number": "singular",
                "person": 1,
                "singular": ["mine",        "mine",         "yours",        "its"],
                "plural":   ["ours",        "ours",         "yours",        "theirs"],
            },
            "yours": {
                "number": "singular",
                "person": 2,
                "singular": ["yours",       "mine",         "yours",        "its"],
                "plural":   ["yours",       "ours",         "yours",        "theirs"],
            },
            "hers": {
                "number": "singular",
                "person": 3,
                "singular": ["hers",        "mine",         "yours",        "hers"],
                "plural":   ["theirs",      "ours",         "yours",        "theirs"],
            },
            "his": {
                "number": "singular",
                "person": 3,
                "singular": ["his",         "mine",         "yours",        "his"],
                "plural":   ["theirs",      "ours",         "yours",        "theirs"],
            },
            "its": {
                "number": "singular",
                "person": 3,
                "singular": ["its",         "mine",         "yours",        "its"],
                "plural":   ["theirs",      "ours",         "yours",        "theirs"],
            },
            "one's": {
                "number": "singular",
                "person": 3,
                "singular": ["one's",       "mine",         "yours",        "one's"],
                "plural":   ["theirs",      "ours",         "yours",        "theirs"],
            },
            "ours": {
                "number": "plural",
                "person": 1,
                "singular": ["mine",        "mine",         "yours",        "its"],
                "plural":   ["ours",        "ours",         "yours",        "theirs"],
            },
            "theirs": {
                "number": "plural",
                "person": 3,
                "singular": ["its",         "mine",         "yours",        "its"],
                "plural":   ["theirs",      "ours",         "yours",        "theirs"],
            },
            "whose": {
                "number": "singular",
                "person": 3,
                "singular": ["whose",       "whose",        "whose",        "whose"],
                "plural":   ["whose",       "whose",        "whose",        "whose"],
            },
            "whosever": {
                "number": "singular",
                "person": 3,
                "singular": ["whosever",    "whosever",     "whosever",     "whosever"],
                "plural":   ["whosever",    "whosever",     "whosever",     "whosever"],
            },
            "whosesoever": {
                "number": "singular",
                "person": 3,
                "singular": ["whosesoever", "whosesoever",  "whosesoever",  "whosesoever"],
                "plural":   ["whosesoever", "whosesoever",  "whosesoever",  "whosesoever"]
            },
        },
        # CASE
        #   TERM                0TH            1ST             2ND             3RD
        "reflexive": {
            "myself": {
                "number": "singular",
                "person": 1,
                "singular": ["myself",      "myself",       "yourself",     "itself"],
                "plural":   ["ourselves",   "ourselves",    "yourselves",   "themselves"],
            },
            "yourself": {
                "number": "singular",
                "person": 2,
                "singular": ["yourself",    "myself",       "yourself",     "itself"],
                "plural":   ["yourselves",  "ourselves",    "yourselves",   "themselves"],
            },
            "herself": {
                "number": "singular",
                "person": 3,
                "singular": ["herself",     "myself",       "yourself",     "herself"],
                "plural":   ["themselves",  "ourselves",    "yourselves",   "themselves"],
            },
            "himself": {
                "number": "singular",
                "person": 3,
                "singular": ["himself",     "myself",       "yourself",     "himself"],
                "plural":   ["themselves",  "ourselves",    "yourselves",   "themselves"],
            },
            "themself": {
                "number": "singular",
                "person": 3,
                "singular": ["themselves",  "myself",       "yourself",     "themselves"],
                "plural":   ["themselves",  "ourselves",    "yourselves",   "themselves"],
            },
            "itself": {
                "number": "singular",
                "person": 3,
                "singular": ["itself",      "myself",       "yourself",     "itself"],
                "plural":   ["themselves",  "ourselves",    "yourselves",   "themselves"],
            },
            "oneself": {
                "number": "singular",
                "person": 3,
                "singular": ["oneself",     "myself",       "yourself",     "oneself"],
                "plural":   ["oneselves",   "ourselves",    "yourselves",   "oneselves"],
            },
            "ourselves": {
                "number": "plural",
                "person": 1,
                "singular": ["myself",      "myself",       "yourself",     "itself"],
                "plural":   ["ourselves",   "ourselves",    "yourselves",   "themselves"],
            },
            "yourselves": {
                "number": "plural",
                "person": 2,
                "singular": ["yourself",    "myself",       "yourself",     "itself"],
                "plural":   ["yourselves",  "ourselves",    "yourselves",   "themselves"],
            },
            "themselves": {
                "number": "plural",
                "person": 3,
                "singular": ["itself",      "myself",       "yourself",     "themselves"],
                "plural":   ["themselves",  "ourselves",    "yourselves",   "themselves"],
            },
            "oneselves": {
                "number": "plural",
                "person": 3,
                "singular": ["oneself",     "myself",       "yourself",     "oneself"],
                "plural":   ["oneselves",   "ourselves",    "yourselves",   "oneselves"],
            },
        },
    }

    # Regex to detect a preposition
    _prep_regex = re.compile(
        r"""\A ( \s*(?:
                about   | above   | across  | after  | among   | around   | athwart
            | at      | before  | behind  | below  | beneath | besides?
            | between | betwixt | beyond  | but    | by      | during
            | except  | for     | from    | into   | in      | near     | off
            | of      | onto    | on      | out    | over    | since    | till
            | to      | under   | until   | unto   | upon    | within   | without | with
        )\s+)
        """, flags=re.IGNORECASE | re.VERBOSE
    )

    def __init__(self, term: str):
        # TODO: Trailing and preceding whitespace? Trailing whitespace would break singularisation
        # TODO: Normalise to lowercase before passing to noun_core functions, possibly preserve capitalisation
        super().__init__(term)

    """
    Override default methods from Term    
    """

    def is_noun(self) -> bool:
        return True

    def is_singular(self) -> bool:
        return is_singular(self.term)

    def is_plural(self) -> bool:
        return is_plural(self.term)

    def singular(self, person: Optional[int] = 0) -> str:
        # TODO: Check whether person is valid
        match = Noun._prep_regex.match(self.term)

        if match:
            prep = match.group()
            term = self.term[match.end():]

            for case in ["objective", "possessive", "reflexive", "nominative"]:
                if term.lower() in Noun._noun_inflection[case]:
                    return self._encase(prep + Noun._noun_inflection[case][term.lower()]["singular"][person])

            return self._encase(prep + convert_to_singular(term))

        for case in ["nominative", "objective", "possessive", "reflexive"]:
            if self.term.lower() in Noun._noun_inflection[case]:
                return self._encase(Noun._noun_inflection[case][self.term.lower()]["singular"][person])

        return self._encase(convert_to_singular(self.term))

    def plural(self, person: Optional[int] = 0) -> str:
        # TODO: Check whether person is valid
        match = Noun._prep_regex.match(self.term)

        if match:
            prep = match.group()
            term = self.term[match.end():]

            for case in ["objective", "possessive", "reflexive", "nominative"]:
                if term.lower() in Noun._noun_inflection[case]:
                    return self._encase(prep + Noun._noun_inflection[case][term.lower()]["plural"][person])

            return self._encase(prep + convert_to_modern_plural(term))

        for case in ["nominative", "objective", "possessive", "reflexive"]:
            if self.term.lower() in Noun._noun_inflection[case]:
                return self._encase(Noun._noun_inflection[case][self.term.lower()]["plural"][person])

        return self._encase(convert_to_modern_plural(self.term))

    def classical(self) -> "Term":
        # TODO: Cache this
        # TODO: Should we also have modern() ?
        # NOTE: This method of creating a Classical noun will repeat getting whitespace etc.
        # TODO: This might be broken actually ^^.
        if self.term == "them":
            return ClassicalNoun(self.term)
        return ClassicalNoun(self.singular())

    def as_regex(self) -> "re.Pattern":
        return re.compile("|".join(sorted(map(re.escape, {self.singular(),
                                                          self.plural(),
                                                          self.classical().plural()}), reverse=True)), flags=re.I)

    """
    Methods exclusively for Noun
    """

    def indef_article(self) -> str:
        return select_indefinite_article(self.term)

    def indefinite(self, count: Optional[int] = 1) -> str:
        if count == 1:
            return prepend_indefinite_article(self.term)
        return f"{count} {self.plural()}"

    def cardinal(self, threshold: int) -> str:
        raise NotImplementedError()

    def ordinal(self, threshold: int) -> str:
        raise NotImplementedError()


class ClassicalNoun(Noun):
    def __init__(self, term) -> None:
        # TODO: Consider that repr(Noun("books").classical()) will output "ClassicalNoun('book')"
        super().__init__(term)

    def plural(self, person: Optional[int] = 0) -> str:
        # TODO: Check whether person is valid
        return self._encase(convert_to_classical_plural(self.term))

    def classical(self) -> "Term":
        return self

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Generator, Optional

class Term(object):
    """
    `Term` is the base class of the `Noun`, `Verb`, `Adjective` subclasses,
    and holds some default implementations of methods used across these
    subclasses.
    """

    # Supported casing formats: I, lower, Title, UPPER, Mc
    # Note that if the passed word is "i", we always output "I"
    def _transform(func):
        return lambda word: "I" if word.lower() == "i" else func(word)

    _casing_formats = {
        "I": {
            "regex": re.compile(r"^I$"),
            "transformation": _transform(str.lower)
        },
        "Mc": {
            "regex": re.compile(r"^Mc[A-Z][^A-Z]+$"),
            "transformation": _transform(lambda word: "Mc" + word[2:].title() if word.lower().startswith("mc") else word.title())
        },
        "lower":{
            "regex": re.compile(r"^[^A-Z]+$"),
            "transformation": _transform(str.lower)
        },
        "title":{
            "regex": re.compile(r"^[A-Z][^A-Z]+$"),
            "transformation": _transform(str.title)
        },
        "upper":{
            "regex": re.compile(r"^[^a-z]+$"),
            "transformation": _transform(str.upper)
        },
    }

    # Regex for finding a word
    _word_regex = re.compile(r"([^\r\n\t\f\v\-\' ]+)")

    def __init__(self, term: str):
        super().__init__()
        # Whitestring strings before and after the terms
        self.start  = ""
        self.end    = ""
        # Default format for the separator between words
        self.spaces = [" "]

        self.term = term.strip()
        
        # Extract whitespace before and after the term
        if term.startswith(" ") or term.endswith(" "):
            self.start, self.end = re.match(r"(?P<start>^\s*).*?(?P<end>\s*$)", term).groups()

        # If there is troublesome double whitespace, find the substrings
        # between words and normalize them 
        # NOTE: Assume there are no tabs, newlines, etc. in the input terms
        if " " in self.term or "-" in self.term:
            self.spaces = re.findall(r"([\r\n\t\f\v\- ]+)", self.term)
        if "  " in self.term:
            self.term = re.sub(r"\s{2,}", self.term)

    def is_noun(self) -> bool:
        """
        Returns `True` only if this object is instantiated via Noun(term).
        """
        return False

    def is_verb(self) -> bool:
        """
        Returns `True` only if this object is instantiated via Verb(term).
        """
        return False

    def is_adj(self) -> bool:
        """
        Returns `True` only if this object is instantiated via Adjective(term)
        """
        return False

    def is_singular(self) -> bool:
        """
        Returns `True` only if this object represents a term of the singular grammatical number.
        """
        raise NotImplementedError()

    def is_plural(self) -> bool:
        """
        Returns `True` only if this object represents a term of the plural grammatical number.
        """
        raise NotImplementedError()

    def singular(self, person:Optional[int] = 0) -> str:
        """Returns this object's singular form.

        `person` Represents the grammatical "person" (1st, 2nd, 3rd). 
        This option only affects personal and possessive pronouns, 
        possessive adjectives, and verbs. Defaults to 0.
        """
        raise NotImplementedError()

    def plural(self, person:Optional[int] = 0) -> str:
        """Returns this object's singular form.

        `person` Represents the grammatical "person" (1st, 2nd, 3rd). 
        This option only affects personal and possessive pronouns, 
        possessive adjectives, and verbs. Defaults to 0.
        """
        raise NotImplementedError()

    def classical(self) -> "Term":
        """
        Returns an object always inflecting in the classical/unassimilated manner.

        For example:
        ```
        >>> Noun('cow').plural()
        'cows'
        >>> Noun('cow').classical().plural()
        'kine'
        ```

        Identical to `unassimilated()`
        """
        return self

    def unassimilated(self) -> "Term":
        """
        Returns an object always inflecting in the classical/unassimilated manner.

        For example:
        ```
        >>> Noun('cow').plural()
        'cows'
        >>> Noun('cow').unassimilated().plural()
        'kine'
        ```

        Identical to `classical()`
        """
        return self.classical()
    
    def as_regex(self) -> "re.Pattern":
        """
        Returns a `re.Pattern` object which case-insensitively matches
        any inflected form of the word.

        For example:
        ```
        >>> Noun('cherub').as_regex()
        re.compile('cherubs|cherubim|cherub', re.IGNORECASE)
        >>> Verb('eat').as_regex()
        re.compile('eats|eating|eaten|eat|ate', re.IGNORECASE)
        ```
        """
        return re.compile("|".join(sorted(map(re.escape, {self.singular(),
                                                          self.plural()}), reverse=True)), flags=re.I)

    def __repr__(self) -> str:
        """
        Returns a string representation of the class instance.
        """
        return f"{self.__class__.__name__}({self._reapply_whitespace(self.term)!r})"
    
    def _encase(self, target: str) -> str:
        """
        Apply casing from `self.term` string onto `target` string.

        TODO: Currently "Toms'" -> "Toms'S"
        """

        # Special case for 'I'
        if self.term == "I" or target == "I":
            return target
        
        # Get list of lambda functions that correspond to the
        # casing formats for `original`.
        transformations = []
        for word in Term._word_regex.findall(self.term):
            for casing_format in Term._casing_formats.values():
                if casing_format["regex"].match(word):
                    transformations.append(casing_format["transformation"])
                    break
            else:
                # If no casing regexes matches
                transformations.append(lambda word: word)
        
        # If no words found in term, just return target
        if not transformations:
            return target

        # Generator that gets next transformation until there is
        # just one transformation left, after which it will 
        # continuously yield that last transformation
        def get_transformations(transformations) -> Generator:
            while True:
                yield transformations[0]
                if len(transformations) > 1:
                    transformations = transformations[1:]
        
        # Apply the transformations found in `original` to `target`
        transformations_gen = get_transformations(transformations)
        return self._reapply_whitespace(Term._word_regex.sub(lambda match_obj: next(transformations_gen)(match_obj.group(0)), target))

    def _reapply_whitespace(self, phrase: str):
        """
        Reapply whitespace formats before, after and within a phrase,
        based on `self.start`, `self.end` and `self.spaces`
        """
        def get_spaces(spaces: list):
            while True:
                yield spaces[0]
                if len(spaces) > 1:
                    spaces = spaces[1:]

        spaces_gen = get_spaces(self.spaces)

        return self.start + re.sub("-| ", lambda _: next(spaces_gen), phrase.strip()) + self.end
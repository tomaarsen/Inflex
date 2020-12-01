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
    def __init__(self, term: str):
        super().__init__()
        self.term = term

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
    
    def as_regex(self) -> re.Pattern:
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
        return re.compile("|".join(sorted({self.singular(),
                                           self.plural()}, reverse=True)), flags=re.I)

    def __repr__(self) -> str:
        """
        Returns a string representation of the class instance.
        """
        return f"{self.__class__.__name__}({self.term!r})"
    
    def _encase(self, target: str) -> str:
        """
        Apply casing from `self.term` string onto `target` string.
        """

        # Special case for 'I'
        if self.term == "I" or target == "I":
            return target
        
        # Supported casing formats, lower, Title, UPPER
        casing_formats = {
            "lower":{
                "regex": re.compile(r"^[^A-Z]+$"),
                "transformation": lambda word: word.lower()
            },
            "title":{
                "regex": re.compile(r"^[A-Z][^A-Z]+$"),
                "transformation": lambda word: word.title()
            },
            "upper":{
                "regex": re.compile(r"^[^a-z]+$"),
                "transformation": lambda word: word.upper()
            },
        }
        # Regex for finding a word
        word_regex = re.compile(r"(\S+)")

        # Get list of lambda functions that correspond to the
        # casing formats for `original`.
        transformations = []
        for word in word_regex.findall(self.term):
            for casing_format in casing_formats.values():
                if casing_format["regex"].match(word):
                    transformations.append(casing_format["transformation"])
                    break
            else:
                # If no casing regexes matches
                transformations.append(lambda word: word)
        
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
        return word_regex.sub(lambda match_obj: next(transformations_gen)(match_obj.group(0)), target)
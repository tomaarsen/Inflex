#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    "Term"
]

import re
from typing import Callable, Generator, List, Optional, TypeVar
import warnings

T = TypeVar("T")


def list_to_generator(input_list: List[T]) -> Generator[T, None, None]:
    """Yield element from list, repeating the very last element infinitely.

    Args:
        input_list (List[T]): List of elements.

    Yields:
        T: Element of `input_list`
    """
    while True:
        yield input_list[0]
        if len(input_list) > 1:
            input_list = input_list[1:]


class Term(object):
    """`Term` is the base class of the `Noun`, `Verb`, `Adjective` subclasses,
    and holds some default implementations of methods used across these
    subclasses.

    Method docstrings from this class are inherited to the subclasses' methods.
    """

    def _transform(func: Callable[[str], str]) -> str:
        """If `func` is called with "i" or "I", then return "I", otherwise simply call `func`

        Args:
            func (Callable[[str], str]): Function for converting the casing of an input string.

        Returns:
            str: Input string converted according to `func`'s casing rules.
        """
        return lambda word: "I" if word.lower() == "i" else func(word)

    # Supported casing formats: I, lower, Title, UPPER, Mc
    # Note that if the passed word is "i", we always output "I"
    _casing_formats = {
        "I": {
            "regex": re.compile(r"^I$"),
            "transformation": _transform(str.lower)
        },
        "lower": {
            "regex": re.compile(r"^[^A-Z]+$"),
            "transformation": _transform(str.lower)
        },
        "title": {
            "regex": re.compile(r"^[A-Z][^A-Z]+$"),
            "transformation": _transform(str.title)
        },
        "upper": {
            "regex": re.compile(r"^[^a-z]+$"),
            "transformation": _transform(str.upper)
        },
        "Mc": {
            "regex": re.compile(r"^Mc[A-Z][^A-Z]+$"),
            "transformation": _transform(lambda word: "Mc" + word[2:].title() if word.lower().startswith("mc") else word.title())
        },
        "AbbreviationPlural": {
            "regex": re.compile(r"^[A-Z]+s$"),
            "transformation": _transform(lambda word: word[:-1].upper() + word[-1] if word.endswith(("s", "S")) else word.upper())
        }
    }

    # Regex for finding a word
    _word_regex = re.compile(r"([^\r\n\t\f\v\-\' ]+)")

    # Regex for extracting whitespace before and after input
    _whitespace_regex = re.compile(r"(?P<start>^\s*).*?(?P<end>\s*$)")

    def __init__(self, term: str):
        """Creates class instance with detection and conversion methods.

        Note:
            Capitalisation and whitespace will be preserved between input `term` and
            generated output.

        Args:
            term (str): Input word or collocation.
        """
        super().__init__()
        # Whitestring strings before and after the terms
        self.start = ""
        self.end = ""
        # Default format for the separator between words
        self.spaces = None

        self.term = term.strip()

        # Extract whitespace before and after the term
        if term.startswith(" ") or term.endswith(" "):
            self.start, self.end = Term._whitespace_regex.match(term).groups()

        # If there is troublesome double whitespace, find the substrings
        # between words and normalize them
        # NOTE: Assume there are no tabs, newlines, etc. in the input terms
        if " " in self.term or "-" in self.term:
            self.spaces = re.findall(r"([\r\n\t\f\v\- ]+)", self.term)
        if "  " in self.term:
            self.term = re.sub(r"\s{2,}", " ", self.term)

    def is_noun(self) -> bool:
        """Returns `True` only if this object is instantiated via Noun(term).

        Returns:
            bool: Returns `True` only if this object is instantiated via Noun(term).
        """
        return False

    def is_verb(self) -> bool:
        """Returns `True` only if this object is instantiated via Verb(term).

        Returns:
            bool: Returns `True` only if this object is instantiated via Verb(term).
        """
        return False

    def is_adj(self) -> bool:
        """Returns `True` only if this object is instantiated via Adjective(term)

        Returns:
            bool: Returns `True` only if this object is instantiated via Adjective(term).
        """
        return False

    def is_singular(self) -> bool:
        """Detect whether this object is in singular form.

        Returns:
            bool: True if this object is deemed singular.
        """
        raise NotImplementedError()

    def is_plural(self) -> bool:
        """Detect whether this object is in plural form.

        Returns:
            bool: True if this object is deemed plural.
        """
        raise NotImplementedError()

    def singular(self, person: Optional[int] = 0) -> str:
        """Returns this object's singular form.

        Args:
            person (Optional[int], optional): Represents the grammatical "person" (1st, 2nd, 3rd).
                This option only affects personal and possessive pronouns, possessive adjectives,
                and verbs. Defaults to 0.

        Returns:
            str: This object's singular form.
        """
        raise NotImplementedError()

    def plural(self, person: Optional[int] = 0) -> str:
        """Returns this object's plural form.

        Args:
            person (Optional[int], optional): Represents the grammatical "person" (1st, 2nd, 3rd).
                This option only affects personal and possessive pronouns, possessive adjectives,
                and verbs. Defaults to 0.

        Returns:
            str: This object's plural form.
        """
        raise NotImplementedError()

    def classical(self) -> "Term":
        """Returns an object always inflecting in the classical/unassimilated manner.

        Examples:
            ```
            >>> Noun('cow').plural()
            'cows'
            >>> Noun('cow').unassimilated().plural()
            'kine'
            ```

        Note:
            Identical to `unassimilated()`.

        Returns:
            Term: A Term object, or a subclass thereof.
        """
        return self

    def unassimilated(self) -> "Term":
        """Returns an object always inflecting in the classical/unassimilated manner.

        Examples:
            ```
            >>> Noun('cow').plural()
            'cows'
            >>> Noun('cow').unassimilated().plural()
            'kine'
            ```

        Note:
            Identical to `classical()`.

        Returns:
            Term: A Term object, or a subclass thereof.
        """
        return self.classical()

    def check_valid_person(self, person: int) -> bool:
        """Return True if `person` is valid, i.e. in [0, 1, 2, 3].

        Otherwise, return False and output a warning stating that the
        `person` parameter is invalid.

        Args:
            person (int): Represents the grammatical "person" (1st, 2nd, 3rd).

        Raises:
            UserWarning: If `person` is invalid, this warning is thrown.

        Returns:
            bool: True if `person` is valid, i.e. in [0, 1, 2, 3]. False Otherwise.
        """
        if person not in [0, 1, 2, 3]:
            warnings.warn(
                "Invalid `person` parameter supplied. Valid values include 0, 1, 2, and 3.",
                stacklevel=2)
            return False
        return True

    def as_regex(self) -> "re.Pattern":
        """Returns a `re.Pattern` which case-insensitively matches any inflected form of the word.

        Returns:
            re.Pattern: Compiled regex object which case-insensitively matches any inflected form
                of the word.

        Examples:
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
        """Return repr(self)

        Examples:
            ```
            >>>noun = Noun("book")
            >>>f"My noun: {noun!r}"
            "My noun: Noun('book')"
            ```
        """
        return f"{self.__class__.__name__}({self._reapply_whitespace(self.term)!r})"

    def _encase(self, target: str) -> str:
        """Apply casing from `self.term` string onto `target` string.

        TODO: Currently "show--off" -> "show----off"
        TODO: self.term as i-th and target as i-th -> I-th
            : Perhaps don't force capitalize I if followed by a hyphen.
        TODO: Let self.term as ABC and target as ABCs convert to ABCs rather than ABCS
            : Also consider that some Noun tests may be broken

        Args:
            target (str): The word or collocation on which to apply the casing
                that exists on `self.term`.

        Returns:
            str: `target`, but encased according to the patterns applied on `self.term`.
        """

        # Split off 's
        suffix = ""
        if target.endswith("'s"):
            target = target[:-2]
            suffix = "'s"

        # Special case for 'I'
        if self.term == "I" or target == "I":
            return self._reapply_whitespace(target + suffix)

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
            return self._reapply_whitespace(target + suffix)

        # Generator that gets next transformation until there is
        # just one transformation left, after which it will
        # continuously yield that last transformation
        # Apply the transformations found in `original` to `target`
        transformations_gen = list_to_generator(transformations)
        # Phrase is target, but with the proper casing from the term applied
        phrase = Term._word_regex.sub(
            lambda match_obj: next(transformations_gen)(match_obj.group()),
            target)
        return self._reapply_whitespace(phrase + suffix)

    def _reapply_whitespace(self, phrase: str) -> str:
        """Reapply whitespace formats before, after and within a phrase.
        Based on `self.start`, `self.end` and `self.spaces` which were saved at __init__().

        Args:
            phrase (str): The word or collocation on which whitespace and hyphens are added.

        Returns:
            str: `phrase`, but with whitespace before, after and within a phrase.
        """
        if self.spaces:
            spaces_iter = iter(self.spaces)
            return self.start +\
                re.sub("-| ",
                       lambda _: next(spaces_iter),
                       phrase.strip(),
                       count=len(self.spaces)) +\
                self.end
        return self.start + phrase.strip() + self.end

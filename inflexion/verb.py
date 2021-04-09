#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Optional, Tuple

from inflexion.syllable import Syllable
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
    plural_of,
    singular_of,
    past_of,
    pres_part_of,
    past_part_of,
)


class Verb(Term):
    """ """

    _prefixes = (
        'counter',
        'trans',
        'cross',
        'inter',
        'under',
        'fore',
        'back',
        'over',
        # 'post',
        'out',
        'mis',
        'for',
        'dis',
        'way',
        # 'pre',
        # 'sub',
        'un',
        'in',
        # 'be',
        'up',
        're',
        # 'co',
        # 'de',
    )

    """
    Regexes to be tried before applying -ed or -ing.
    E.g. "argue" is converted to "argu" according to these regexes,
    and then "ing" or "ed" are appended for present participle,
    and past/past participle respectively.
    This produces "arguing" and "argued".
    """
    _stem_regexes = {
        # Words ending in "fer" always duplicate their consonant,
        # e.g. "transfer" -> "transferr" (+ "ed" or "ing")
        re.compile(r"fer\Z"): lambda match: "ferr",
        # Words ending in "c" will have an extra "k" appended before
        # -ed and -ing. One exception is "arc" -> "arced".
        re.compile(r"c\Z"): lambda match: "ck",
        # Words ending in "ie" will end in "y" before appending
        # -ed or -ing.
        re.compile(r"ie\Z"): lambda match: "y",
        # Words ending with "ski" don't change,
        # and then immediately have -ed or -ing appended.
        re.compile(r"ski\Z"): lambda match: "ski",
        # Words ending with "e" prepended by anything other than an "e"
        # have that "e" stripped. e.g. "argue" -> "argu"
        re.compile(r"([^e])e\Z"): lambda match: match.group(1),
        # Words ending with "er" don't duplicate.
        re.compile(r"er\Z"): lambda match: match.group(),
        # Words ending with "en" don't duplicate,
        # unless the word is small, e.g. ken -> kenned, pen -> penned, yen -> yenned
        re.compile(r"..en\Z"): lambda match: match.group(),
        # Words ending with "on" don't duplicate.
        re.compile(r"(.[bdghklmnprstzy]on)\Z"): lambda match: match.group(1),
        # Convert duplicate "ee" into just one "e"
        re.compile(r"ee\Z"): lambda match: "e",
        # Always duplicate CVl (British English)
        re.compile(r"[^aeo][aeiuo]l\Z"): lambda match: match.group() + "l",
    }

    _stem_double_regex = re.compile(
        r"((?:[^aeiou]|^)[aeiouy]([bcdlgkmnprstvz]))\Z")

    def __init__(self, term: str):
        super().__init__(term)

    """
    Override default methods from Term    
    """

    def is_verb(self) -> bool:
        """ """
        return True

    def is_singular(self) -> bool:
        """ """
        return is_singular(self.term)

    def is_plural(self) -> bool:
        """ """
        return is_plural(self.term)

    def singular(self, person: Optional[int] = 0) -> str:
        """

        Args:
          person: Optional[int]:  (Default value = 0)

        Returns:

        """
        self.check_valid_person(person)

        # "To be" is special
        if self.term.lower() in ["is", "am", "are"]:
            if person == 0:
                # "are" is already singular, e.g. "they are my friend",
                # but the expected result is "is", so we opt for that.
                if self.term.lower() == "are":
                    return self._encase("is")
                return self._reapply_whitespace(self.term)
            if person == 2 or not self.is_singular():
                return self._encase("are")
            if person == 1:
                return self._encase("am")
            return self._encase("is")

        # Third person uses the "notational" singular inflection
        if person == 3 or person == 0:
            # Get first word, last section of that word (if "-" in the word)
            term, form = self.get_subterm(self.term)

            # If this term is in the list of known cases
            if term.lower() in singular_of:
                return self._encase(form.format(singular_of[term.lower()]))

            # Try splitting off a prefix
            prefix, subterm = self.split_prefix(term)
            if prefix:
                known = convert_to_singular(subterm)
                if known:
                    return self._encase(form.format(prefix + known))

            # Otherwise convert the first word, last section
            known = convert_to_singular(term)
            if known:
                return self._encase(form.format(known))

            # If all else fails, return the term
            return self._reapply_whitespace(self.term)

        # First and second person always use the uninflected (i.e. "notational plural" form)
        return self.plural()

    def plural(self, person: Optional[int] = 0) -> str:
        """

        Args:
          person: Optional[int]:  (Default value = 0)

        Returns:

        """
        self.check_valid_person(person)

        known = None
        # Get first word, last section of that word (if "-" in the word)
        term, form = self.get_subterm(self.term)

        # If this term is in the list of known cases
        if term.lower() in plural_of:
            return self._encase(form.format(plural_of[term.lower()]))

        # Try splitting off a prefix
        prefix, subterm = self.split_prefix(term)
        known = convert_to_plural(subterm)
        if known:
            return self._encase(form.format(prefix + known))

        # Otherwise convert the first word, last section
        known = convert_to_plural(term)
        if known:
            return self._encase(form.format(known))

        # If all else fails, return the term
        return self._reapply_whitespace(self.term)

    def as_regex(self) -> "re.Pattern":
        """ """
        return re.compile("|".join(sorted(map(re.escape, {self.singular(),
                                                          self.plural(),
                                                          self.past(),
                                                          self.past_part(),
                                                          self.classical().pres_part()
                                                          }), reverse=True)), flags=re.I)

    """
    Methods exclusively for Verb
    """

    def _stem(self, term: str) -> str:
        """

        Args:
          term: str: 

        Returns:

        """
        # Utility method that adjusts final consonants when they need to be doubled in inflexions
        # Apply the first relevant transform
        for regex in Verb._stem_regexes:
            match = regex.search(term)
            if match:
                # Adding `term[match.end():]` is unnecessary for now,
                # but allows for more complex regexes.
                return term[:match.start()] + Verb._stem_regexes[regex](match) + term[match.end():]

        # Get the last word from the term, and remove a potential prefix
        last_word = term.replace("-", " ").split()[-1]
        _, last_word = self.split_prefix(last_word)

        # Get a set of known syllable counts for last_word
        syllable_count = Syllable.count_syllables(last_word)

        # Duplicate last letter if:
        if (
            # The word is certainly just one syllable, or
            1 in syllable_count
            # The word is just one syllable, or
            or (not syllable_count and Syllable.guess_if_one_syllable(last_word))
            # The last syllable is stressed
            or (Syllable.ends_with_stress(last_word))
        ) and Verb._stem_double_regex.search(term):  # AND the word ends in (roughly) CVC
            return term + term[-1]

        return term

    def split_prefix(self, term: str) -> Tuple[str, str]:
        """Split the prefix off of the term.
        "unbind"    -> ("un", "bind")
        "mistake"   -> ("mis", "take")
        "reappear"  -> ("re", "appear")

        Args:
          term: str: 

        Returns:

        """
        if term.startswith(Verb._prefixes):
            for prefix in Verb._prefixes:
                if term.startswith(prefix) and len(term[len(prefix):]) > 1:
                    return prefix, term[len(prefix):]
        return "", term

    def get_subterm(self, term: str) -> Tuple[str, str]:
        """Extract last sub-section (split by '-') of the first word.
        "aaa-bbb ccc" -> ("aaa-{} ccc", "bbb")

        Args:
          term: str: 

        Returns:

        """
        form = "{}"
        if " " in term:
            split_term = term.split()
            # form = f"{{}} {' '.join(split_term[1:])}"
            form = "{}" + "".join(" " + t for t in split_term[1:])
            term = split_term[0]
        if "-" in term:
            split_term = term.split("-")
            # form = f"{'-'.join(split_term[:-1])}-" + form
            form = "".join(t + "-" for t in split_term[:-1]) + form
            term = split_term[-1]
        return term, form

    def past(self) -> str:
        """ """
        known = None
        # "To be" is special
        if self.term.lower() in ["is", "am"]:
            return "was"
        if self.term.lower() == "are":
            return "were"

        # Get first word, last section of that word (if "-" in the word)
        term, form = self.get_subterm(self.term)

        # If this term is in the list of known cases
        if term.lower() in past_of:
            return self._encase(form.format(past_of[term.lower()]))

        # Try splitting off a prefix
        prefix, subterm = self.split_prefix(term)
        if prefix:
            known = convert_to_past(subterm)
            if known:
                return self._encase(form.format(prefix + known))

        # Convert the root of the term
        root, form = self.get_subterm(self.plural())
        known = convert_to_past(root)
        if known:
            return self._encase(form.format(known))

        # Otherwise use the standard pattern on the root
        known = self._stem(root) + "ed"

        return self._encase(form.format(known))

    def pres_part(self) -> str:
        """ """
        known = None
        # If this term is in the list of known cases
        if self.term.lower() in pres_part_of:
            return self._encase(pres_part_of[self.term.lower()])

        # Get first word, last section of that word (if "-" in the word)
        term, form = self.get_subterm(self.plural())

        # Try splitting off a prefix
        prefix, subterm = self.split_prefix(term)
        if prefix:
            known = convert_to_pres_part(subterm)
            if known:
                return self._encase(form.format(prefix + known))

        # Convert the full (sub)term
        known = convert_to_pres_part(term)

        # Otherwise use the standard pattern on the root
        if known is None:
            known = self._stem(term) + "ing"

        return self._encase(form.format(known))

    def past_part(self) -> str:
        """ """
        known = None
        # If this term is in the list of known cases
        if self.term.lower() in past_part_of:
            return self._encase(past_part_of[self.term.lower()])

        # Get first word, last section of that word (if "-" in the word)
        term, form = self.get_subterm(self.plural())

        # Try splitting off a prefix
        prefix, subterm = self.split_prefix(term)
        if prefix:
            known = convert_to_past_part(subterm)
            if known:
                return self._encase(form.format(prefix + known))

        # Convert the full (sub)term
        known = convert_to_past_part(term)

        # Otherwise use the standard pattern on the root
        if known is None:
            known = self._stem(term) + "ed"

        return self._encase(form.format(known))

    def is_past(self) -> str:
        """ """
        return is_past(self.term)

    def is_pres_part(self) -> str:
        """ """
        return is_pres_part(self.term)

    def is_past_part(self) -> str:
        """ """
        return is_past_part(self.term)

    def indefinite(self, count: Optional[int] = 1) -> str:
        """

        Args:
          count: Optional[int]:  (Default value = 1)

        Returns:

        """
        if count == 1:
            return self.singular()
        return self.plural()

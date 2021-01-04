#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from typing import Optional, Tuple

import prosodic
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
        #'de',
    )

    _stem_regexes = {
        re.compile(r"fer\Z"): lambda match: "ferr",
        re.compile(r"c\Z"): lambda match: "ck",
        re.compile(r"ie\Z"): lambda match: "y",
        re.compile(r"ski\Z"): lambda match: "ski",
        re.compile(r"([^e])e\Z"): lambda match: match.group(1),
        re.compile(r".*er\Z"): lambda match: match.group(),
        re.compile(r".{2,}en\Z"): lambda match: match.group(), # Only if long enough {('ken', 'kened', ('kenned',)), ('yen', 'yened', ('yenned',)), ('pen', 'pened', ('penned',))}
        re.compile(r"(.[bdghklmnprstzy]on)\Z"): lambda match: match.group(1), # TODO: Try adding y
        re.compile(r"ee\Z"): lambda match: "e", # Turns "ee" to "e"
        re.compile(r"([^aeo][aeiuo])l\Z"): lambda match: match.group(1) + "ll", # Always duplicate CVl (British English)
    }

    _stem_double_regex = re.compile(r"((?:[^aeiou]|^)[aeiouy]([bcdlgkmnprstvz]))\Z")

    def __init__(self, term: str):
        super().__init__(term)

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
            term, form = self.get_subterm(self.term)
            prefix, subterm = self.split_prefix(term)
            if prefix:
                known = convert_to_singular(subterm)
                if known:
                    return self._encase(form.format(prefix + known))

            known = convert_to_singular(term)
            if known:
                return self._encase(form.format(known))
            
            return self._reapply_whitespace(self.term)

        # First and second person always use the uninflected (i.e. "notational plural" form)
        return self.plural()

    def plural(self, person:Optional[int] = 0) -> str:
        known = None
        term, form = self.get_subterm(self.term)
        
        prefix, subterm = self.split_prefix(term)
        known = convert_to_plural(subterm)
        if known:
            return self._encase(form.format(prefix + known))

        known = convert_to_plural(term)
        if known:
            return self._encase(form.format(known))

        return self._reapply_whitespace(self.term)
    
    def as_regex(self) -> "re.Pattern":
        return re.compile("|".join(sorted(map(re.escape, {self.singular(),
                                                          self.plural(),
                                                          self.past(),
                                                          self.past_part(),
                                                          self.classical().pres_part()}), reverse=True)), flags=re.I)

    """
    Methods exclusively for Verb
    """

    def is_one_syllable(self, term: str):
        converted = ''.join("V" if char in "aeiou" else "C" for char in term.lower())
        while "CC" in converted:
            converted = converted.replace("CC", "C")
        return "VCV" not in converted

    def _stem(self, term: str) -> str:
        # Utility method that adjusts final consonants when they need to be doubled in inflexions...
        # Apply the first relevant transform...
        for regex in Verb._stem_regexes:
            match = regex.search(term)
            # TODO: Make more efficient by using match start and stop indices
            if match:
                return regex.sub(Verb._stem_regexes[regex](match), term)

        # Get the last word from the term, and remove a potential prefix
        last_word = term.replace("-", " ").split()[-1]
        _, last_word = self.split_prefix(last_word)

        # Get a prosodic Word object to find the stress
        word = prosodic.Word(last_word)
        
        # Duplicate last letter if:
        if  (
            len(word.children) == 1                                     # The word is certainly just one syllable, or
            or (not word.children and self.is_one_syllable(last_word))  # The word is just one syllable, or
            or (word.children and word.children[-1].stressed)           # The last syllable is stressed
            ) and Verb._stem_double_regex.search(term):                 # AND the word ends in (roughly) CVC
            return term + term[-1]

        return term

    def split_prefix(self, term: str) -> Tuple[str, str]:
        """
        Split the prefix off of the term.
        "unbind"    -> ("un", "bind")
        "mistake"   -> ("mis", "take")
        "reappear"  -> ("re", "appear")
        """
        if term.startswith(Verb._prefixes):
            for prefix in Verb._prefixes:
                if term.startswith(prefix) and len(term[len(prefix):]) > 1:
                    return prefix, term[len(prefix):]
        return "", term

    def get_subterm(self, term: str) -> Tuple[str, str]:
        """
        Extract last sub-section (split by '-') of the first word.
        "aaa-bbb ccc" -> ("aaa-{} ccc", "bbb")
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
        known = None
        # Get first word, last section of that word (if "-" in the word)
        term, form = self.get_subterm(self.term)

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
        known = None
        # Get first word, last section of that word (if "-" in the word)
        term, form = self.get_subterm(self.plural())
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
        known = None
        # Get first word, last section of that word (if "-" in the word)
        term, form = self.get_subterm(self.plural())
        # Strip prefix if possible
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
        return is_past(self.term)

    def is_pres_part(self) -> str:
        return is_pres_part(self.term)

    def is_past_part(self) -> str:
        return is_past_part(self.term)

    def indefinite(self, count:Optional[int] = 1) -> str:
        if count == 1:
            return self.singular()
        return self.plural()

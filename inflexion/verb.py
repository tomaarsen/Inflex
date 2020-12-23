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

        # re.compile(r"ue\Z"): lambda match: "u", # Overlaps with rule for [^e]e
        # re.compile(r"([auy])e\Z"): lambda match: match.group(1), # Overlaps with rule for [^e]e
        # re.compile(r"[^b]i\Z"): lambda match: "", # I don't see the purpose
        # re.compile(r"([^aeiou][aeiouy]([bcdlgmnprstv]))\Z"): lambda match: match.group(1) + match.group(2),
#            re.compile(r"([^aeiou][aeiouy]([bcdlgkmnprstvz]))\Z"): lambda match: match.group(1) + match.group(2),
        # re.compile(r"(([aioeu])(?!\2)[aioeu]([^aioeu]))$"): lambda match: match.group(1) + match.group(3), # Different vowels, e.g. ue, ia, but not oo # seems worse
        # re.compile(r"^(.?[aeiou]([^aeiouwjxhqy]))\Z"): lambda match: match.group(1) + match.group(2), # Attempt to duplicate consonant for short word
        # re.compile(r"")
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
            """
            words = self.term.split()
            known = convert_to_singular(words[0])
            if known is not None:
                if words[1:]:
                    known += " " + " ".join(words[1:])
                return self._encase(known)
            return self._reapply_whitespace(self.term)
            """
            term, form = self.get_subterm(self.term)
            """
            # Check whether a known past exists when removing a prefix
            if term.startswith(Verb.PREFIXES):
                for prefix in Verb.PREFIXES:
                    if term.startswith(prefix) and len(term[len(prefix):]) > 1:
                        known = convert_to_singular(term[len(prefix):])
                        if known:
                            return self._encase(form.format(prefix + known))
                        break
            """
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
        # Problems: "using" -> "using"
        """
        words = self.term.split()
        known = convert_to_plural(words[0])
        if known is not None:
            if words[1:]:
                known += " " + " ".join(words[1:])
            return self._encase(known)
        return self._reapply_whitespace(self.term)
        """
        known = None
        term, form = self.get_subterm(self.term)
        
        # Check whether a known past exists when removing a prefix
        """
        if term.startswith(Verb.PREFIXES):
            for prefix in Verb.PREFIXES:
                if term.startswith(prefix):
                    known = convert_to_plural(term[len(prefix):])
                    if known:
                        known = prefix + known
                        # return self._encase(form.format(prefix + known))
                    break
        """
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
        # One line, but slower:
        # return re.search(r"[aieuo][^aieuo]+[aieuo]", term, flags=re.I) is not None

    """
    # Faster but uglier
    def is_one_syllable(self, term: str):
        term = term.lower()
        count = 0
        last_char = ""
        for char in term:
            if char in "aeiou" and last_char != "v":
                count += 1
                if count == 2:
                    return False
                last_char = "v"
            else:
                last_char = "c"
        return True
    """

    def _stem(self, term: str) -> str:
        # Utility method that adjusts final consonants when they need to be doubled in inflexions...
        # Apply the first relevant transform...
        for regex in Verb._stem_regexes:
            match = regex.search(term)
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
        """
        # Problems: "using" -> "usinged"
        root = self.plural()
        words = self.term.split()
        split_first_word = words[0].split("-")
        before = "-".join(split_first_word[:-1])
        words[0] = split_first_word[-1]
        known = convert_to_past(words[0])
        print(f"Known past of term: {known}")
        if known is None:
            words = root.split()
            before = "-".join(split_first_word[:-1])
            words[0] = split_first_word[-1]
            known = convert_to_past(words[0])
            print(f"Known past of root: {known}")

        if known is None and "-" in words[0]:
            split_first_word = words[0].split("-")
            past = convert_to_past(split_first_word[-1])
            if past:
                known = "-".join(split_first_word[:-1]) + "-" + past

        # TODO: Check if these prefixes are separate syllables
        prefixes = ('counter', 'trans', 'cross', 'inter', 'under', 'fore', 'back', 'over', 'out', 'mis', 'for', 'dis', 'way', 'un', 'in', 'de', 'be', 'up', 're')
        if known is None and words[0].startswith(prefixes):
            for prefix in prefixes:
                if words[0].startswith(prefix):
                    known = convert_to_past(words[0][len(prefix):])
                    if known:
                        known = prefix + known
                    break

        # Otherwise use the standard pattern
        if known is None:
            known = self._stem(words[0]) + "ed"
            # print(f"Standard pattern past: {known}")

        if words[1:]:
            known += " " + " ".join(words[1:])
        if before:
            known = before + "-" + known

        return self._encase(known)
        """
        known = None
        # Get first word, last section of that word (if "-" in the word)
        term, form = self.get_subterm(self.term)

        """
        # Check whether a known past exists when removing a prefix
        if term.startswith(Verb.PREFIXES):
            for prefix in Verb.PREFIXES:
                if term.startswith(prefix):
                    known = convert_to_past(term[len(prefix):])
                    if known:
                        known = prefix + known
                        # return self._encase(form.format(prefix + known))
                    break
        """
        prefix, subterm = self.split_prefix(term)
        if prefix:
            known = convert_to_past(subterm)
            if known:
                return self._encase(form.format(prefix + known))
        
        # Convert the full (sub)term
        known = convert_to_past(term)

        # Convert the root of the term
        if known is None:
            root, form = self.get_subterm(self.plural())
            known = convert_to_past(root)
        
        # Otherwise use the standard pattern on the root
        if known is None:
            known = self._stem(root) + "ed"

        return self._encase(form.format(known))

    def pres_part(self) -> str:
        """
        # Problems: "using" -> "usinging"
        root = self.plural()
        words = root.split()
        # known = convert_to_pres_part(self.term)
        # print(f"Known pres_part of term: {known}")
        # if known is None:
        known = convert_to_pres_part(words[0])
        # print(f"Known pres_part of root: {known}")

        # Otherwise use the standard pattern
        if known is None:
            known = self._stem(words[0]) + "ing"
            # print(f"Standard pattern pres_part: {known}")
        if words[1:]:
            known += " " + " ".join(words[1:])

        return self._encase(known)
        """
        known = None
        # Get first word, last section of that word (if "-" in the word)
        term, form = self.get_subterm(self.plural())
        # print(term, form)
        """
        # Check whether a known past exists when removing a prefix
        if term.startswith(Verb.PREFIXES):
            for prefix in Verb.PREFIXES:
                if term.startswith(prefix):
                    known = convert_to_pres_part(term[len(prefix):])
                    if known:
                        known = prefix + known
                        # return self._encase(form.format(prefix + known))
                    break
        """
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
        """
        # Problems: "using" -> "usinged"
        root = self.plural()
        words = root.split()
        # known = convert_to_past_part(self.term)
        # print(f"Known past_part of term: {known}")
        # if known is None:
        known = convert_to_past_part(words[0])
        # print(f"Known past_part of root: {known}")

        # Otherwise use the standard pattern
        if known is None:
            known = self._stem(words[0]) + "ed"
            # print(f"Standard pattern past_part: {known}")
        if words[1:]:
            known += " " + " ".join(words[1:])

        return self._encase(known)
        """
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

"""
Counter({'t': 29,
         'e': 16,
         'd': 15,
         'r': 15,
         'p': 11,
         'y': 7,
         'l': 7,
         'n': 6,
         's': 6,
         'g': 5,
         'o': 4,
         'w': 3,
         'k': 2,
         'b': 1,
         'i': 1,
         'O': 1})

Counter({'er': 10,
         'et': 9,
         'ip': 7,
         'it': 7,
         'nd': 7,
         'ay': 6,
         'at': 5,
         'ht': 5,
         'de': 5,
         'ar': 5,
         'ld': 3,
         'll': 3,
         'un': 3,
         've': 3,
         'ed': 3,
         'op': 3,
         'ag': 2,
         'te': 2,
         'el': 2,
         'ad': 2,
         'in': 2,
         'is': 2,
         'do': 2,
         'ow': 2,
         'og': 2,
         'go': 2,
         'us': 2,
         'ew': 1,
         'al': 1,
         'be': 1,
         'ee': 1,
         'se': 1,
         'up': 1,
         'ue': 1,
         'ol': 1,
         'ob': 1,
         'nt': 1,
         'ki': 1,
         'me': 1,
         'ot': 1,
         'ly': 1,
         'nk': 1,
         'eg': 1,
         'ns': 1,
         'KO': 1,
         'ak': 1,
         'as': 1,
         'ut': 1,
         'ie': 1,
         'an': 1})

Counter({'fer': 6,
         'ght': 5,
         'ide': 5,
         'lay': 4,
         'run': 3,
         'fit': 3,
         'ind': 3,
         'und': 3,
         'ive': 3,
         'eed': 3,
         'ter': 3,
         'ear': 3,
         'uip': 2,
         'ell': 2,
         'ild': 2,
         'ead': 2,
         'rop': 2,
         'let': 2,
         'eat': 2,
         'hip': 2,
         'say': 2,
         'ret': 2,
         'set': 2,
         'lew': 1,
         'zag': 1,
         'uat': 1,
         'old': 1,
         'lip': 1,
         'mit': 1,
         'rip': 1,
         'net': 1,
         'ute': 1,
         'lel': 1,
         'eal': 1,
         'bat': 1,
         'be': 1,
         'see': 1,
         'ise': 1,
         'cup': 1,
         'sin': 1,
         'ver': 1,
         'het': 1,
         'cis': 1,
         'rin': 1,
         'ite': 1,
         'hop': 1,
         'que': 1,
         'ado': 1,
         'rol': 1,
         'mob': 1,
         'ent': 1,
         'end': 1,
         'ski': 1,
         'met': 1,
         'ome': 1,
         'tat': 1,
         'rot': 1,
         'uit': 1,
         'bag': 1,
         'par': 1,
         'low': 1,
         'fog': 1,
         'rgo': 1,
         'fly': 1,
         'hit': 1,
         'sit': 1,
         'tgo': 1,
         'iel': 1,
         'log': 1,
         'all': 1,
         'now': 1,
         'ink': 1,
         'gar': 1,
         'leg': 1,
         'ons': 1,
         'KO': 1,
         'eak': 1,
         'ias': 1,
         'but': 1,
         'lie': 1,
         'edo': 1,
         'sip': 1,
         'pan': 1,
         'lis': 1,
         'cus': 1,
         'lus': 1})
"""
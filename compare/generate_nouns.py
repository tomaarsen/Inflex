#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from typing import List, Tuple, Optional

"""
Keys existing in Lingua::EN::Inflexion, but not in mine:
classical_plural_of:
{'zoon', 'arf', 'lf', 'nse', 'sis', '-ox', ' ox'}
modern_plural_of:
{'zoon', 'arf', 'lf', 'nse', 'sis', '-ox', ' ox'}
singular_of:
{'zoa', 'arves', 'lves', 'nses', 'ses', '-oxen', ' oxen'}

There are no keys in mine that are not in Lingua
"""

"""
Compiled variants of useful regexes used all around this file
"""
xms = re.VERBOSE | re.MULTILINE | re.DOTALL
COMMENT_LINE_PAT = re.compile(r" \A \s* \#",         flags=xms)
COMMENT_PAT = re.compile(r" \# .* ",            flags=xms)
BLANK_LINE_PAT = re.compile(r" \A \s* $ ",         flags=xms)
WS = re.compile(r" [\s]* ",            flags=xms)
DATA_PAT = re.compile(r"""
    \A
      (?: {WS} < ([^>]+) > )?    # ...optional category tag
      {WS} ([*-]?) {WS}             # ...leading whitespace and optional generic marker
      (.*?)                     # ...singular word
      {WS} =>                    # ...singular/plural separator
      {WS} ([*-]?) {WS}             # ...leading whitespace and optional generic marker
      (.*?)                     # ...plural of word
      (?:                       # ...optionally:
        {WS} \|                  #    ...modern/classical separator
        {WS} ([*-]?) {WS}           #    ...leading whitespace and optional generic marker
        (.*?)                   #    ...classical plural of word
      )?
    {WS}                         # ...trailing whitespace
    (?:{COMMENT_PAT})?               # Optional trailing comment
    \Z                          # ...trailing whitespace
""".format(WS=WS.pattern, COMMENT_PAT=COMMENT_PAT.pattern),
    flags=xms)
RECURSE = re.compile(r"\(SING\) | \(PREP\)", flags=xms)
RECURSE_GROUPED = re.compile(r"""
      (?P<star>  \*        )
    | (?P<sing>  \(SING\)  )
    | (?P<plur>  \(PL\)    )
    | (?P<prep>  \(PREP\)  )
""", flags=xms)
"""
CONS     = re.compile(r"\(CONS\)", flags=xms)
VOWEL    = re.compile(r"\(VOWEL\)", flags=xms)
VOWELY   = re.compile(r"\(VOWELY\)", flags=xms)
"""
DASH = re.compile(r"-")
STAR = re.compile(r"\*")
RESTRICT = re.compile(r"( \[.*?\] )+", flags=xms)
"""
SPLIT    = re.compile(r"(.*?) [|] (.*)", flags=xms)
"""


class Word(object):
    def __init__(self, gen: Optional[str], word: Optional[str]):
        super().__init__()
        self.gen = gen or ""
        self.word = word or ""
        self.restrict = ""

    def expand_dash_star(self):
        """
        Replace - and * with the proper regex variant in input gen: "-" -> ".+"
        """
        if not self.gen:
            return
        self.gen = DASH.sub(r".+", self.gen)
        self.gen = STAR.sub(r".*", self.gen)

    '''
    def expand_cons_vowel(self) -> str:
        """
        Replace (CONS), (VOWEL) and (VOWELS) macros in input verb, e.g. "(VOWEL)ys" -> "[aeiou]ys"
        """
        self.word = CONS.sub(r"[^aeiou]", self.word)
        self.word = VOWEL.sub(r"[aeiou]", self.word)
        self.word = VOWELY.sub(r"[aeiouy]", self.word)
    '''

    def restrict_word(self) -> str:
        """
        Input verb (e.g. "[aeiou]ys") is split up into restriction (e.g. "[aeiou]") and remainder (e.g. "ys")
        """
        if not self.word:
            return
        match = RESTRICT.search(self.word)
        if match:
            self.restrict = match.group()
            self.word = RESTRICT.sub(r"", self.word, count=1)

    '''
    def split(self) -> Optional[str]:
        match = SPLIT.match(self.word)
        if match:
            self.word = match.group(1)
            return match.group(2)
        return None
    '''

    def __str__(self) -> str:
        return f"{self.gen or ''}{self.restrict}{self.word}"


class Noun(object):
    def __init__(self, match):
        super().__init__()
        # tag                   Optional category tag, eg "nonindicative"
        # is_generic            "*", "-" or ""
        # sing:                 Singular word
        # is_pure_generic       "*", "-" or ""
        # pl1:                  Plural word 1
        # other                 "*", "", "-", None
        # pl2:                  Plural word 2
        self.tag = match.group(1) or ""
        self.sing = Word(match.group(2), match.group(3))
        self.sing.expand_dash_star()
        self.sing.restrict_word()

        self.plur_one = Word(match.group(4), match.group(5))
        self.plur_one.restrict_word()
        self.plur_two = Word(match.group(6), match.group(7))
        self.plur_two.restrict_word()
        # TODO: Check if this can be removed
        # If the first plural does not exist, have both point to the same object
        if not self.plur_one.word:
            self.plur_one = self.plur_two

    def has_hyphen(self):
        return "-" in self.sing.word or "-" in self.plur_one.word or "-" in self.plur_two.word

    def replace_hyphens(self, repl: str):
        self.sing.word = self.sing.word.replace("-", repl)
        self.plur_one.word = self.plur_one.word.replace("-", repl)
        self.plur_two.word = self.plur_two.word.replace("-", repl)

    def __str__(self) -> str:
        # return (f"<{self.tag}> " if self.tag else "") + f"{self.sing}: {self.plur_one} | "
        return "{: <14} : {: <20} => {: <20} | {: <20}".format(self.tag or "",
                                                               str(self.sing),
                                                               str(
                                                                   self.plur_one) if self.plur_one.word else "",
                                                               str(self.plur_two) if self.plur_two.word else "")


class Reader(object):
    def __init__(self, fname: str):
        types = ["modern_plural", "classical_plural", "singular"]
        # self.patterns = {key:[] for key in types}
        # self.literals = {key:{} for key in types}
        self.words = {
            "plural": set(),
            "singular": set()
        }
        self.fname = fname

    def get_readlines(self) -> List[str]:
        with open(self.fname, "r") as f:
            return f.readlines()

    def parse_file(self):
        """
        Fill `pattern`, `literal` and `words`
        """

        lines = self.get_readlines()

        for line in lines:
            # Skip empty or comment lines
            if COMMENT_LINE_PAT.match(line) or BLANK_LINE_PAT.match(line):
                continue

            # Extract data
            match = DATA_PAT.match(line)
            if match:
                noun = Noun(match)
            else:
                # TODO: Change exception
                raise Exception("Unknown input:", line)

            if not RECURSE.search(noun.sing.word) and not noun.plur_one.gen:
                # self.add_literals(noun)
                self.add_words(noun)

                if noun.has_hyphen():
                    noun.replace_hyphens(" ")
                    # self.add_literals(noun)
                    self.add_words(noun)

    def add_words(self, noun):
        self.words["plural"].add(noun.plur_one.word)
        self.words["plural"].add(noun.plur_two.word)
        self.words["singular"].add(noun.sing.word)


if __name__ == "__main__":
    in_fname = "lei//nouns.lei"
    out_fname = "inflexion//noun_core.py"
    out_import = "noun_core"

    reader = Reader(in_fname)
    reader.parse_file()

    # Words from noun.py rather than nouns.lei
    words = {'oneselves', 'he', 'mine', 'whosesoever', 'she', 'we', 'these', 'whosoever', 'him', 'theirs', 'me', 'myself', 'this', "one's", 'those', 'herself', 'whom', 'it', 'ours', 'whomever', 'some', 'us', 'whomsoever', 'I', 'oneself', 'yourself', 'that', 'you', 'one', 'yourselves', 'whose', 'yours', 'hers', 'themselves', 'himself', 'her', 'who', 'ourselves', 'his', 'whosever', 'its', 'itself', 'they', 'them', 'whoever'}

    with open(f"compare/words/nouns.txt", "w+") as f:
        words = {*words, *reader.words["plural"], *reader.words["singular"]}
        f.write("\n".join(sorted(word for word in words if word)))

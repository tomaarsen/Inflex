#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from datetime import datetime
from typing import List, Tuple, Optional

"""
Compiled variants of useful regexes used all around this file
"""
xms = re.VERBOSE | re.MULTILINE | re.DOTALL
COMMENT_LINE_PAT = re.compile(r" \A \s* \#",         flags=xms)
COMMENT_PAT = re.compile(r" \# .* ",            flags=xms)
BLANK_LINE_PAT = re.compile(r" \A \s* $ ",         flags=xms)
WS = re.compile(r" [\s]* ",            flags=xms)
WORD_SEQ = re.compile(r" \S* (?: \s \S+)* ", flags=xms)
DATA_PAT = re.compile(r"""
    \A
        {WS}
        ([*-])? ( {WORD_SEQ} )      # 3rd person singular
        {WS}
        ([*-])? ( {WORD_SEQ} )      # 3rd person plural
        {WS}
        ([*-])? ( {WORD_SEQ} )      # Simple past (preterite)
        {WS}
        ([*-])? ( {WORD_SEQ} )      # Present continuous participle
        {WS}
        ([*-])? ( {WORD_SEQ} )      # Past participle
        {WS}
        (?:{COMMENT_PAT})?          # Optional trailing comment
    \Z
""".format(WS=WS.pattern, WORD_SEQ=WORD_SEQ.pattern, COMMENT_PAT=COMMENT_PAT.pattern),
    flags=xms)
CONS = re.compile(r"\(CONS\)", flags=xms)
VOWEL = re.compile(r"\(VOWEL\)", flags=xms)
VOWELY = re.compile(r"\(VOWELY\)", flags=xms)
DASH = re.compile(r"-")
STAR = re.compile(r"\*")
RESTRICT = re.compile(r"( \[.*?\] )+", flags=xms)
SPLIT = re.compile(r"(.*?) [|] (.*)", flags=xms)


class Word(object):
    def __init__(self, gen: Optional[str], word: str):
        super().__init__()
        self.gen = gen
        self.word = word
        self.restrict = ""

    def expand_dash_star(self):
        """
        Replace - and * with the proper regex variant in input gen: "-" -> ".+"
        """
        if not self.gen:
            return
        self.gen = DASH.sub(r".+", self.gen)
        self.gen = STAR.sub(r".*", self.gen)

    def expand_cons_vowel(self) -> str:
        """
        Replace (CONS), (VOWEL) and (VOWELS) macros in input verb, e.g. "(VOWEL)ys" -> "[aeiou]ys"
        """
        self.word = CONS.sub(r"[^aeiou]", self.word)
        self.word = VOWEL.sub(r"[aeiou]", self.word)
        self.word = VOWELY.sub(r"[aeiouy]", self.word)

    def restrict_word(self) -> str:
        """
        Input verb (e.g. "[aeiou]ys") is split up into restriction (e.g. "[aeiou]") and remainder (e.g. "ys")
        """
        match = RESTRICT.search(self.word)
        if match:
            self.restrict = match.group()
            self.word = RESTRICT.sub(r"", self.word, count=1)

    def split(self) -> Optional[str]:
        match = SPLIT.match(self.word)
        if match:
            self.word = match.group(1)
            return match.group(2)
        return None

    def __str__(self) -> str:
        return f"{self.gen or ''}{self.restrict}{self.word}"


class Verb(object):
    def __init__(self, match):
        super().__init__()
        """
        Extract line information.
        
        sing -> Singular
        plur -> Plural
        pret -> Preterite
        pres -> Present participle
        past -> Past participle

        ..._gen holds "-" and "*" generator for suffixes, e.g. in "-ys" or "*melts"
        """
        types = ["sing", "plur", "pret", "pres", "past"]
        self.verbs = {}
        for i, key in enumerate(types):
            # Get gen and verb of this word
            gen = match.group(i * 2 + 1)
            verb = match.group(i * 2 + 2)
            # Turn into Word object and add to list for this type
            w = Word(gen, verb)
            self.verbs[key] = w
            # It's possible this word can be split up, eg "was|were"
            if key == "pret":
                self.pret_plur = w.split()

        """
        For each word: 
        - Replace (CONS), (VOWEL) and (VOWELS) macros: "(VOWEL)ys" -> "[aeiou]ys"
        - Replace - and * with the proper regex variant: "-ys" -> ".+ys"
        - Split up word (e.g. "[aeiou]ys") into restriction (e.g. "[aeiou]") and remainder (e.g. "ys")
        """
        for word in self.verbs.values():
            word.expand_cons_vowel()
            word.expand_dash_star()
            word.restrict_word()

    def replace_hyphens(self, repl: str):
        for word in self.verbs.values():
            word.word = word.word.replace("-", repl)

    def __getitem__(self, key):
        return self.verbs[key]

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.verbs[name]

    def has_gen(self) -> bool:
        """
        Returns true iff there is at least one verb between the five that is prefixed with * or -
        """
        return any(self.verbs[key].gen for key in self.verbs)

    def __str__(self) -> str:
        return "\n".join(f"{key: <9}: {self.verbs[key]}" for key in self.verbs) + (f"\npret_plur: {self.pret_plur}" if self.pret_plur else "")


class Reader(object):
    def __init__(self, fname: str):
        types = ["plural", "singular", "past", "pres_part", "past_part"]
        self.patterns = {key: [] for key in types}
        self.literals = {key: {} for key in types}
        self.words = {key: set() for key in types}
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
                verb = Verb(match)
            else:
                # TODO: Change exception
                raise Exception("Unknown input:", line)

            if not (verb.sing.gen and verb.plur.gen and verb.pret.gen):
                self.add_words(verb)

                # If there is a hyphen in the singular verb, replace the hyphens
                # in all verbs, and add those to the literals and words too
                if "-" in verb.sing.word:
                    verb.replace_hyphens(" ")
                    self.add_words(verb)

    def add_words(self, verb):
        self.words["singular"].add(verb.sing.word)
        self.words["plural"].add(verb.plur.word)

        if verb.pret.word:
            self.words["past"].add(verb.pret.word)

            if verb.pret_plur:
                self.words["past"].add(verb.pret_plur)

        if verb.pres.word:
            self.words["pres_part"].add(verb.pres.word)

        if verb.past.word:
            self.words["past_part"].add(verb.past.word)


if __name__ == "__main__":
    in_fname = "lei//verbs.lei"
    out_fname = "inflexion//verb_core.py"
    out_import = "verb_core"
    reader = Reader(in_fname)
    reader.parse_file()

    with open(f"compare/words/verbs.txt", "w+") as f:
        words = {*reader.words["plural"], *reader.words["singular"], *
                 reader.words["past"], *reader.words["pres_part"], *reader.words["past_part"]}
        f.write("\n".join(sorted(word for word in words if word and word != "_")))

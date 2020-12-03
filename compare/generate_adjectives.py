#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
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
        ( {WORD_SEQ} )      # singular
        {WS}=>{WS}
        ( {WORD_SEQ} )      # plural
        {WS}
        (?:{COMMENT_PAT})?  # Optional trailing comment
    \Z
""".format(WS=WS.pattern, WORD_SEQ=WORD_SEQ.pattern, COMMENT_PAT=COMMENT_PAT.pattern),
    flags=xms)
"""
CONS     = re.compile(r"\(CONS\)", flags=xms)
VOWEL    = re.compile(r"\(VOWEL\)", flags=xms)
VOWELY   = re.compile(r"\(VOWELY\)", flags=xms)
DASH     = re.compile(r"-")
STAR     = re.compile(r"\*")
RESTRICT = re.compile(r"( \[.*?\] )+", flags=xms)
SPLIT    = re.compile(r"(.*?) [|] (.*)", flags=xms)
"""


class Adjective(object):
    def __init__(self, match):
        super().__init__()

        self.sing = match.group(1)
        self.plur = match.group(2)

    def __str__(self) -> str:
        return f"Singular: {self.sing}\nPlural  : {self.plur}"


class Reader(object):
    def __init__(self, fname: str):
        types = ["plural", "singular"]
        self.words = {key: set() for key in types}
        self.fname = fname

    def get_readlines(self) -> List[str]:
        with open(self.fname, "r") as f:
            return f.readlines()

    def parse_file(self):
        lines = self.get_readlines()

        # Read lines in reverse so the first lines are eventually checked before the later ones
        for line in lines[::-1]:
            # Skip empty or comment lines
            if COMMENT_LINE_PAT.match(line) or BLANK_LINE_PAT.match(line):
                continue

            # Extract data
            match = DATA_PAT.match(line)
            if match:
                sing = match.group(1)
                plur = match.group(2)
                self.words["plural"].add(plur)
                self.words["singular"].add(sing)
            else:
                # TODO: Change exception
                raise Exception("Unknown input:", line)

def get_cases(words):
    final_words = words.copy()
    for word in words:
        final_words.add(word.title())
        final_words.add(word.upper())
        final_words.add(word.lower())
        final_words.add(''.join(random.choice((str.upper, str.lower))(c) for c in word))
    return final_words

if __name__ == "__main__":
    random.seed(0)
    in_fname = "lei//adjectives.lei"
    out_fname = "inflexion//adjective_core.py"
    out_import = "adjective_core"
    reader = Reader(in_fname)
    reader.parse_file()

    with open(f"compare/words/adjectives.txt", "w+") as f:
        words = {*reader.words["plural"], *reader.words["singular"]}
        words = get_cases(words)
        f.write("\n".join(sorted(word for word in words if word)))

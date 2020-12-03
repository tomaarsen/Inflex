#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import re
import json
from datetime import datetime
import string
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
        self.words = set()
        self.fname = fname

    def get_readlines(self) -> List[str]:
        with open(self.fname, "r") as f:
            return f.readlines()

    def gen_string(self, min_length, max_length):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randrange(min_length, max_length)))

    def parse_file(self):
        """
        Fill `pattern`, `literal` and `words`
        """

        # Add conversions for possessives
        """
        self.patterns["modern_plural"].append({
            "from": r"(.*?)'s?",
            "to": "lambda match: convert_to_modern_plural(match.group(1)) + '\\'' if convert_to_modern_plural(match.group(1)).endswith('s') else convert_to_modern_plural(match.group(1)) + '\\'s'",
            "conv_conditional": "lambda match: is_singular(match.group(1))",
            "tag": ""
        })
        self.patterns["classical_plural"].append({
            "from": r"(.*?)'s?",
            "to": "lambda match: convert_to_classical_plural(match.group(1)) + '\\'' if convert_to_classical_plural(match.group(1)).endswith('s') else convert_to_classical_plural(match.group(1)) + '\\'s'",
            "conv_conditional": "lambda match: is_singular(match.group(1))",
            "tag": ""
        })
        self.patterns["singular"].append({
            "from": r"(.*?)'s?",
            "to": "lambda match: convert_to_singular(match.group(1)) + '\\'' if convert_to_singular(match.group(1)).endswith('s') else convert_to_singular(match.group(1)) + '\\'s'",
            "conv_conditional": "lambda match: is_plural(match.group(1))",
            "tag": ""
        })
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
            
            if noun.sing.gen:
                # If plus
                prefixes = [self.gen_string(1, 3), self.gen_string(2, 5), self.gen_string(4, 6)]
                restrict = ""
                if noun.sing.gen == ".*":
                    prefixes.append("")
                if noun.sing.restrict:
                    if noun.sing.restrict.startswith("[^"):
                        restrict = random.choice(list(set(string.ascii_lowercase) - set(noun.sing.restrict)))
                    else:
                        restrict = random.choice(noun.sing.restrict[1:-1])
                
                for prefix in prefixes:
                    self.words.add(f"{prefix}{restrict}{noun.sing.word}")
                    self.words.add(f"{prefix}{restrict}{noun.plur_one.word}")
                    if noun.plur_two.word:# and noun.plur_two.word != "_":
                        self.words.add(f"{prefix}{restrict}{noun.plur_two.word}")

            elif RECURSE.search(noun.sing.word):
                # self.add_recurse_patterns(noun)

                # if noun.has_hyphen():
                    # noun.replace_hyphens(" ")
                    # self.add_recurse_patterns(noun)

                # TODO: Investigate this setting to 1
                noun.plur_one.gen = 1
            
            if not noun.plur_one.gen:
                self.add_words(noun)

                if noun.has_hyphen():
                    noun.replace_hyphens(" ")
                    self.add_words(noun) 

    def add_recurse_patterns(self, noun):
        self.optionally_add_pattern(self.patterns["modern_plural"], {
            **self.build_recursive(_from=noun.sing.word, 
                                    to=noun.plur_one.word, 
                                    from_type="singular", 
                                    to_type="modern_plural"), 
            **{"tag": noun.tag}
        })
        self.optionally_add_pattern(self.patterns["singular"], {
            **self.build_recursive(_from=noun.plur_one.word, 
                                    to=noun.sing.word, 
                                    from_type="modern_plural", 
                                    to_type="singular"), 
            **{"tag": noun.tag}
        })

        if not noun.plur_two.word:
            noun.plur_two = noun.plur_one
        
        self.optionally_add_pattern(self.patterns["classical_plural"], {
            **self.build_recursive(_from=noun.sing.word, 
                                    to=noun.plur_two.word, 
                                    from_type="singular", 
                                    to_type="classical_plural"), 
            **{"tag": noun.tag}
        })
        self.optionally_add_pattern(self.patterns["singular"], {
            **self.build_recursive(_from=noun.plur_two.word, 
                                    to=noun.sing.word, 
                                    from_type="classical_plural", 
                                    to_type="singular"), 
            **{"tag": noun.tag}
        })

    def optionally_add_pattern(self, collection, dict_to_add):
        if dict_to_add["from"] not in (pattern["from"] for pattern in collection):
            collection.append(dict_to_add)

    def optionally_add_literal(self, collection, key, word):
        # if key == "_" or word == "_":
            # return
        if key not in collection:
            collection[key] = word

    def add_words(self, noun):
        self.words.add(noun.plur_one.word)
        self.words.add(noun.plur_two.word)
        self.words.add(noun.sing.word)

    def build_recursive(self, _from: str, to: str, from_type: str, to_type: str):
        check_conditional = ""
        
        def wrap(input_string: str) -> str:
            return '{' + str(input_string) + '}'
        
        def irepl(match, input_string: str, replace: str) -> str:
            """
            Replace using indices from match
            """
            return input_string[:match.start()] + replace + input_string[match.end():]

        n = 1
        # Get list of match objects, right to left, for both _from and to
        # This way we can use match indices to replace, rather than relying on substitutions
        # which causes issues with * being both in the input and output
        from_matches = list(RECURSE_GROUPED.finditer(_from))[::-1]
        to_matches   = list(RECURSE_GROUPED.finditer(to))[::-1]
        if len(from_matches) != len(to_matches):
            # TODO: Write exception
            raise Exception()

        n = len(from_matches)
        # Iterate over all matches right to left
        for from_match, to_match in zip(from_matches, to_matches):
            if from_match.group("star"):
                _from = irepl(from_match, _from, r"(.*?)")
                to    = irepl(to_match, to, wrap(f'match.group({n})'))
            
            elif from_match.group("sing"):
                _from = irepl(from_match, _from, r"(.*?)")
                to    = irepl(to_match, to, wrap(f"convert_to_{to_type}(match.group({n})) if is_singular(match.group({n})) else match.group({n})"))
                if not check_conditional:
                    check_conditional = f"lambda match: is_singular(match.group({n}))"

            elif from_match.group("plur"):
                _from = irepl(from_match, _from, r"(.*?)")
                to    = irepl(to_match, to, wrap(f"convert_to_{to_type}(match.group({n})) if is_plural(match.group({n})) else match.group({n})"))
                if not check_conditional:
                    check_conditional = f"lambda match: is_plural(match.group({n}))"

            elif from_match.group("prep"):
                _from=irepl(from_match, _from, r"(about|above|across|after|among|around|athwart|at|before|behind|below|beneath|besides?|between|betwixt|beyond|but|by|during|except|for|from|into|in|near|off|of|onto|on|out|over|since|till|to|under|until|unto|upon|with)")
                to    = irepl(to_match, to, wrap(f'match.group({n})'))

            n -= 1
        
        return {
            "from": _from,
            "to": f'lambda match: f"{to}"',
            "check_conditional": check_conditional
        }

    """
    def parse_file(self):
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
    """

def get_cases(words):
    final_words = words.copy()
    prepositions = ["about", "above", "across", "after", "among", "around", "athwart", "at", "before", "behind", "below", "beneath", "beside", "besides", "between", "betwixt", "beyond", "but", "by", "during", "except", "for", "from", "into", "in", "near", "off", "of", "onto", "on", "out", "over", "since", "till", "to", "under", "until", "unto", "upon", "with"]
    for word in words:
        if not word:
            continue
        final_words.add(word.title())
        final_words.add(word.upper())
        final_words.add(word.lower())
        final_words.add(''.join(random.choice((str.upper, str.lower))(c) for c in word))
        final_words.add(f"{random.choice(prepositions)} {word}")
    return final_words

if __name__ == "__main__":
    random.seed(0)
    in_fname = "lei//nouns.lei"
    out_fname = "inflexion//noun_core.py"
    out_import = "noun_core"

    reader = Reader(in_fname)
    reader.parse_file()

    # Words from noun.py rather than nouns.lei
    words = {'oneselves', 'he', 'mine', 'whosesoever', 'she', 'we', 'these', 'whosoever', 'him', 'theirs', 'me', 'myself', 'this', "one's", 'those', 'herself', 'whom', 'it', 'ours', 'whomever', 'some', 'us', 'whomsoever', 'I', 'oneself', 'yourself', 'that', 'you', 'one', 'yourselves', 'whose', 'yours', 'hers', 'themselves', 'himself', 'her', 'who', 'ourselves', 'his', 'whosever', 'its', 'itself', 'they', 'them', 'whoever'}

    with open(f"compare/words/nouns.txt", "w+") as f:
        words = get_cases(words.union(reader.words))
        f.write("\n".join(sorted(word for word in words if word)))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, json
from datetime import datetime
from typing import List, Tuple, Optional

from generate_tests import TestWriter

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
xms  = re.VERBOSE | re.MULTILINE | re.DOTALL
COMMENT_LINE_PAT = re.compile(r" \A \s* \#",         flags=xms)
COMMENT_PAT      = re.compile(r" \# .* ",            flags=xms)
BLANK_LINE_PAT   = re.compile(r" \A \s* $ ",         flags=xms)
WS               = re.compile(r" [\s]* ",            flags=xms)
DATA_PAT         = re.compile(r"""
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
RECURSE  = re.compile(r"\(SING\) | \(PREP\)", flags=xms)
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
DASH     = re.compile(r"-")
STAR     = re.compile(r"\*")
RESTRICT = re.compile(r"( \[.*?\] )+", flags=xms)
"""
SPLIT    = re.compile(r"(.*?) [|] (.*)", flags=xms)
"""

class Word(object):
    def __init__(self, gen: Optional[str], word: Optional[str]):
        super().__init__()
        self.gen      = gen or ""
        self.word     = word or ""
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
        self.tag      = match.group(1) or ""
        self.sing     = Word(match.group(2), match.group(3))
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
        #return (f"<{self.tag}> " if self.tag else "") + f"{self.sing}: {self.plur_one} | "
        return "{: <14} : {: <20} => {: <20} | {: <20}".format(self.tag or "", 
                                                              str(self.sing), 
                                                              str(self.plur_one) if self.plur_one.word else "", 
                                                              str(self.plur_two) if self.plur_two.word else "")

class Reader(object):
    def __init__(self, fname: str):
        types = ["modern_plural", "classical_plural", "singular"]
        self.patterns = {key:[] for key in types}
        self.literals = {key:{} for key in types}
        self.words    = {
            "plural": set(),
            "singular": set()
        }
        self.fname    = fname

    def get_readlines(self) -> List[str]:
        with open(self.fname, "r") as f: 
            return f.readlines()

    def parse_file(self):
        """
        Fill `pattern`, `literal` and `words`
        """

        # Add conversions for possessives
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
                self.patterns["modern_plural"].append({ 
                    "from": f"({noun.sing.gen}{noun.sing.restrict}){noun.sing.word}", 
                    "to": 'lambda match: f"{match.group(1)}' + f'{noun.plur_one.word}"', 
                    #"conditional": "lambda match: True",
                    "tag": noun.tag
                })
                self.patterns["singular"].append({ 
                    "from": f"({noun.sing.gen}{noun.plur_one.restrict}){noun.plur_one.word}", 
                    "to": 'lambda match: f"{match.group(1)}' + f'{noun.sing.word}"',
                    #"conditional": "lambda match: True",
                    "tag": noun.tag 
                })

                if noun.plur_two.word:
                    self.patterns["classical_plural"].append({ 
                        "from": f"({noun.sing.gen}{noun.sing.restrict}){noun.sing.word}", 
                        "to": 'lambda match: f"{match.group(1)}' + f'{noun.plur_two.word}"', 
                        #"conditional": "lambda match: True",
                        "tag": noun.tag 
                    })
                    self.patterns["singular"].append({ 
                        "from": f"({noun.sing.gen}{noun.plur_two.restrict}){noun.plur_two.word}", 
                        "to": 'lambda match: f"{match.group(1)}' + f'{noun.sing.word}"', 
                        #"conditional": "lambda match: True",
                        "tag": noun.tag 
                    })
                else:
                    self.patterns["classical_plural"].append({ 
                        "from": f"({noun.sing.gen}{noun.sing.restrict}){noun.sing.word}", 
                        "to": 'lambda match: f"{match.group(1)}' + f'{noun.plur_one.word}"', 
                        #"conditional": "lambda match: True",
                        "tag": noun.tag 
                    })

            elif RECURSE.search(noun.sing.word):
                self.add_recurse_patterns(noun)

                if noun.has_hyphen():
                    noun.replace_hyphens(" ")
                    self.add_recurse_patterns(noun)

                # TODO: Investigate this setting to 1
                noun.plur_one.gen = 1
            
            if not noun.plur_one.gen:
                self.add_literals(noun)
                self.add_words(noun)

                if noun.has_hyphen():
                    noun.replace_hyphens(" ")
                    self.add_literals(noun)
                    self.add_words(noun) 

    def add_recurse_patterns(self, noun):
        self.patterns["modern_plural"].append({
            **self.build_recursive(_from=noun.sing.word, 
                                    to=noun.plur_one.word, 
                                    from_type="singular", 
                                    to_type="modern_plural"), 
            **{"tag": noun.tag}
        })
        self.patterns["singular"].append({
            **self.build_recursive(_from=noun.plur_one.word, 
                                    to=noun.sing.word, 
                                    from_type="modern_plural", 
                                    to_type="singular"), 
            **{"tag": noun.tag}
        })

        if not noun.plur_two.word:
            noun.plur_two = noun.plur_one
        
        self.patterns["classical_plural"].append({
            **self.build_recursive(_from=noun.sing.word, 
                                    to=noun.plur_two.word, 
                                    from_type="singular", 
                                    to_type="classical_plural"), 
            **{"tag": noun.tag}
        })
        self.patterns["singular"].append({
            **self.build_recursive(_from=noun.plur_two.word, 
                                    to=noun.sing.word, 
                                    from_type="classical_plural", 
                                    to_type="singular"), 
            **{"tag": noun.tag}
        })

    def add_literals(self, noun):
        if not noun.plur_two.word:
            noun.plur_two = noun.plur_one

        self.literals["modern_plural"][noun.sing.word] = noun.plur_one.word
        self.literals["classical_plural"][noun.sing.word] = noun.plur_two.word
        self.literals["singular"][noun.plur_one.word] = noun.sing.word
        self.literals["singular"][noun.plur_two.word] = noun.sing.word

    def add_words(self, noun):
        self.words["plural"].add(noun.plur_one.word)
        self.words["plural"].add(noun.plur_two.word)
        self.words["singular"].add(noun.sing.word)

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

class CodeWriter(object):
    def __init__(self, reader, fname):
        super().__init__()
        self.reader = reader
        self.fname = fname
    
    def write_file(self):
        version = datetime.strftime(datetime.now(), '%Y%m%d.%H%M%S')
        generated_code = f'''\
#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
## NOTE: This module was autogenerated. ##
## Contains no user-servicable parts!!! ##
##########################################

import re

VERSION = {version}

def rei(regex):
    """
    Return compiled regular expression object with 
    pattern `regex` and the IGNORECASE flag.
    """
    return re.compile(regex, flags=re.I)

'''

        for key in self.reader.literals:
            generated_code += f"{key}_of = " + json.dumps(reader.literals[key], indent=4, sort_keys=True) + "\n\n" 
        
        for key in self.reader.literals:
            generated_code += self.get_convert_rule_output(key, self.reader.patterns[key]) + "\n\n"
        
        generated_code += self.get_recognize_rule_output("plural", self.reader.patterns["singular"]) + "\n\n"
        generated_code += self.get_recognize_rule_output("singular", self.reader.patterns["modern_plural"] + self.reader.patterns["classical_plural"]) + "\n\n"
        
        generated_code += """def known_plural(word):
    return word in modern_plural_of.values() or\\
        word in classical_plural_of.values() or\\
        word in singular_of.keys()

def known_singular(word):
    return word in singular_of.values() or\\
        word in modern_plural_of.keys() or\\
        word in classical_plural_of.keys()

"""

        for key in self.reader.literals:
            generated_code += self.get_converter_output(key, self.reader.patterns[key]) + "\n\n"

        generated_code += self.get_recognizer_output("plural", "singular") + "\n\n"
        generated_code += self.get_recognizer_output("singular", "plural") + "\n\n"

        generated_code += """\
if __name__ == "__main__":
    breakpoint()
"""

        self.output_code(generated_code)

    def output_code(self, generated_code):
        with open(self.fname, "w+") as f:
            f.write(generated_code)

    def get_convert_rule_output(self, name, replacement_suffixes):
        output = name + "_convert_rules = {\n"
        used_lines = []
        for replacement_dict in replacement_suffixes:
            line = f'    rei(r"{replacement_dict["from"]}$"): '
            # Add a non-empty conditional if it exists
            if "conv_conditional" in replacement_dict and replacement_dict["conv_conditional"]:
                line += "{\n" + f'        "conditional": {replacement_dict["conv_conditional"]},\n        '
            else:
                line += "{"
            line += f'"output": {replacement_dict["to"]}'
            if "conv_conditional" in replacement_dict and replacement_dict["conv_conditional"]:
                line += '\n    '
            line += "},\n"
            # Don't repeat lines
            if line not in used_lines:
                used_lines.append(line)
                output += line
        output += "}"
        return output

    def get_converter_output(self, name, replacement_suffixes):
        _type = "plural" if "plural" in name else "singular"
        _extra_check = " and not known_singular(word)" if _type == "plural" else ""

        output = f"""def convert_to_{name}(word, verbose=False):
    if word in {name}_of:
        if verbose: print(word, 'in {name}_of')
        return {name}_of[word]
    if word.lower() in {name}_of:
        if verbose: print(word.lower(), 'in {name}_of')
        return {name}_of[word.lower()]
    if known_{_type}(word){_extra_check}:
        if verbose: print('known_{_type}(word){_extra_check}')
        return word
    for rule in {name}_convert_rules:
        match = rule.match(word)
        if match:
            if verbose: print(word, 'matched', rule.pattern)
            # If there is no conditional, or if the condition succeeds
            if not "conditional" in {name}_convert_rules[rule] or {name}_convert_rules[rule]["conditional"](match):
                if verbose: print(word, 'passed the conditional, or there was no conditional')
                return {name}_convert_rules[rule]["output"](match)
            else:
                if verbose: print(word, 'failed the conditional')
    return word"""
        return output

    def get_recognize_rule_output(self, name, replacement_suffixes):
        output = name + "_recognize_rules = {\n"
        used_lines = []
        for replacement_dict in replacement_suffixes:
            if replacement_dict["tag"] == "nonindicative":
                continue
            line = f'    rei(r"{replacement_dict["from"]}$"): '
            # Add a non-empty conditional if it exists
            if "check_conditional" in replacement_dict and replacement_dict["check_conditional"]:
                line += "{" + f'"conditional": {replacement_dict["check_conditional"]}' + "},\n"
            else:
                line += "{},\n"
            # Don't repeat lines
            if line not in used_lines:
                used_lines.append(line)
                output += line
        output += "}"
        return output

    def get_recognizer_output(self, name, compl_name):
        output = f"""def is_{name}(word, verbose=False):
    if known_{name}(word) or known_{name}(word.lower()):
        if verbose: print('known_{name}(word)')
        return True"""
        if compl_name:
            output += f"""
    if known_{compl_name}(word) or known_{compl_name}(word.lower()):
        if verbose: print('known_{compl_name}(word)')
        return False
    for rule in {name}_recognize_rules:
        match = rule.match(word)
        if match:
            if verbose: print(word, 'matched', rule.pattern)
            if not "conditional" in {name}_recognize_rules[rule] or {name}_recognize_rules[rule]["conditional"](match):
                if verbose: print(word, 'passed the conditional, or there was no conditional')
                return True
            else:
                if verbose: print(word, 'failed the conditional')
    if verbose: print("Matched no rules")"""
        if name == "singular":
            output += "\n    return not is_plural(word)"
        else:
            output += "\n    return word.strip().endswith('s')"
        return output

class NounTestWriter(TestWriter):
    def __init__(self, reader, out_fname):
        super().__init__(out_fname)
        self.reader = reader
        """
        For each test case we need the following information to be passed to the format:
        import_fname:       Equivalent to out_fname, already known as self.import_fname
        test_function:      Name of function to test.
        test_args:          List of dictionaries with testing arguments.
        test_name_pascal:   Name of the test in Pascal Case
        """
    
    def write_tests(self):
        self.write_is_singular_test()
        self.write_is_plural_test()

        self.write_to_singular_test()
        self.write_to_modern_plural_test()
        self.write_to_classical_plural_test()

    def write_is_singular_test(self):
        test_path = self.test_folder_name + "//test_noun_core_is_singular.py"
        test_function = "is_singular"
        test_name_pascal = "NounIsSingular"
        test_args = [
            {
                "in": word,
                "out": True
            } for word in self.reader.words["singular"]
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_is_plural_test(self):
        test_path = self.test_folder_name + "//test_noun_core_is_plural.py"
        test_function = "is_plural"
        test_name_pascal = "NounIsPlural"
        test_args = [
            {
                "in": word,
                "out": True
            } for word in self.reader.words["plural"]
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_to_singular_test(self):
        test_path = self.test_folder_name + "//test_noun_core_to_singular.py"
        test_function = "convert_to_singular"
        test_name_pascal = "NounToSingular"
        test_args = [
            {
                "in": plur,
                "out": sing
            } for plur, sing in self.reader.literals["singular"].items()
        ]
        test_args += [
            {
                "in": sing,
                "out": sing
            } for sing in self.reader.literals["singular"].values()
            if sing not in self.reader.words["plural"]
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_to_modern_plural_test(self):
        test_path = self.test_folder_name + "//test_noun_core_to_modern_plural.py"
        test_function = "convert_to_modern_plural"
        test_name_pascal = "NounToModernPlural"
        test_args = [
            {
                "in": sing,
                "out": plur
            } for sing, plur in self.reader.literals["modern_plural"].items()
        ]
        test_args += [
            {
                "in": plur,
                "out": plur
            } for plur in self.reader.literals["modern_plural"].values()
            if plur not in self.reader.words["singular"]
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_to_classical_plural_test(self):
        test_path = self.test_folder_name + "//test_noun_core_to_classical_plural.py"
        test_function = "convert_to_classical_plural"
        test_name_pascal = "NounToClassicalPlural"
        test_args = [
            {
                "in": sing,
                "out": plur
            } for sing, plur in self.reader.literals["classical_plural"].items()
        ]
        test_args += [
            {
                "in": plur,
                "out": plur
            } for plur in self.reader.literals["classical_plural"].values()
            if plur not in self.reader.words["singular"]
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

if __name__ == "__main__":    
    in_fname = "lei//nouns.lei"
    out_fname = "src//noun_core.py"
    out_import = "src.noun_core"

    reader = Reader(in_fname)
    reader.parse_file()

    cwriter = CodeWriter(reader, out_fname)
    cwriter.write_file()

    twriter = NounTestWriter(reader, out_import)
    twriter.write_tests()
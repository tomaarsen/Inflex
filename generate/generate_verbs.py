#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, json
from datetime import datetime
from typing import List, Tuple, Optional

from generate_tests import TestWriter

"""
Compiled variants of useful regexes used all around this file
"""
xms  = re.VERBOSE | re.MULTILINE | re.DOTALL
COMMENT_LINE_PAT = re.compile(r" \A \s* \#",         flags=xms)
COMMENT_PAT      = re.compile(r" \# .* ",            flags=xms)
BLANK_LINE_PAT   = re.compile(r" \A \s* $ ",         flags=xms)
WS               = re.compile(r" [\s]* ",            flags=xms)
WORD_SEQ         = re.compile(r" \S* (?: \s \S+)* ", flags=xms)
DATA_PAT         = re.compile(r"""
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
CONS     = re.compile(r"\(CONS\)", flags=xms)
VOWEL    = re.compile(r"\(VOWEL\)", flags=xms)
VOWELY   = re.compile(r"\(VOWELY\)", flags=xms)
DASH     = re.compile(r"-")
STAR     = re.compile(r"\*")
RESTRICT = re.compile(r"( \[.*?\] )+", flags=xms)
SPLIT    = re.compile(r"(.*?) [|] (.*)", flags=xms)

class Word(object):
    def __init__(self, gen: Optional[str], word: str):
        super().__init__()
        self.gen      = gen
        self.word     = word
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
            gen  = match.group(i * 2 + 1)
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
        self.patterns = {key:[] for key in types}
        self.literals = {key:{} for key in types}
        self.words    = {key:set() for key in types}
        self.fname    = fname

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
            
            if verb.has_gen():
                self.patterns["plural"].append({
                    "is": f"({verb.plur.gen}{verb.plur.restrict}){verb.plur.word}",
                    "from": f"(.*{verb.sing.restrict}){verb.sing.word}",
                    "to": 'lambda match: f"{match.group(1)}' + f'{verb.plur.word}"' 
                })
                self.patterns["singular"].append({
                    "is": f"({verb.sing.gen}{verb.sing.restrict}){verb.sing.word}",
                    "from": f"(.*{verb.plur.restrict}){verb.plur.word}",
                    "to": 'lambda match: f"{match.group(1)}' + f'{verb.sing.word}"'
                })
                if verb.pret.word != "_":
                    self.patterns["past"].append({
                        "is": f"({verb.pret.gen}{verb.pret.restrict}){verb.pret.word}",
                        "from": f"(.*{verb.sing.restrict}){verb.sing.word}",
                        "to": 'lambda match: f"{match.group(1)}' + f'{verb.pret.word}"'
                    })
                    self.patterns["past"].append({
                        "from": f"(.*{verb.plur.restrict}){verb.plur.word}",
                        "to": 'lambda match: f"{match.group(1)}' + f'{verb.pret.word}"'
                    })
                if verb.pres.word != "_":
                    self.patterns["pres_part"].append({
                        "is": f"({verb.pres.gen}{verb.pres.restrict}){verb.pres.word}",
                        "from": f"(.*{verb.sing.restrict}){verb.sing.word}",
                        "to": 'lambda match: f"{match.group(1)}' + f'{verb.pres.word}"'
                    })
                    self.patterns["pres_part"].append({
                        "from": f"(.*{verb.plur.restrict}){verb.plur.word}",
                        "to": 'lambda match: f"{match.group(1)}' + f'{verb.pres.word}"'
                    })
                if verb.past.word != "_":
                    self.patterns["past_part"].append({
                        "is": f"({verb.past.gen}{verb.past.restrict}){verb.past.word}",
                        "from": f"(.*{verb.sing.restrict}){verb.sing.word}",
                        "to": 'lambda match: f"{match.group(1)}' + f'{verb.past.word}"'
                    })
                    self.patterns["past_part"].append({
                        "from": f"(.*{verb.plur.restrict}){verb.plur.word}",
                        "to": 'lambda match: f"{match.group(1)}' + f'{verb.past.word}"'
                    })
            
            if not (verb.sing.gen and verb.plur.gen and verb.pret.gen):
                self.add_literals_and_words(verb)

                # If there is a hyphen in the singular verb, replace the hyphens
                # in all verbs, and add those to the literals and words too
                if "-" in verb.sing.word:
                    verb.replace_hyphens(" ")
                    self.add_literals_and_words(verb)

    def add_literals_and_words(self, verb):
        self.literals["plural"][verb.sing.word]   = verb.plur.word
        self.literals["singular"][verb.plur.word] = verb.sing.word

        self.words["singular"].add(verb.sing.word)
        self.words["plural"].add(verb.plur.word)
    
        if verb.pret.word:
            self.words["past"].add(verb.pret.word)

            self.literals["past"][verb.sing.word] = verb.pret.word
            self.literals["past"][verb.past.word] = verb.pret.word
            self.literals["past"][verb.pres.word] = verb.pret.word
            self.literals["past"][verb.past.word] = verb.pret.word

            if verb.pret_plur:
                self.literals["past"][verb.plur.word] = verb.pret_plur
                self.words["past"].add(verb.pret_plur)
            else:
                self.literals["past"][verb.plur.word] = verb.pret.word
        
        if verb.pres.word:
            self.words["pres_part"].add(verb.pres.word)

            self.literals["pres_part"][verb.sing.word] = verb.pres.word
            self.literals["pres_part"][verb.plur.word] = verb.pres.word
            self.literals["pres_part"][verb.pret.word] = verb.pres.word
            self.literals["pres_part"][verb.pres.word] = verb.pres.word
            self.literals["pres_part"][verb.past.word] = verb.pres.word

        if verb.past.word:
            self.words["past_part"].add(verb.past.word)

            self.literals["past_part"][verb.sing.word] = verb.past.word
            self.literals["past_part"][verb.plur.word] = verb.past.word
            self.literals["past_part"][verb.pret.word] = verb.past.word
            self.literals["past_part"][verb.pres.word] = verb.past.word
            self.literals["past_part"][verb.past.word] = verb.past.word

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
        
        for key in self.reader.literals:
            generated_code += self.get_recognize_rule_output(key, self.reader.patterns[key]) + "\n\n"
        
        generated_code += """\
def known_plural(word):
    return word in plural_of.values() or\\
        word in singular_of.keys() or\\
        word in past_of.values() or\\
        word in pres_part_of.values() or\\
        word in past_part_of.values()

def known_singular(word):
    return word in singular_of.values() or\\
        word in plural_of.keys() or\\
        word in past_of.values() or\\
        word in pres_part_of.values() or\\
        word in past_part_of.values()

def known_past(word):
    return word in past_of.values()

def known_past_part(word):
    return word in past_part_of.values()

def known_pres_part(word):
    return word in pres_part_of.values()

"""

        for key in self.reader.literals:
            generated_code += self.get_converter_output(key, self.reader.patterns[key]) + "\n\n"

        generated_code += self.get_recognizer_output("plural", "singular", self.reader.literals["plural"]) + "\n\n"
        generated_code += self.get_recognizer_output("singular", "plural", self.reader.literals["singular"]) + "\n\n"
        generated_code += self.get_recognizer_output("past", None, self.reader.literals["past"]) + "\n\n"
        generated_code += self.get_recognizer_output("pres_part", None, self.reader.literals["pres_part"]) + "\n\n"
        generated_code += self.get_recognizer_output("past_part", None, self.reader.literals["past_part"]) + "\n"

        self.output_code(generated_code)

    def output_code(self, generated_code):
        with open(self.fname, "w+") as f:
            f.write(generated_code)

    def get_convert_rule_output(self, name, replacement_suffixes):
        output = name + "_convert_rules = {\n"
        for replacement_dict in replacement_suffixes:
            output += f'    rei("{replacement_dict["from"]}$"): {replacement_dict["to"]},\n'
        output += "}"
        return output

    def get_converter_output(self, name, replacement_suffixes):
        output = f"""\
def convert_to_{name}(word):
    if word in {name}_of:
        return {name}_of[word]
    if word.lower() in {name}_of:
        return {name}_of[word.lower()]
    if known_{name}(word):
        return word
    for rule in {name}_convert_rules:
        match = rule.match(word)
        if match:
            return {name}_convert_rules[rule](match)
    return '_'"""
        return output

    def get_recognize_rule_output(self, name, replacement_suffixes):
        output = name + "_recognize_rules = [\n"
        for replacement_dict in replacement_suffixes:
            if "is" in replacement_dict:
                output += f'    rei("{replacement_dict["is"]}$"),\n'
        output += "]"
        return output

    def get_recognizer_output(self, name, compl_name, replacement_suffixes):
        output = f"""\
def is_{name}(word):
    if known_{name}(word) or known_{name}(word.lower()):
        return True"""
        if compl_name:
            output += f"""
    if known_{compl_name}(word) or known_{compl_name}(word.lower()):
        return False"""
        output += f"""
    for rule in {name}_recognize_rules:
        if rule.match(word):
            return True
"""
        if name == "singular":
            output += "    return not is_plural(word)"
        else:
            output += "    return False"
        return output

class VerbTestWriter(TestWriter):
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
        # Ignore "am", "is" and "are" for these tests
        self.reader.words["plural"] -= {"am", "is", "are"}
        self.reader.words["singular"] -= {"am", "is", "are"}
        
        self.write_is_singular_test()
        self.write_is_plural_test()
        self.write_is_past_test()
        self.write_is_pres_part_test()
        self.write_is_past_part_test()

        self.write_to_singular_test()
        self.write_to_plural_test()
        self.write_to_past_test()
        self.write_to_pres_part_test()
        self.write_to_past_part_test()

    def write_is_singular_test(self):
        """
        Note, only tests whether `is_singular` detects that known singular 
        words are indeed singular
        """
        test_path = self.test_folder_name + "//test_verb_core_is_singular.py"
        test_function = "is_singular"
        test_name_pascal = "VerbIsSingular"
        test_args = [
            {
                "in": word,
                "out": True
            } for word in self.reader.words["singular"]
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_is_plural_test(self):
        """
        Note, only tests whether `is_plural` detects that known plural 
        words are indeed plural
        """
        test_path = self.test_folder_name + "//test_verb_core_is_plural.py"
        test_function = "is_plural"
        test_name_pascal = "VerbIsPlural"
        test_args = [
            {
                "in": word,
                "out": True
            } for word in self.reader.words["plural"]
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_is_past_test(self):
        """
        Note, only tests whether `is_past` detects that known past 
        words are indeed past
        """
        test_path = self.test_folder_name + "//test_verb_core_is_past.py"
        test_function = "is_past"
        test_name_pascal = "VerbIsPast"
        test_args = [
            {
                "in": word,
                "out": True
            } for word in self.reader.words["past"]
            if word and word != "_"
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_is_pres_part_test(self):
        """
        Note, only tests whether `is_pres_part` detects that known present participle 
        words are indeed present participles
        """
        test_path = self.test_folder_name + "//test_verb_core_is_pres_part.py"
        test_function = "is_pres_part"
        test_name_pascal = "VerbIsPresPart"
        test_args = [
            {
                "in": word,
                "out": True
            } for word in self.reader.words["pres_part"]
            if word and word != "_"
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_is_past_part_test(self):
        """
        Note, only tests whether `is_past_part` detects that known past participle 
        words are indeed past participles
        """
        test_path = self.test_folder_name + "//test_verb_core_is_past_part.py"
        test_function = "is_past_part"
        test_name_pascal = "VerbIsPastPart"
        test_args = [
            {
                "in": word,
                "out": True
            } for word in self.reader.words["past_part"]
            if word and word != "_"
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_to_singular_test(self):
        test_path = self.test_folder_name + "//test_verb_core_to_singular.py"
        test_function = "convert_to_singular"
        test_name_pascal = "VerbToSingular"
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

    def write_to_plural_test(self):
        test_path = self.test_folder_name + "//test_verb_core_to_plural.py"
        test_function = "convert_to_plural"
        test_name_pascal = "VerbToPlural"
        test_args = [
            {
                "in": sing,
                "out": plur
            } for sing, plur in self.reader.literals["plural"].items()
        ]
        test_args += [
            {
                "in": plur,
                "out": plur
            } for plur in self.reader.literals["plural"].values()
            if plur not in self.reader.words["singular"]
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_to_past_test(self):
        test_path = self.test_folder_name + "//test_verb_core_to_past.py"
        test_function = "convert_to_past"
        test_name_pascal = "VerbToPast"
        test_args = [
            {
                "in": verb,
                "out": past
            } for verb, past in self.reader.literals["past"].items()
            if verb and past != "_"
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_to_pres_part_test(self):
        test_path = self.test_folder_name + "//test_verb_core_to_pres_part.py"
        test_function = "convert_to_pres_part"
        test_name_pascal = "VerbToPresPart"
        test_args = [
            {
                "in": verb,
                "out": pres_part
            } for verb, pres_part in self.reader.literals["pres_part"].items()
            if verb and pres_part != "_"
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

    def write_to_past_part_test(self):
        test_path = self.test_folder_name + "//test_verb_core_to_past_part.py"
        test_function = "convert_to_past_part"
        test_name_pascal = "VerbToPastPart"
        test_args = [
            {
                "in": verb,
                "out": past_part
            } for verb, past_part in self.reader.literals["past_part"].items()
            if verb and past_part != "_"
        ]
        self.write_test(test_path, test_function, test_name_pascal, test_args)

if __name__ == "__main__":    
    in_fname = "lei//verbs.lei"
    out_fname = "inflexion//verb_core.py"
    out_import = "verb_core"
    reader = Reader(in_fname)
    reader.parse_file()
    
    cwriter = CodeWriter(reader, out_fname)
    cwriter.write_file()
    
    twriter = VerbTestWriter(reader, out_import)
    twriter.write_tests()

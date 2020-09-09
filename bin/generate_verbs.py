#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, json
from datetime import datetime
from typing import List, Tuple, Optional

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
        types = ["plur", "sing", "pret", "pres", "past"]
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
        """
        return f"Singular        : {self.sing_gen or ''}{self.sing_restrict}{self.sing}\n"\
               f"Plural          : {self.plur_gen or ''}{self.plur_restrict}{self.plur}\n"\
               f"Preterite       : {self.pret_gen or ''}{self.pret_restrict}{self.pret}\n"\
               f"Pres participle : {self.pres_gen or ''}{self.pres_restrict}{self.pres}\n"\
               f"Past participle : {self.past_gen or ''}{self.past_restrict}{self.past}\n"
        """

class Reader(object):
    def __init__(self, fname: str):
        types = ["plural", "singular", "past", "pres_part", "past_part"]
        self.patterns = {key:[] for key in types}
        self.literals = {key:{} for key in types}
        self.words    = {key:[] for key in types}
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
                    "to": "{}" + verb.plur.word
                })
                self.patterns["singular"].append({
                    "is": f"({verb.sing.gen}{verb.sing.restrict}){verb.sing.word}",
                    "from": f"(.*{verb.plur.restrict}){verb.plur.word}",
                    "to": "{}" + verb.sing.word
                })
                if verb.pret.word != "_":
                    self.patterns["past"].append({
                        "is": f"({verb.pret.gen}{verb.pret.restrict}){verb.pret.word}",
                        "from": f"(.*{verb.sing.restrict}){verb.sing.word}",
                        "to": "{}" + verb.pret.word
                    })
                    self.patterns["past"].append({
                        "from": f"(.*{verb.plur.restrict}){verb.plur.word}",
                        "to": "{}" + verb.pret.word
                    })
                if verb.pres.word != "_":
                    self.patterns["pres_part"].append({
                        "is": f"({verb.pres.gen}{verb.pres.restrict}){verb.pres.word}",
                        "from": f"(.*{verb.sing.restrict}){verb.sing.word}",
                        "to": "{}" + verb.pres.word
                    })
                    self.patterns["pres_part"].append({
                        "from": f"(.*{verb.plur.restrict}){verb.plur.word}",
                        "to": "{}" + verb.pres.word
                    })
                if verb.past.word != "_":
                    self.patterns["past_part"].append({
                        "is": f"({verb.past.gen}{verb.past.restrict}){verb.past.word}",
                        "from": f"(.*{verb.sing.restrict}){verb.sing.word}",
                        "to": "{}" + verb.past.word
                    })
                    self.patterns["past_part"].append({
                        "from": f"(.*{verb.plur.restrict}){verb.plur.word}",
                        "to": "{}" + verb.past.word
                    })
            
            if not (verb.sing.gen and verb.plur.gen and verb.pret.gen):
                self.literals["plural"][verb.sing.word]   = verb.plur.word
                self.literals["singular"][verb.plur.word] = verb.sing.word

                self.words["singular"].append(verb.sing.word)
                self.words["plural"].append(verb.plur.word)
            
                if verb.pret.word:
                    self.words["past"].append(verb.pret.word)

                    self.literals["past"][verb.sing.word] = verb.pret.word
                    self.literals["past"][verb.past.word] = verb.pret.word
                    self.literals["past"][verb.pres.word] = verb.pret.word
                    self.literals["past"][verb.past.word] = verb.pret.word

                    if verb.pret_plur:
                        self.literals["past"][verb.plur.word] = verb.pret_plur
                        self.words["past"].append(verb.pret_plur)
                    else:
                        self.literals["past"][verb.plur.word] = verb.pret.word
                
                if verb.pres.word:
                    self.words["pres_part"].append(verb.pres.word)

                    self.literals["pres_part"][verb.sing.word] = verb.pres.word
                    self.literals["pres_part"][verb.plur.word] = verb.pres.word
                    self.literals["pres_part"][verb.pret.word] = verb.pres.word
                    self.literals["pres_part"][verb.pres.word] = verb.pres.word
                    self.literals["pres_part"][verb.past.word] = verb.pres.word

                if verb.past.word:
                    self.words["past_part"].append(verb.pres.word)

                    self.literals["past_part"][verb.sing.word] = verb.past.word
                    self.literals["past_part"][verb.plur.word] = verb.past.word
                    self.literals["past_part"][verb.pret.word] = verb.past.word
                    self.literals["past_part"][verb.pres.word] = verb.past.word
                    self.literals["past_part"][verb.past.word] = verb.past.word

            # TODO: Investigate redo

class Writer(object):
    def __init__(self, reader, fname):
        super().__init__()
        self.reader = reader
        self.fname = fname
    
    def write_file(self):
        version = datetime.strftime(datetime.now(), '%Y%m%d.%H%M%S')
        generated_code = f"""\
#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
## NOTE: This module was autogenerated. ##
## Contains no user-servicable parts!!! ##
##########################################

import re

VERSION = {version}

"""

        for key in self.reader.literals:
            generated_code += f"{key}_of = " + json.dumps(reader.literals[key], indent=4, sort_keys=True) + "\n\n" 
        
        for key in self.reader.literals:
            generated_code += self.get_convert_rule_output(key, self.reader.patterns[key]) + "\n\n"
        
        for key in self.reader.literals:
            generated_code += self.get_recognize_rule_output(key, self.reader.patterns[key]) + "\n\n"
        
        generated_code += """def known_plural(word):
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
            output += f'    re.compile("{replacement_dict["from"]}$", flags=re.I): "{replacement_dict["to"]}",\n'
        output += "}"
        return output

    def get_converter_output(self, name, replacement_suffixes):
        output = f"""def convert_to_{name}(word):
    if word in {name}_of:
        return {name}_of[word]
    if word.lower() in {name}_of:
        return {name}_of[word.lower()]
    if known_{name}(word):
        return word
    for rule in {name}_convert_rules:
        if rule.match(word):
            return {name}_convert_rules[rule]
    return '_'"""
        return output

    def get_recognize_rule_output(self, name, replacement_suffixes):
        output = name + "_recognize_rules = [\n"
        for replacement_dict in replacement_suffixes:
            if "is" in replacement_dict:
                output += f'    re.compile("{replacement_dict["is"]}$", flags=re.I),\n'
        output += "]"
        return output

    def get_recognizer_output(self, name, compl_name, replacement_suffixes):
        output = f"""def is_{name}(word):
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
            output += "return not is_plural(word)"
        else:
            output += "return False"
        return output

    def write_tests(self):
        pass

if __name__ == "__main__":    
    in_fname = "..//verbs.lei"
    out_fname = "..//verb_output.py"
    reader = Reader(in_fname)
    reader.parse_file()
    writer = Writer(reader, out_fname)
    writer.write_file()
    writer.write_tests()

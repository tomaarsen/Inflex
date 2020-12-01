#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from typing import Union
sys.path.insert(0, os.path.join(sys.path[0], '..')) 
sys.path.insert(0, os.path.join(sys.path[0], '../.')) 

from inflexion import Noun, Verb, Adjective

functions = {
    "nouns": ["is_plural", "is_singular", "plural", "singular"],
    "verbs": ["is_plural", "is_singular", "is_past", "is_pres_part", "is_past_part", "plural", "singular", "past", "pres_part", "past_part"], 
    "adjectives": ["is_plural", "is_singular", "plural", "singular"]
}
word_types = ["nouns", "verbs", "adjectives"]
classes = [Noun, Verb, Adjective]

def output(inp: Union[bool, str]):
    if isinstance(inp, bool):
        if inp:
            return "1\n"
        return "0\n"
    # If string is empty, return 0\n as the Perl file does the same
    if inp:
        return inp + "\n"
    return "0\n"

for word_type, inf_class in zip(word_types, classes):
    for func in functions[word_type]:
        f_out = open(f"compare/python_output/{word_type}/modern/{func}.txt", "w+")
        f_out_classical = open(f"compare/python_output/{word_type}/classical/{func}.txt", "w+")

        f_in = open(f"compare/words/{word_type}.txt")
        for line in f_in.readlines():
            line = line.strip()
            f_out.write(output(getattr(inf_class(line), func)()))
            f_out_classical.write(output(getattr(inf_class(line).classical(), func)()))
        
        f_in.close()
        f_out.close()
        f_out_classical.close()
    
    for arg in range(1, 4):
        for func in ["plural", "singular"]:
            f_out = open(f"compare/python_output/{word_type}/modern/{func}_{arg}.txt", "w+")
            f_out_classical = open(f"compare/python_output/{word_type}/classical/{func}_{arg}.txt", "w+")

            f_in = open(f"compare/words/{word_type}.txt")
            for line in f_in.readlines():
                line = line.strip()
                f_out.write(output(getattr(inf_class(line), func)(arg)))
                f_out_classical.write(output(getattr(inf_class(line).classical(), func)(arg)))
            
            f_in.close()
            f_out.close()
            f_out_classical.close()

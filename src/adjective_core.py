#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

# Load adjective tables, always taking first option...
adjectives = [
    # Determiners...
        ('a'      ,  'some'),
        ('an'     ,  'some'),
 
    # Demonstratives...
        ('that'   ,  'those'),
        ('this'   ,  'these'),
 
    # Possessives...
        ('my'     ,  'our'),
        ('your'   ,  'your'),
        ('their'  ,  'their'),
        ('her'    ,  'their'),
        ('his'    ,  'their'),
        ('its'    ,  'their'),
]

adj_is_singular = []
adj_is_plural   = []
adj_singular_of = {}
adj_plural_of   = {}
for sing, plur in adjectives[::-1]:
    adj_is_singular.append(sing)
    adj_singular_of[plur] = sing
    
    adj_is_plural.append(plur)
    adj_plural_of[sing] = plur

def is_plural(word):
    return word in adj_is_plural or\
           word.lower() in adj_is_plural or\
           (word not in adj_is_singular and word.lower() not in adj_is_singular)

def is_singular(word):
    return word in adj_is_singular or\
           word.lower() in adj_is_singular or\
           (word not in adj_is_plural and word.lower() not in adj_is_plural)

def convert_to_plural(word):
    if word in adj_plural_of:
        return adj_plural_of[word]
    if word.lower() in adj_plural_of:
        return adj_plural_of[word.lower()]
    return word

def convert_to_singular(word):
    if word in adj_singular_of:
        return adj_singular_of[word]
    if word.lower() in adj_singular_of:
        return adj_singular_of[word.lower()]
    return word

if __name__ == "__main__":
    breakpoint()
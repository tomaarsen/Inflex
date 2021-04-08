#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from typing import Dict, List, Set


class Syllable:

    _data = {}

    @staticmethod
    def data() -> Dict[str, List[List[float]]]:
        """
        Lazy load stress data when requested.
        """
        if Syllable._data:
            return Syllable._data

        path = os.path.join(os.path.dirname(__file__),
                            "data/cmudict_stress.json")
        with open(path, "r", encoding="utf8") as f:
            Syllable._data = json.load(f)
        return Syllable._data

    @staticmethod
    def get_stress(word: str) -> List[List[float]]:
        """
        Return list of list of stress values, e.g.
        [[1, 0, 0.5], [1, 0, 0, 0.5]]
        This shows that a word either has 3 or 4 syllables, 
        and the first syllable of either interpretation has the primary stress,
        while the last syllable of either interpretation has the secondary stress.
        The other syllables are unstressed.
        """
        try:
            return Syllable.data()[word]
        except KeyError:
            return []

    @staticmethod
    def count_syllables(word: str) -> Set[int]:
        """
        Returns the set with valid numbers of syllables in the input word.
        Note that some words have multiple valid syllable counts.
        """
        return {len(stress) for stress in Syllable.get_stress(word)}

    @staticmethod
    def ends_with_stress(word: str) -> bool:
        """
        Returns True if there is an interpretation of the input word
        that has either primary or secondary stress on the final syllable.

        TODO: Consider only True when primary stress
            NOTE: Tested - and performs marginally worse
        TODO: Consider only True when stress is on all interpretations
            NOTE: Tested - and performs marginally better
        """
        stresses = Syllable.get_stress(word)
        return all(stress[-1] > 0 for stress in stresses if stress)

    @staticmethod
    def guess_if_one_syllable(word: str) -> bool:
        """
        Guess whether the word is one Syllable, by converting letters
        to either V or C depending on if the letter is a vowel or consonant,
        respectively. Then, remove double C's and check whether the pattern
        "VCV" exists. If it does, the word likely has more than one syllable.
        """
        converted = ''.join(
            "V" if char in "aeiou" else "C" for char in word.lower())
        while "CC" in converted:
            converted = converted.replace("CC", "C")
        return "VCV" not in converted
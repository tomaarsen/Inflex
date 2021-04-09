#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from typing import Dict, List, Set


class Syllable:
    """Class with Syllable information from Carnegie Mellon University's cmudict.txt.
    This class provides several static methods which can be used to count the
    number of syllables of an input word. Another purpose is to find out whether
    the word ends with stress.
    """

    _data = {}

    @staticmethod
    def data() -> Dict[str, List[List[float]]]:
        """Lazy load syllable and stress data when requested.

        Examples:
            >>>Stress.data()
            {
                "ab": [[1], [1, 1]],
	            "ababa": [[0, 1, 0], [1, 0, 0]],
	            "abacha": [[1, 0, 0]],
                ...
            }

        Returns:
            Dict[str, List[List[float]]]: The dictionary key is a regular word, which maps
                to a list of syllable interpretations. Each interpretation is a list of stress
                values, where 1 means Primary stress, 0.5 means secondary stress,
                and 0 is unstressed.
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
        """Return a list of syllable interpretations that correspond to stress values, for `word`.

        Examples:
            >>>Stress.get_stress("abdomen")
            [[0, 1, 0], [1, 0, 0]]
            This shows that the word has two interpretations, both with 3 syllables.
            In the first interpretation, the second syllable has primary stress, while
            in the second interpretation, the first syllable has primary stress.
            The other syllables are unstressed.

        Args:
            word (str): The input word.

        Returns:
            List[List[float]]: A list of syllable interpretations that correspond to stress values,
                for `word`.
        """
        try:
            return Syllable.data()[word]
        except KeyError:
            return []

    @staticmethod
    def count_syllables(word: str) -> Set[int]:
        """Return the set of valid syllable counts of `word`.

        Note:
            Some words have multiple valid syllable counts, like "abdomen".

        Args:
            word (str): The input word.

        Returns:
            Set[int]: The set of valid syllable counts of `word`.
        """
        return {len(stress) for stress in Syllable.get_stress(word)}

    @staticmethod
    def ends_with_stress(word: str) -> bool:
        """Returns True if all syllable interpretations of `word` end with stress.

        Note:
            Either primary or secondary stress is considered stress.

        Args:
            word (str): The input word.

        Returns:
            bool: True if all syllable interpretations of `word` end with stress.
                False otherwise.
        """
        stresses = Syllable.get_stress(word)
        return all(stress[-1] > 0 for stress in stresses if stress)

    @staticmethod
    def guess_if_one_syllable(word: str) -> bool:
        """Guess whether the word is just one Syllable.

        Guessing is done by converting letters to either V or C depending on
        if the letter is a vowel or consonant, respectively.
        Then, remove double C's and check whether the pattern
        "VCV" exists. If it does, the word likely has more than one syllable.

        Args:
            word (str): The input word.

        Returns:
            bool: True if `word` is guessed to be just one syllable.
        """
        converted = ''.join(
            "V" if char in "aeiou" else "C" for char in word.lower())
        while "CC" in converted:
            converted = converted.replace("CC", "C")
        return "VCV" not in converted

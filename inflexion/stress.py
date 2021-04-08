#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from typing import Dict, List, Set


class Stress:

    _data = {}

    @staticmethod
    def data() -> Dict[str, List[List[float]]]:
        """
        Lazy load stress data when requested.
        """
        if Stress._data:
            return Stress._data

        path = os.path.join(os.path.dirname(__file__),
                            "data/cmudict_stress.json")
        with open(path, "r", encoding="utf8") as f:
            Stress._data = json.load(f)
        return Stress._data

    @staticmethod
    def get_stress(word) -> List[List[float]]:
        """
        Return list of list of stress values, e.g.
        [[1, 0, 0.5], [1, 0, 0, 0.5]]
        This shows that a word either has 3 or 4 syllables, 
        and the first syllable of either interpretation has the primary stress,
        while the last syllable of either interpretation has the secondary stress.
        The other syllables are unstressed.
        """
        try:
            return Stress.data()[word]
        except KeyError:
            return []

    @staticmethod
    def count_syllables(word) -> Set[int]:
        """
        Returns the set with valid numbers of syllables in the input word.
        Note that some words have multiple valid syllable counts.
        """
        return {len(stress) for stress in Stress.get_stress(word)}

    @staticmethod
    def ends_with_stress(word) -> bool:
        """
        Returns True if there is an interpretation of the input word
        that has either primary or secondary stress on the final syllable.

        TODO: Consider only True when primary stress
            NOTE: Tested - and performs marginally worse
        TODO: Consider only True when stress is on all interpretations
            NOTE: Tested - and performs marginally better
        """
        stresses = Stress.get_stress(word)
        return all(stress[-1] > 0 for stress in stresses if stress)

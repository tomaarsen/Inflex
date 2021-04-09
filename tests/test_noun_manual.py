#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random
import unittest

from inflexion import Noun


class TestNouns(unittest.TestCase):

    def test_is_noun(self):
        noun = Noun("book")
        self.assertFalse(noun.is_verb())
        self.assertTrue(noun.is_noun())
        self.assertFalse(noun.is_adj())

    def test_as_regex(self):
        noun = Noun("brother")
        pattern = noun.as_regex()
        self.assertEqual(pattern, re.compile("brothers|brother|brethren", re.IGNORECASE),
                         "Check whether as_regex produces a compiled regex object correctly.")

    def test_classical_as_regex(self):
        noun = Noun("brother")
        classical = noun.classical()
        pattern = classical.as_regex()
        self.assertEqual(pattern, re.compile("brother|brethren", re.IGNORECASE),
                         "Check whether as_regex on classical() produces a compiled regex object correctly.")

    def test_classical_cache(self):
        noun = Noun("brother")
        classical_one = noun.classical()
        classical_two = noun.classical()
        self.assertEqual(classical_one, classical_two,
                         "Cache of Noun(...).classical()")

    def test_classical_classical(self):
        classical_one = Noun("brother").classical()
        classical_two = classical_one.classical()
        self.assertEqual(classical_one, classical_two,
                         "Noun(...).classical() == Noun(...).classical().classical()")

    def test_classical_modern(self):
        noun = Noun("brother")
        classical = noun.classical()
        modern = classical.modern()
        self.assertEqual(noun, modern,
                         "Noun(...) = Noun(...).classical().modern()")

    def test_repr(self):
        noun = Noun("brother")
        self.assertEqual(f"{noun!r}", "Noun('brother')")

    def test_classical_repr(self):
        noun = Noun("brother")
        classical = noun.classical()
        self.assertEqual(f"{classical!r}", "Noun('brother').classical()")

    def test_indefinite_plural(self):
        test_data = [
            ('universe', 'universes'),
            ('uniplex', 'uniplexes'),
            ('height', 'heights'),
            ('FSM', 'FSMS'),
            ('use', 'uses'),
            ('lady in waiting', 'ladies in waiting'),
            ('octavo', 'octavos'),
            ('D', 'DS'),
            ('Q', 'QS'),
            ('PET', 'PETS'),
            ('P', 'PS'),
            ('erratum', 'errata'),
            ('once-and-future-king', 'once-and-future-kings'),
            ('Tth', 'Tths'),
            ('urn', 'urns'),
            ('DNR', 'DNRS'),
            ('N', 'NS'),
            ('FACT', 'FACTS'),
            ('UNESCO representative', 'UNESCO representatives'),
            ('Oth', 'Oths')]
        for sing, plur in test_data:
            with self.subTest():
                digit = random.randrange(2, 10)
                out = Noun(sing).indefinite(count=digit)
                self.assertEqual(out, f'{digit} {plur}',
                                 f"Noun({sing!r}).indefinite(count={digit})")


if __name__ == "__main__":
    unittest.main()

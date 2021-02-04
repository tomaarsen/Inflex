
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from inflexion.adjective import Adjective

class TestAdjectives(unittest.TestCase):
    
    adjectives = [
        'defiant',
        'homeless',
        'adorable',
        'delightful',
        'homely',
        'quaint',
        'adventurous',
        'depressed',
        'horrible',
        'aggressive',
        'determined',
        'hungry',
        'real',
        'agreeable',
        'different',
        'hurt',
        'relieved',
        'alert',
        'difficult',
        'repulsive',
        'alive',
        'disgusted',
        'ill',
        'rich',
        'amused',
        'distinct',
        'important',
        'angry',
        'disturbed',
        'impossible',
        'scary',
        'annoyed',
        'dizzy',
        'inexpensive',
        'selfish',
        'annoying',
        'doubtful',
        'innocent',
        'shiny',
        'anxious',
        'drab',
        'inquisitive',
        'shy',
        'arrogant',
        'dull',
        'itchy',
        'silly',
        'ashamed',
        'sleepy',
        'attractive',
        'eager',
        'jealous',
        'smiling',
        'average',
        'easy',
        'jittery',
        'smoggy',
        'awful',
        'elated',
        'jolly',
        'sore',
        'elegant',
        'joyous',
        'sparkling',
        'bad',
        'embarrassed',
        'splendid',
        'beautiful',
        'enchanting',
        'kind',
        'spotless',
        'better',
        'encouraging',
        'stormy',
        'bewildered',
        'energetic',
        'lazy',
        'strange',
        'black',
        'enthusiastic',
        'light',
        'stupid',
        'bloody',
        'envious',
        'lively',
        'successful',
        'blue',
        'evil',
        'lonely',
        'super',
        'blue-eyed',
        'excited',
        'long',
        'blushing',
        'expensive',
        'lovely',
        'talented',
        'bored',
        'exuberant',
        'lucky',
        'tame',
        'brainy',
        'tender',
        'brave',
        'fair',
        'magnificent',
        'tense',
        'breakable',
        'faithful',
        'misty',
        'terrible',
        'bright',
        'famous',
        'modern',
        'tasty',
        'busy',
        'fancy',
        'motionless',
        'thankful',
        'fantastic',
        'muddy',
        'thoughtful',
        'calm',
        'fierce',
        'mushy',
        'thoughtless',
        'careful',
        'filthy',
        'mysterious',
        'tired',
        'cautious',
        'fine',
        'tough',
        'charming',
        'foolish',
        'nasty',
        'troubled',
        'cheerful',
        'fragile',
        'naughty',
        'clean',
        'frail',
        'nervous',
        'ugliest',
        'clear',
        'frantic',
        'nice',
        'ugly',
        'clever',
        'friendly',
        'nutty',
        'uninterested',
        'cloudy',
        'frightened',
        'unsightly',
        'clumsy',
        'funny',
        'obedient',
        'unusual',
        'colorful',
        'obnoxious',
        'upset',
        'combative',
        'gentle',
        'odd',
        'uptight',
        'comfortable',
        'gifted',
        'old-fashioned',
        'concerned',
        'glamorous',
        'open',
        'vast',
        'condemned',
        'gleaming',
        'outrageous',
        'victorious',
        'confused',
        'glorious',
        'outstanding',
        'vivacious',
        'cooperative',
        'good',
        'courageous',
        'gorgeous',
        'panicky',
        'wandering',
        'crazy',
        'graceful',
        'perfect',
        'weary',
        'creepy',
        'grieving',
        'plain',
        'wicked',
        'crowded',
        'grotesque',
        'pleasant',
        'wide-eyed',
        'cruel',
        'grumpy',
        'poised',
        'wild',
        'curious',
        'poor',
        'witty',
        'cute',
        'handsome',
        'powerful',
        'worrisome',
        'happy',
        'precious',
        'worried',
        'dangerous',
        'healthy',
        'prickly',
        'wrong',
        'dark',
        'helpful',
        'proud',
        'dead',
        'helpless',
        'putrid',
        'zany',
        'defeated',
        'hilarious',
        'puzzled',
        'zealous'
    ]
    
    test_possessive_to_singular_args = [
        {'in': 'my',    'out': 'my',    'kwargs': {'person': 0}},
        {'in': 'my',    'out': 'my',    'kwargs': {'person': 1}},
        {'in': 'my',    'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'my',    'out': 'its',   'kwargs': {'person': 3}},

        {'in': 'your',  'out': 'your',  'kwargs': {'person': 0}},
        {'in': 'your',  'out': 'my',    'kwargs': {'person': 1}},
        {'in': 'your',  'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'your',  'out': 'its',   'kwargs': {'person': 3}},

        {'in': 'her',   'out': 'her',   'kwargs': {'person': 0}},
        {'in': 'her',   'out': 'my',    'kwargs': {'person': 1}},
        {'in': 'her',   'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'her',   'out': 'her',   'kwargs': {'person': 3}},

        {'in': 'his',   'out': 'his',   'kwargs': {'person': 0}},
        {'in': 'his',   'out': 'my',    'kwargs': {'person': 1}},
        {'in': 'his',   'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'his',   'out': 'his',   'kwargs': {'person': 3}},

        {'in': 'its',   'out': 'its',   'kwargs': {'person': 0}},
        {'in': 'its',   'out': 'my',    'kwargs': {'person': 1}},
        {'in': 'its',   'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'its',   'out': 'its',   'kwargs': {'person': 3}},

        {'in': 'our',   'out': 'my',    'kwargs': {'person': 0}},
        {'in': 'our',   'out': 'my',    'kwargs': {'person': 1}},
        {'in': 'our',   'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'our',   'out': 'its',   'kwargs': {'person': 3}},

        {'in': 'their', 'out': 'its',   'kwargs': {'person': 0}},
        {'in': 'their', 'out': 'my',    'kwargs': {'person': 1}},
        {'in': 'their', 'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'their', 'out': 'its',   'kwargs': {'person': 3}},

        {"in": "feet's", "out": "foot's"},
        {"in": "foot's", "out": "foot's"},
        {"in": "children's", "out": "child's"},
        {"in": "child's", "out": "child's"},
        {"in": "oxen's", "out": "ox's"},
        {"in": "ox's", "out": "ox's"},
        {"in": "latches'", "out": "latch's"},
        {"in": "latch's", "out": "latch's"},
        {"in": "ladies'", "out": "lady's"},
        {"in": "lady's", "out": "lady's"},
        {"in": "women's", "out": "woman's"},
        {"in": "woman's", "out": "woman's"},
    ]

    test_possessive_to_plural_args = [
        {'in': 'my',    'out': 'our',   'kwargs': {'person': 0}},
        {'in': 'my',    'out': 'our',   'kwargs': {'person': 1}},
        {'in': 'my',    'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'my',    'out': 'their', 'kwargs': {'person': 3}},

        {'in': 'your',  'out': 'your',  'kwargs': {'person': 0}},
        {'in': 'your',  'out': 'our',   'kwargs': {'person': 1}},
        {'in': 'your',  'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'your',  'out': 'their', 'kwargs': {'person': 3}},

        {'in': 'her',   'out': 'their', 'kwargs': {'person': 0}},
        {'in': 'her',   'out': 'our',   'kwargs': {'person': 1}},
        {'in': 'her',   'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'her',   'out': 'their', 'kwargs': {'person': 3}},

        {'in': 'his',   'out': 'their', 'kwargs': {'person': 0}},
        {'in': 'his',   'out': 'our',   'kwargs': {'person': 1}},
        {'in': 'his',   'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'his',   'out': 'their', 'kwargs': {'person': 3}},

        {'in': 'its',   'out': 'their', 'kwargs': {'person': 0}},
        {'in': 'its',   'out': 'our',   'kwargs': {'person': 1}},
        {'in': 'its',   'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'its',   'out': 'their', 'kwargs': {'person': 3}},

        {'in': 'our',   'out': 'our',   'kwargs': {'person': 0}},
        {'in': 'our',   'out': 'our',   'kwargs': {'person': 1}},
        {'in': 'our',   'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'our',   'out': 'their', 'kwargs': {'person': 3}},

        {'in': 'their', 'out': 'their', 'kwargs': {'person': 0}},
        {'in': 'their', 'out': 'our',   'kwargs': {'person': 1}},
        {'in': 'their', 'out': 'your',  'kwargs': {'person': 2}},
        {'in': 'their', 'out': 'their', 'kwargs': {'person': 3}},

        {"in": "foot's", "out": "feet's"},
        {"in": "feet's", "out": "feet's"},
        {"in": "child's", "out": "children's"},
        {"in": "children's", "out": "children's"},
        {"in": "ox's", "out": "oxen's"},
        {"in": "oxen's", "out": "oxen's"},
        {"in": "latch's", "out": "latches'"},
        {"in": "latches'", "out": "latches'"},
        {"in": "lady's", "out": "ladies'"},
        {"in": "ladies'", "out": "ladies'"},
        {"in": "woman's", "out": "women's"},
        {"in": "women's", "out": "women's"},
    ]

    def test_possessive_to_singular(self):
        for test_case in self.test_possessive_to_singular_args:
            with self.subTest():
                # Add default `kwargs` if it doesn't exist in test_case yet
                test_case = {**{
                    "kwargs": dict()
                }, **test_case}
                test_case["desc"] = f"Adjective({repr(test_case['in'])}).singular({test_case['kwargs']}) => {repr(test_case['out'])}"
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.singular(**test_case["kwargs"]), test_case["out"], test_case["desc"])

    def test_possessive_to_plural(self):
        for test_case in self.test_possessive_to_plural_args:
            with self.subTest():
                # Add default `kwargs` if it doesn't exist in test_case yet
                test_case = {**{
                    "kwargs": dict()
                }, **test_case}
                test_case["desc"] = f"Adjective({repr(test_case['in'])}).plural({test_case['kwargs']}) => {repr(test_case['out'])}"
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.plural(**test_case["kwargs"]), test_case["out"], test_case["desc"])

    def test_to_singular(self):
        for adjective in self.adjectives:
            with self.subTest():
                test_case = {
                    "in": adjective,
                    "out": adjective,
                    "desc": f"Adjective({repr(adjective)}).singular() => {repr(adjective)}",
                    "kwargs": dict()
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.singular(**test_case["kwargs"]), test_case["out"], test_case["desc"])

    def test_to_plural(self):
        for adjective in self.adjectives:
            with self.subTest():
                test_case = {
                    "in": adjective,
                    "out": adjective,
                    "desc": f"Adjective({repr(adjective)}).plural() => {repr(adjective)}",
                    "kwargs": dict()
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.plural(**test_case["kwargs"]), test_case["out"], test_case["desc"])

    def test_to_classical_plural(self):
        for adjective in self.adjectives:
            with self.subTest():
                test_case = {
                    "in": adjective,
                    "out": adjective,
                    "desc": f"Adjective({repr(adjective)}).classical().plural() => {repr(adjective)}",
                    "kwargs": dict()
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.classical().plural(**test_case["kwargs"]), test_case["out"], test_case["desc"])

if __name__ == "__main__":
    unittest.main()

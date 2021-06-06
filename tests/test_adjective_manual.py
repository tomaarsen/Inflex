#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unittest

from inflex import Adjective


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

        # We have opted to stick to "their" as a singular word
        # so 0th person singular of "their" stays as "their".
        {'in': 'their', 'out': 'their', 'kwargs': {'person': 0}},
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

    def test_is_adj(self):
        adj = Adjective("our")
        self.assertFalse(adj.is_verb())
        self.assertFalse(adj.is_noun())
        self.assertTrue(adj.is_adj())

    def test_as_regex(self):
        adj = Adjective("our")
        pattern = adj.as_regex()
        self.assertEqual(pattern, re.compile("our|my", re.IGNORECASE),
                         "Check whether as_regex produces a compiled regex object correctly.")

    def test_classical(self):
        adj = Adjective("our")
        self.assertEqual(adj, adj.classical(),
                         "Check whether Adjective(...) = Adjective(...).classical()")

    def test_plural_wrong_person(self):
        with self.assertRaises(ValueError):
            Adjective("our").plural(5)
        with self.assertRaises(ValueError):
            Adjective("our").plural("hello")
        with self.assertRaises(ValueError):
            Adjective("our").plural("first")

    def test_singular_wrong_person(self):
        with self.assertRaises(ValueError):
            Adjective("our").singular(5)
        with self.assertRaises(ValueError):
            Adjective("our").singular("hello")
        with self.assertRaises(ValueError):
            Adjective("our").singular("first")

    def test_empty(self):
        adj = Adjective("")
        adj.is_singular()
        adj.is_plural()
        adj.singular()
        adj.plural()
        adj.comparative()
        adj.superlative()

    def test_possessive_to_singular(self):
        for test_case in self.test_possessive_to_singular_args:
            with self.subTest():
                # Add default `kwargs` if it doesn't exist in test_case yet
                test_case = {**{
                    "kwargs": {}
                }, **test_case}
                test_case["desc"] = f"Adjective({repr(test_case['in'])}).singular({test_case['kwargs']}) => {repr(test_case['out'])}"
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.singular(
                    **test_case["kwargs"]), test_case["out"], test_case["desc"])

    def test_possessive_to_plural(self):
        for test_case in self.test_possessive_to_plural_args:
            with self.subTest():
                # Add default `kwargs` if it doesn't exist in test_case yet
                test_case = {**{
                    "kwargs": {}
                }, **test_case}
                test_case["desc"] = f"Adjective({repr(test_case['in'])}).plural({test_case['kwargs']}) => {repr(test_case['out'])}"
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.plural(
                    **test_case["kwargs"]), test_case["out"], test_case["desc"])

    def test_to_singular(self):
        for adjective in self.adjectives:
            with self.subTest():
                test_case = {
                    "in": adjective,
                    "out": adjective,
                    "desc": f"Adjective({repr(adjective)}).singular() => {repr(adjective)}",
                    "kwargs": {}
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.singular(
                    **test_case["kwargs"]), test_case["out"], test_case["desc"])

    def test_to_plural(self):
        for adjective in self.adjectives:
            with self.subTest():
                test_case = {
                    "in": adjective,
                    "out": adjective,
                    "desc": f"Adjective({repr(adjective)}).plural() => {repr(adjective)}",
                    "kwargs": {}
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.plural(
                    **test_case["kwargs"]), test_case["out"], test_case["desc"])

    def test_to_classical_plural(self):
        for adjective in self.adjectives:
            with self.subTest():
                test_case = {
                    "in": adjective,
                    "out": adjective,
                    "desc": f"Adjective({repr(adjective)}).classical().plural() => {repr(adjective)}",
                    "kwargs": {}
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.classical().plural(
                    **test_case["kwargs"]), test_case["out"], test_case["desc"])

    test_comparative_superlative_args = [
        ["angry", "angrier", "angriest"],
        ["bad", "worse", "worst"],
        ["beautiful", "more beautiful", "most beautiful"],
        ["big", "bigger", "biggest"],
        ["black", "blacker", "blackest"],
        ["bland", "blander", "blandest"],
        ["bloody", "bloodier", "bloodiest"],
        ["blue", "bluer", "bluest"],
        ["bold", "bolder", "boldest"],
        ["boring", "more boring", "most boring"],
        ["bossy", "bossier", "bossiest"],
        ["brave", "braver", "bravest"],
        ["brief", "briefer", "briefest"],
        ["bright", "brighter", "brightest"],
        ["broad", "broader", "broadest"],
        ["busy", "busier", "busiest"],
        ["calm", "calmer", "calmest"],
        ["cheap", "cheaper", "cheapest"],
        ["chewy", "chewier", "chewiest"],
        ["chubby", "chubbier", "chubbiest"],
        ["classy", "classier", "classiest"],
        ["clean", "cleaner", "cleanest"],
        ["clear", "clearer", "clearest"],
        ["close", "closer", "closest"],
        ["cloudy", "cloudier", "cloudiest"],
        ["clumsy", "clumsier", "clumsiest"],
        ["coarse", "coarser", "coarsest"],
        ["cold", "colder", "coldest"],
        ["cool", "cooler", "coolest"],
        ["crazy", "crazier", "craziest"],
        ["creamy", "creamier", "creamiest"],
        ["creepy", "creepier", "creepiest"],
        ["crispy", "crispier", "crispiest"],
        ["crunchy", "crunchier", "crunchiest"],
        ["curly", "curlier", "curliest"],
        ["curvy", "curvier", "curviest"],
        ["cute", "cuter", "cutest"],
        ["damp", "damper", "dampest"],
        ["dark", "darker", "darkest"],
        ["deadly", "deadlier", "deadliest"],
        ["deep", "deeper", "deepest"],
        ["dense", "denser", "densest"],
        ["difficult", "more difficult", "most difficult"],
        ["dirty", "dirtier", "dirtiest"],
        ["dry", "drier", "driest"],
        ["dull", "duller", "dullest"],
        ["dumb", "dumber", "dumbest"],
        ["dusty", "dustier", "dustiest"],
        ["early", "earlier", "earliest"],
        ["easy", "easier", "easiest"],
        ["expensive", "more expensive", "most expensive"],
        ["faint", "fainter", "faintest"],
        ["fair", "fairer", "fairest"],
        ["fancy", "fancier", "fanciest"],
        ["far", "further", "furthest"],
        ["fast", "faster", "fastest"],
        ["fat", "fatter", "fattest"],
        ["few", "fewer", "fewest"],
        ["fierce", "fiercer", "fiercest"],
        ["filthy", "filthier", "filthiest"],
        ["fine", "finer", "finest"],
        ["firm", "firmer", "firmest"],
        ["fit", "fitter", "fittest"],
        ["flaky", "flakier", "flakiest"],
        ["flat", "flatter", "flattest"],
        ["fresh", "fresher", "freshest"],
        ["friendly", "friendlier", "friendliest"],
        ["full", "fuller", "fullest"],
        ["funny", "funnier", "funniest"],
        ["gentle", "gentler", "gentlest"],
        ["gloomy", "gloomier", "gloomiest"],
        ["good", "better", "best"],
        ["grand", "grander", "grandest"],
        ["grave", "graver", "gravest"],
        ["greasy", "greasier", "greasiest"],
        ["great", "greater", "greatest"],
        ["greedy", "greedier", "greediest"],
        ["gross", "grosser", "grossest"],
        ["guilty", "guiltier", "guiltiest"],
        ["hairy", "hairier", "hairiest"],
        ["handy", "handier", "handiest"],
        ["happy", "happier", "happiest"],
        ["hard", "harder", "hardest"],
        ["harsh", "harsher", "harshest"],
        ["healthy", "healthier", "healthiest"],
        ["heavy", "heavier", "heaviest"],
        ["high", "higher", "highest"],
        ["hip", "hipper", "hippest"],
        ["hot", "hotter", "hottest"],
        ["humble", "humbler", "humblest"],
        ["hungry", "hungrier", "hungriest"],
        ["icy", "icier", "iciest"],
        ["interesting", "more interesting", "most interesting"],
        ["itchy", "itchier", "itchiest"],
        ["juicy", "juicier", "juiciest"],
        ["kind", "kinder", "kindest"],
        ["large", "larger", "largest"],
        ["late", "later", "latest"],
        ["lazy", "lazier", "laziest"],
        ["less", "lesser", "least"],
        ["light", "lighter", "lightest"],
        ["likely", "likelier", "likeliest"],
        ["little", "littler", "littlest"],
        ["lively", "livelier", "liveliest"],
        ["lonely", "lonelier", "loneliest"],
        ["long", "longer", "longest"],
        ["loud", "louder", "loudest"],
        ["lovely", "lovelier", "loveliest"],
        ["low", "lower", "lowest"],
        ["mad", "madder", "maddest"],
        ["many", "more", "most"],
        ["mean", "meaner", "meanest"],
        ["messy", "messier", "messiest"],
        ["mild", "milder", "mildest"],
        ["modern", "more modern", "most modern"],
        ["moist", "moister", "moistest"],
        ["much", "more", "most"],
        ["narrow", "narrower", "narrowest"],
        ["nasty", "nastier", "nastiest"],
        ["naughty", "naughtier", "naughtiest"],
        ["near", "nearer", "nearest"],
        ["neat", "neater", "neatest"],
        ["needy", "needier", "neediest"],
        ["new", "newer", "newest"],
        ["nice", "nicer", "nicest"],
        ["noisy", "noisier", "noisiest"],
        ["odd", "odder", "oddest"],
        ["oily", "oilier", "oiliest"],
        ["old", "older", "oldest"],
        ["plain", "plainer", "plainest"],
        ["poor", "poorer", "poorest"],
        ["popular", "more popular", "most popular"],
        ["pretty", "prettier", "prettiest"],
        ["proud", "prouder", "proudest"],
        ["pure", "purer", "purest"],
        ["quick", "quicker", "quickest"],
        ["rare", "rarer", "rarest"],
        ["raw", "rawer", "rawest"],
        ["rich", "richer", "richest"],
        ["ripe", "riper", "ripest"],
        ["risky", "riskier", "riskiest"],
        ["roomy", "roomier", "roomiest"],
        ["rough", "rougher", "roughest"],
        ["rude", "ruder", "rudest"],
        ["rusty", "rustier", "rustiest"],
        ["sad", "sadder", "saddest"],
        ["safe", "safer", "safest"],
        ["salty", "saltier", "saltiest"],
        ["sane", "saner", "sanest"],
        ["scary", "scarier", "scariest"],
        ["shallow", "shallower", "shallowest"],
        ["sharp", "sharper", "sharpest"],
        ["shiny", "shinier", "shiniest"],
        ["short", "shorter", "shortest"],
        ["silly", "sillier", "silliest"],
        ["simple", "simpler", "simplest"],
        ["skinny", "skinnier", "skinniest"],
        ["sleepy", "sleepier", "sleepiest"],
        ["slim", "slimmer", "slimmest"],
        ["slimy", "slimier", "slimiest"],
        ["slow", "slower", "slowest"],
        ["small", "smaller", "smallest"],
        ["smart", "smarter", "smartest"],
        ["smelly", "smellier", "smelliest"],
        ["smoky", "smokier", "smokiest"],
        ["smooth", "smoother", "smoothest"],
        ["soft", "softer", "softest"],
        ["soon", "sooner", "soonest"],
        ["sore", "sorer", "sorest"],
        ["sorry", "sorrier", "sorriest"],
        ["spicy", "spicier", "spiciest"],
        ["steep", "steeper", "steepest"],
        ["stingy", "stingier", "stingiest"],
        ["strange", "stranger", "strangest"],
        ["strict", "stricter", "strictest"],
        ["strong", "stronger", "strongest"],
        ["sunny", "sunnier", "sunniest"],
        ["sweaty", "sweatier", "sweatiest"],
        ["sweet", "sweeter", "sweetest"],
        ["tall", "taller", "tallest"],
        ["tan", "tanner", "tannest"],
        ["tasty", "tastier", "tastiest"],
        ["thick", "thicker", "thickest"],
        ["thin", "thinner", "thinnest"],
        ["thirsty", "thirstier", "thirstiest"],
        ["tiny", "tinier", "tiniest"],
        ["tired", "more tired", "most tired"],
        ["tough", "tougher", "toughest"],
        ["true", "truer", "truest"],
        ["ugly", "uglier", "ugliest"],
        ["warm", "warmer", "warmest"],
        ["weak", "weaker", "weakest"],
        ["wealthy", "wealthier", "wealthiest"],
        ["weird", "weirder", "weirdest"],
        ["well", "better", "best"],
        ["wet", "wetter", "wettest"],
        ["wide", "wider", "widest"],
        ["wild", "wilder", "wildest"],
        ["windy", "windier", "windiest"],
        ["wise", "wiser", "wisest"],
        ["worldly", "worldlier", "worldliest"],
        ["worthy", "worthier", "worthiest"],
        ["young", "younger", "youngest"],

        ["major league", "more major league", "most major league"],
        ["pure and simple", "purer and simpler", "purest and simplest"],
        ["quick and dirty", "quicker and dirtier", "quickest and dirtiest"],
        ["high and mighty", "higher and mightier", "highest and mightiest"],
        ["lean and mean", "leaner and meaner", "leanest and meanest"],
        ["short and sweet", "shorter and sweeter", "shortest and sweetest"],
        ["neat and tidy", "neater and tidier", "neatest and tidiest"],
        ["cutting edge", "more cutting edge", "most cutting edge"],
        ["future proof", "more future proof", "most future proof"],
        ["morbidly obese", "more morbidly obese", "most morbidly obese"],
        ["good for someone", "better for someone", "best for someone"],

        ["unfit", "unfitter", "unfittest"],
        ["unlikely", "unlikelier", "unlikeliest"],
        ["unkind", "unkinder", "unkindest"],
        ["unpopular", "more unpopular", "most unpopular"],
        ["unsafe", "unsafer", "unsafest"],
        ["untasty", "untastier", "untastiest"],
        ["unwealthy", "unwealthier", "unwealthiest"],
        ["unworldly", "unworldlier", "unworldliest"],
    ]

    def test_to_comparative(self):
        for adjective, comparative, _ in self.test_comparative_superlative_args:
            with self.subTest():
                test_case = {
                    "in": adjective,
                    "out": comparative,
                    "desc": f"Adjective({repr(adjective)}).comparative() => {repr(comparative)}",
                    "kwargs": {}
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.comparative(**test_case["kwargs"]), test_case["out"],
                                 test_case["desc"])

    def test_to_superlative(self):
        for adjective, _, superlative in self.test_comparative_superlative_args:
            with self.subTest():
                test_case = {
                    "in": adjective,
                    "out": superlative,
                    "desc": f"Adjective({repr(adjective)}).superlative() => {repr(superlative)}",
                    "kwargs": {}
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.superlative(**test_case["kwargs"]), test_case["out"],
                                 test_case["desc"])

    def test_from_comp_to_comp(self):
        comparative_exceptions = [
            "better",
            "worse",
            "further",
            "more"
        ]
        for comparative in comparative_exceptions:
            with self.subTest():
                test_case = {
                    "in": comparative,
                    "out": comparative,
                    "desc": f"Adjective({repr(comparative)}).comparative() => {repr(comparative)}",
                    "kwargs": {}
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.comparative(**test_case["kwargs"]), test_case["out"],
                                 test_case["desc"])

    def test_from_super_to_super(self):
        superlative_exceptions = [
            "best",
            "worst",
            "furthest",
            "most"
        ]
        for superlative in superlative_exceptions:
            with self.subTest():
                test_case = {
                    "in": superlative,
                    "out": superlative,
                    "desc": f"Adjective({repr(superlative)}).superlative() => {repr(superlative)}",
                    "kwargs": {}
                }
                adj = Adjective(test_case["in"])
                self.assertEqual(adj.superlative(**test_case["kwargs"]), test_case["out"],
                                 test_case["desc"])


if __name__ == "__main__":
    unittest.main()

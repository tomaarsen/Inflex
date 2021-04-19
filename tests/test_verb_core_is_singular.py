
#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
## NOTE: This module was autogenerated. ##
## Contains no user-servicable parts!!! ##
##########################################

import unittest

from inflex import Verb


class TestVerbIsSingular(unittest.TestCase):
    '''
    test_args has the format [
        {
            "in":     ..., # (required)
            "out":    ..., # (required)
            "desc":   ..., # (optional)
            "kwargs": ...  # (optional)
        }, ...
    ]
    '''
    test_args = [
        {'in': 'abides', 'out': True},
        {'in': 'aches', 'out': True},
        {'in': 'arcs', 'out': True},
        {'in': 'arises', 'out': True},
        {'in': 'asks', 'out': True},
        {'in': 'avalanches', 'out': True},
        {'in': 'awakes', 'out': True},
        {'in': 'beats', 'out': True},
        {'in': 'becomes', 'out': True},
        {'in': 'begets', 'out': True},
        {'in': 'begins', 'out': True},
        {'in': 'beholds', 'out': True},
        {'in': 'bellyaches', 'out': True},
        {'in': 'bends', 'out': True},
        {'in': 'bets', 'out': True},
        {'in': 'biases', 'out': True},
        {'in': 'bites', 'out': True},
        {'in': 'bleeds', 'out': True},
        {'in': 'blitzes', 'out': True},
        {'in': 'blows', 'out': True},
        {'in': 'breaks', 'out': True},
        {'in': 'brings', 'out': True},
        {'in': 'builds', 'out': True},
        {'in': 'burns', 'out': True},
        {'in': 'bursts', 'out': True},
        {'in': 'buses', 'out': True},
        {'in': 'busts', 'out': True},
        {'in': 'caches', 'out': True},
        {'in': 'caddies', 'out': True},
        {'in': 'can', 'out': True},
        {'in': 'canvases', 'out': True},
        {'in': 'catches', 'out': True},
        {'in': 'caucuses', 'out': True},
        {'in': 'changes', 'out': True},
        {'in': 'chooses', 'out': True},
        {'in': 'choruses', 'out': True},
        {'in': 'claps', 'out': True},
        {'in': 'clings', 'out': True},
        {'in': 'comes', 'out': True},
        {'in': 'continues', 'out': True},
        {'in': 'costs', 'out': True},
        {'in': 'could', 'out': True},
        {'in': 'creches', 'out': True},
        {'in': 'creeps', 'out': True},
        {'in': 'dares', 'out': True},
        {'in': 'deals', 'out': True},
        {'in': 'dies', 'out': True},
        {'in': 'digs', 'out': True},
        {'in': 'disses', 'out': True},
        {'in': 'dives', 'out': True},
        {'in': 'does', 'out': True},
        {'in': 'douches', 'out': True},
        {'in': 'drags', 'out': True},
        {'in': 'dreams', 'out': True},
        {'in': 'drinks', 'out': True},
        {'in': 'drives', 'out': True},
        {'in': 'dwells', 'out': True},
        {'in': 'eats', 'out': True},
        {'in': 'expects', 'out': True},
        {'in': 'falls', 'out': True},
        {'in': 'feels', 'out': True},
        {'in': 'fights', 'out': True},
        {'in': 'finds', 'out': True},
        {'in': 'flees', 'out': True},
        {'in': 'flies', 'out': True},
        {'in': 'flings', 'out': True},
        {'in': 'focuses', 'out': True},
        {'in': 'follows', 'out': True},
        {'in': 'forbids', 'out': True},
        {'in': 'foresees', 'out': True},
        {'in': 'foretells', 'out': True},
        {'in': 'forgets', 'out': True},
        {'in': 'forgives', 'out': True},
        {'in': 'forsakes', 'out': True},
        {'in': 'gases', 'out': True},
        {'in': 'gets', 'out': True},
        {'in': 'gilds', 'out': True},
        {'in': 'gives', 'out': True},
        {'in': 'goes', 'out': True},
        {'in': 'grinds', 'out': True},
        {'in': 'happens', 'out': True},
        {'in': 'has', 'out': True},
        {'in': 'helps', 'out': True},
        {'in': 'hews', 'out': True},
        {'in': 'hies', 'out': True},
        {'in': 'hits', 'out': True},
        {'in': 'hocuses', 'out': True},
        {'in': 'holds', 'out': True},
        {'in': 'hurts', 'out': True},
        {'in': 'inlays', 'out': True},
        {'in': 'insists', 'out': True},
        {'in': 'interlays', 'out': True},
        {'in': 'irises', 'out': True},
        {'in': 'keeps', 'out': True},
        {'in': 'kills', 'out': True},
        {'in': 'kneels', 'out': True},
        {'in': 'knits', 'out': True},
        {'in': 'knows', 'out': True},
        {'in': 'lays', 'out': True},
        {'in': 'leads', 'out': True},
        {'in': 'leans', 'out': True},
        {'in': 'leaps', 'out': True},
        {'in': 'learns', 'out': True},
        {'in': 'leaves', 'out': True},
        {'in': 'lets', 'out': True},
        {'in': 'lies', 'out': True},
        {'in': 'likes', 'out': True},
        {'in': 'lives', 'out': True},
        {'in': 'looks', 'out': True},
        {'in': 'loses', 'out': True},
        {'in': 'loves', 'out': True},
        {'in': 'may', 'out': True},
        {'in': 'means', 'out': True},
        {'in': 'meets', 'out': True},
        {'in': 'menus', 'out': True},
        {'in': 'might', 'out': True},
        {'in': 'misleads', 'out': True},
        {'in': 'mistakes', 'out': True},
        {'in': 'misunderstands', 'out': True},
        {'in': 'moves', 'out': True},
        {'in': 'must', 'out': True},
        {'in': 'needs', 'out': True},
        {'in': 'niches', 'out': True},
        {'in': 'ought', 'out': True},
        {'in': 'outvies', 'out': True},
        {'in': 'overdraws', 'out': True},
        {'in': 'overhears', 'out': True},
        {'in': 'overtakes', 'out': True},
        {'in': 'presets', 'out': True},
        {'in': 'proves', 'out': True},
        {'in': 'provides', 'out': True},
        {'in': 'psyches', 'out': True},
        {'in': 'puts', 'out': True},
        {'in': 'quits', 'out': True},
        {'in': 'quizzes', 'out': True},
        {'in': 'reaches', 'out': True},
        {'in': 'remains', 'out': True},
        {'in': 'remembers', 'out': True},
        {'in': 'rends', 'out': True},
        {'in': 'rents', 'out': True},
        {'in': 'rids', 'out': True},
        {'in': 'rings', 'out': True},
        {'in': 'rises', 'out': True},
        {'in': 'rives', 'out': True},
        {'in': 's', 'out': True},
        {'in': 'saws', 'out': True},
        {'in': 'seeks', 'out': True},
        {'in': 'seems', 'out': True},
        {'in': 'shakes', 'out': True},
        {'in': 'shall', 'out': True},
        {'in': 'shaves', 'out': True},
        {'in': 'sheds', 'out': True},
        {'in': 'shits', 'out': True},
        {'in': 'shoes', 'out': True},
        {'in': 'should', 'out': True},
        {'in': 'shows', 'out': True},
        {'in': 'shrinks', 'out': True},
        {'in': 'sings', 'out': True},
        {'in': 'sinks', 'out': True},
        {'in': 'sits', 'out': True},
        {'in': 'skis', 'out': True},
        {'in': 'slays', 'out': True},
        {'in': 'slides', 'out': True},
        {'in': 'slinks', 'out': True},
        {'in': 'slits', 'out': True},
        {'in': 'smells', 'out': True},
        {'in': 'smites', 'out': True},
        {'in': 'sneaks', 'out': True},
        {'in': 'sows', 'out': True},
        {'in': 'speaks', 'out': True},
        {'in': 'speeds', 'out': True},
        {'in': 'spends', 'out': True},
        {'in': 'spits', 'out': True},
        {'in': 'spoils', 'out': True},
        {'in': 'springs', 'out': True},
        {'in': 'stands', 'out': True},
        {'in': 'staves', 'out': True},
        {'in': 'stays', 'out': True},
        {'in': 'steals', 'out': True},
        {'in': 'stings', 'out': True},
        {'in': 'stinks', 'out': True},
        {'in': 'stops', 'out': True},
        {'in': 'strews', 'out': True},
        {'in': 'strides', 'out': True},
        {'in': 'strips', 'out': True},
        {'in': 'strives', 'out': True},
        {'in': 'sublets', 'out': True},
        {'in': 'sunburns', 'out': True},
        {'in': 'swears', 'out': True},
        {'in': 'sweats', 'out': True},
        {'in': 'sweeps', 'out': True},
        {'in': 'swells', 'out': True},
        {'in': 'swims', 'out': True},
        {'in': 'swings', 'out': True},
        {'in': 'talks', 'out': True},
        {'in': 'tears', 'out': True},
        {'in': 'thrives', 'out': True},
        {'in': 'thrusts', 'out': True},
        {'in': 'treads', 'out': True},
        {'in': 'undergoes', 'out': True},
        {'in': 'underlies', 'out': True},
        {'in': 'understands', 'out': True},
        {'in': 'undertakes', 'out': True},
        {'in': 'upsets', 'out': True},
        {'in': 'vexes', 'out': True},
        {'in': 'vies', 'out': True},
        {'in': 'waits', 'out': True},
        {'in': 'wakes', 'out': True},
        {'in': 'walks', 'out': True},
        {'in': 'wants', 'out': True},
        {'in': 'was', 'out': True},
        {'in': 'watches', 'out': True},
        {'in': 'wears', 'out': True},
        {'in': 'weeps', 'out': True},
        {'in': 'wends', 'out': True},
        {'in': 'will', 'out': True},
        {'in': 'wins', 'out': True},
        {'in': 'wises', 'out': True},
        {'in': 'withdraws', 'out': True},
        {'in': 'withholds', 'out': True},
        {'in': 'withstands', 'out': True},
        {'in': 'would', 'out': True},
        {'in': 'wrings', 'out': True},
    ]

    def test_verb_is_singular(self):
        for test_case in self.test_args:
            with self.subTest():
                # Expand test_case with default cases, if optional keys are not provided
                test_case = {**test_case, **{
                    "desc": f"is_singular({repr(test_case['in'])}) => {repr(test_case['out'])}",
                    "kwargs": dict()
                }}
                self.assertEqual(Verb(test_case["in"]).is_singular(**test_case["kwargs"]), test_case["out"], test_case["desc"])


if __name__ == "__main__":
    unittest.main()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
## NOTE: This module was autogenerated. ##
## Contains no user-servicable parts!!! ##
##########################################

import unittest

from inflexion.verb_core import convert_to_singular

class TestVerbToSingular(unittest.TestCase):
    # test_args has the format [{
    #    "in":     ..., # (required)
    #    "out":    ..., # (required)
    #    "desc":   ..., # (optional) 
    #    "kwargs": ...  # (optional)
    # }, ...
    # ]
    test_args = [
        {'in': 'abide', 'out': 'abides'},
        {'in': 'abides', 'out': 'abides'},
        {'in': 'ache', 'out': 'aches'},
        {'in': 'aches', 'out': 'aches'},
        {'in': 'arc', 'out': 'arcs'},
        {'in': 'arcs', 'out': 'arcs'},
        {'in': 'are', 'out': 'is'},
        {'in': 'arise', 'out': 'arises'},
        {'in': 'arises', 'out': 'arises'},
        {'in': 'ask', 'out': 'asks'},
        {'in': 'asks', 'out': 'asks'},
        {'in': 'avalanche', 'out': 'avalanches'},
        {'in': 'avalanches', 'out': 'avalanches'},
        {'in': 'awake', 'out': 'awakes'},
        {'in': 'awakes', 'out': 'awakes'},
        {'in': 'be', 'out': 'is'},
        {'in': 'beat', 'out': 'beats'},
        {'in': 'beats', 'out': 'beats'},
        {'in': 'become', 'out': 'becomes'},
        {'in': 'becomes', 'out': 'becomes'},
        {'in': 'beget', 'out': 'begets'},
        {'in': 'begets', 'out': 'begets'},
        {'in': 'begin', 'out': 'begins'},
        {'in': 'begins', 'out': 'begins'},
        {'in': 'behold', 'out': 'beholds'},
        {'in': 'beholds', 'out': 'beholds'},
        {'in': 'bellyache', 'out': 'bellyaches'},
        {'in': 'bellyaches', 'out': 'bellyaches'},
        {'in': 'bend', 'out': 'bends'},
        {'in': 'bends', 'out': 'bends'},
        {'in': 'bet', 'out': 'bets'},
        {'in': 'bets', 'out': 'bets'},
        {'in': 'bias', 'out': 'biases'},
        {'in': 'biases', 'out': 'biases'},
        {'in': 'bite', 'out': 'bites'},
        {'in': 'bites', 'out': 'bites'},
        {'in': 'bleed', 'out': 'bleeds'},
        {'in': 'bleeds', 'out': 'bleeds'},
        {'in': 'blitz', 'out': 'blitzes'},
        {'in': 'blitzes', 'out': 'blitzes'},
        {'in': 'blow', 'out': 'blows'},
        {'in': 'blows', 'out': 'blows'},
        {'in': 'break', 'out': 'breaks'},
        {'in': 'breaks', 'out': 'breaks'},
        {'in': 'bring', 'out': 'brings'},
        {'in': 'brings', 'out': 'brings'},
        {'in': 'build', 'out': 'builds'},
        {'in': 'builds', 'out': 'builds'},
        {'in': 'burn', 'out': 'burns'},
        {'in': 'burns', 'out': 'burns'},
        {'in': 'burst', 'out': 'bursts'},
        {'in': 'bursts', 'out': 'bursts'},
        {'in': 'bus', 'out': 'buses'},
        {'in': 'buses', 'out': 'buses'},
        {'in': 'bust', 'out': 'busts'},
        {'in': 'busts', 'out': 'busts'},
        {'in': 'cache', 'out': 'caches'},
        {'in': 'caches', 'out': 'caches'},
        {'in': 'caddie', 'out': 'caddies'},
        {'in': 'caddies', 'out': 'caddies'},
        {'in': 'can', 'out': 'can'},
        {'in': 'canvas', 'out': 'canvases'},
        {'in': 'canvases', 'out': 'canvases'},
        {'in': 'catch', 'out': 'catches'},
        {'in': 'catches', 'out': 'catches'},
        {'in': 'caucus', 'out': 'caucuses'},
        {'in': 'caucuses', 'out': 'caucuses'},
        {'in': 'change', 'out': 'changes'},
        {'in': 'changes', 'out': 'changes'},
        {'in': 'choose', 'out': 'chooses'},
        {'in': 'chooses', 'out': 'chooses'},
        {'in': 'chorus', 'out': 'choruses'},
        {'in': 'choruses', 'out': 'choruses'},
        {'in': 'clap', 'out': 'claps'},
        {'in': 'claps', 'out': 'claps'},
        {'in': 'cling', 'out': 'clings'},
        {'in': 'clings', 'out': 'clings'},
        {'in': 'come', 'out': 'comes'},
        {'in': 'comes', 'out': 'comes'},
        {'in': 'continue', 'out': 'continues'},
        {'in': 'continues', 'out': 'continues'},
        {'in': 'cost', 'out': 'costs'},
        {'in': 'costs', 'out': 'costs'},
        {'in': 'could', 'out': 'could'},
        {'in': 'creche', 'out': 'creches'},
        {'in': 'creches', 'out': 'creches'},
        {'in': 'creep', 'out': 'creeps'},
        {'in': 'creeps', 'out': 'creeps'},
        {'in': 'dare', 'out': 'dares'},
        {'in': 'dares', 'out': 'dares'},
        {'in': 'deal', 'out': 'deals'},
        {'in': 'deals', 'out': 'deals'},
        {'in': 'die', 'out': 'dies'},
        {'in': 'dies', 'out': 'dies'},
        {'in': 'dig', 'out': 'digs'},
        {'in': 'digs', 'out': 'digs'},
        {'in': 'dis', 'out': 'disses'},
        {'in': 'disses', 'out': 'disses'},
        {'in': 'dive', 'out': 'dives'},
        {'in': 'dives', 'out': 'dives'},
        {'in': 'do', 'out': 'does'},
        {'in': 'does', 'out': 'does'},
        {'in': 'douche', 'out': 'douches'},
        {'in': 'douches', 'out': 'douches'},
        {'in': 'drag', 'out': 'drags'},
        {'in': 'drags', 'out': 'drags'},
        {'in': 'dream', 'out': 'dreams'},
        {'in': 'dreams', 'out': 'dreams'},
        {'in': 'drink', 'out': 'drinks'},
        {'in': 'drinks', 'out': 'drinks'},
        {'in': 'drive', 'out': 'drives'},
        {'in': 'drives', 'out': 'drives'},
        {'in': 'dwell', 'out': 'dwells'},
        {'in': 'dwells', 'out': 'dwells'},
        {'in': 'eat', 'out': 'eats'},
        {'in': 'eats', 'out': 'eats'},
        {'in': 'expect', 'out': 'expects'},
        {'in': 'expects', 'out': 'expects'},
        {'in': 'fall', 'out': 'falls'},
        {'in': 'falls', 'out': 'falls'},
        {'in': 'feel', 'out': 'feels'},
        {'in': 'feels', 'out': 'feels'},
        {'in': 'fight', 'out': 'fights'},
        {'in': 'fights', 'out': 'fights'},
        {'in': 'find', 'out': 'finds'},
        {'in': 'finds', 'out': 'finds'},
        {'in': 'flee', 'out': 'flees'},
        {'in': 'flees', 'out': 'flees'},
        {'in': 'flies', 'out': 'flies'},
        {'in': 'fling', 'out': 'flings'},
        {'in': 'flings', 'out': 'flings'},
        {'in': 'fly', 'out': 'flies'},
        {'in': 'focus', 'out': 'focuses'},
        {'in': 'focuses', 'out': 'focuses'},
        {'in': 'follow', 'out': 'follows'},
        {'in': 'follows', 'out': 'follows'},
        {'in': 'forbid', 'out': 'forbids'},
        {'in': 'forbids', 'out': 'forbids'},
        {'in': 'foresee', 'out': 'foresees'},
        {'in': 'foresees', 'out': 'foresees'},
        {'in': 'foretell', 'out': 'foretells'},
        {'in': 'foretells', 'out': 'foretells'},
        {'in': 'forget', 'out': 'forgets'},
        {'in': 'forgets', 'out': 'forgets'},
        {'in': 'forgive', 'out': 'forgives'},
        {'in': 'forgives', 'out': 'forgives'},
        {'in': 'forsake', 'out': 'forsakes'},
        {'in': 'forsakes', 'out': 'forsakes'},
        {'in': 'gas', 'out': 'gases'},
        {'in': 'gases', 'out': 'gases'},
        {'in': 'get', 'out': 'gets'},
        {'in': 'gets', 'out': 'gets'},
        {'in': 'gild', 'out': 'gilds'},
        {'in': 'gilds', 'out': 'gilds'},
        {'in': 'give', 'out': 'gives'},
        {'in': 'gives', 'out': 'gives'},
        {'in': 'go', 'out': 'goes'},
        {'in': 'goes', 'out': 'goes'},
        {'in': 'grind', 'out': 'grinds'},
        {'in': 'grinds', 'out': 'grinds'},
        {'in': 'happen', 'out': 'happens'},
        {'in': 'happens', 'out': 'happens'},
        {'in': 'has', 'out': 'has'},
        {'in': 'have', 'out': 'has'},
        {'in': 'help', 'out': 'helps'},
        {'in': 'helps', 'out': 'helps'},
        {'in': 'hew', 'out': 'hews'},
        {'in': 'hews', 'out': 'hews'},
        {'in': 'hie', 'out': 'hies'},
        {'in': 'hies', 'out': 'hies'},
        {'in': 'hit', 'out': 'hits'},
        {'in': 'hits', 'out': 'hits'},
        {'in': 'hocus', 'out': 'hocuses'},
        {'in': 'hocuses', 'out': 'hocuses'},
        {'in': 'hold', 'out': 'holds'},
        {'in': 'holds', 'out': 'holds'},
        {'in': 'hurt', 'out': 'hurts'},
        {'in': 'hurts', 'out': 'hurts'},
        {'in': 'inlay', 'out': 'inlays'},
        {'in': 'inlays', 'out': 'inlays'},
        {'in': 'insist', 'out': 'insists'},
        {'in': 'insists', 'out': 'insists'},
        {'in': 'interlay', 'out': 'interlays'},
        {'in': 'interlays', 'out': 'interlays'},
        {'in': 'iris', 'out': 'irises'},
        {'in': 'irises', 'out': 'irises'},
        {'in': 'is', 'out': 'is'},
        {'in': 'keep', 'out': 'keeps'},
        {'in': 'keeps', 'out': 'keeps'},
        {'in': 'kill', 'out': 'kills'},
        {'in': 'kills', 'out': 'kills'},
        {'in': 'kneel', 'out': 'kneels'},
        {'in': 'kneels', 'out': 'kneels'},
        {'in': 'knit', 'out': 'knits'},
        {'in': 'knits', 'out': 'knits'},
        {'in': 'know', 'out': 'knows'},
        {'in': 'knows', 'out': 'knows'},
        {'in': 'lay', 'out': 'lays'},
        {'in': 'lays', 'out': 'lays'},
        {'in': 'lead', 'out': 'leads'},
        {'in': 'leads', 'out': 'leads'},
        {'in': 'lean', 'out': 'leans'},
        {'in': 'leans', 'out': 'leans'},
        {'in': 'leap', 'out': 'leaps'},
        {'in': 'leaps', 'out': 'leaps'},
        {'in': 'learn', 'out': 'learns'},
        {'in': 'learns', 'out': 'learns'},
        {'in': 'leave', 'out': 'leaves'},
        {'in': 'leaves', 'out': 'leaves'},
        {'in': 'let', 'out': 'lets'},
        {'in': 'lets', 'out': 'lets'},
        {'in': 'lie', 'out': 'lies'},
        {'in': 'lies', 'out': 'lies'},
        {'in': 'like', 'out': 'likes'},
        {'in': 'likes', 'out': 'likes'},
        {'in': 'live', 'out': 'lives'},
        {'in': 'lives', 'out': 'lives'},
        {'in': 'look', 'out': 'looks'},
        {'in': 'looks', 'out': 'looks'},
        {'in': 'lose', 'out': 'loses'},
        {'in': 'loses', 'out': 'loses'},
        {'in': 'love', 'out': 'loves'},
        {'in': 'loves', 'out': 'loves'},
        {'in': 'may', 'out': 'may'},
        {'in': 'mean', 'out': 'means'},
        {'in': 'means', 'out': 'means'},
        {'in': 'meet', 'out': 'meets'},
        {'in': 'meets', 'out': 'meets'},
        {'in': 'menu', 'out': 'menus'},
        {'in': 'menus', 'out': 'menus'},
        {'in': 'might', 'out': 'might'},
        {'in': 'mislead', 'out': 'misleads'},
        {'in': 'misleads', 'out': 'misleads'},
        {'in': 'mistake', 'out': 'mistakes'},
        {'in': 'mistakes', 'out': 'mistakes'},
        {'in': 'misunderstand', 'out': 'misunderstands'},
        {'in': 'misunderstands', 'out': 'misunderstands'},
        {'in': 'move', 'out': 'moves'},
        {'in': 'moves', 'out': 'moves'},
        {'in': 'must', 'out': 'must'},
        {'in': 'need', 'out': 'needs'},
        {'in': 'needs', 'out': 'needs'},
        {'in': 'niche', 'out': 'niches'},
        {'in': 'niches', 'out': 'niches'},
        {'in': 'ought', 'out': 'ought'},
        {'in': 'outvie', 'out': 'outvies'},
        {'in': 'outvies', 'out': 'outvies'},
        {'in': 'overdraw', 'out': 'overdraws'},
        {'in': 'overdraws', 'out': 'overdraws'},
        {'in': 'overhear', 'out': 'overhears'},
        {'in': 'overhears', 'out': 'overhears'},
        {'in': 'overtake', 'out': 'overtakes'},
        {'in': 'overtakes', 'out': 'overtakes'},
        {'in': 'preset', 'out': 'presets'},
        {'in': 'presets', 'out': 'presets'},
        {'in': 'prove', 'out': 'proves'},
        {'in': 'proves', 'out': 'proves'},
        {'in': 'provide', 'out': 'provides'},
        {'in': 'provides', 'out': 'provides'},
        {'in': 'psyche', 'out': 'psyches'},
        {'in': 'psyches', 'out': 'psyches'},
        {'in': 'put', 'out': 'puts'},
        {'in': 'puts', 'out': 'puts'},
        {'in': 'quit', 'out': 'quits'},
        {'in': 'quits', 'out': 'quits'},
        {'in': 'quiz', 'out': 'quizzes'},
        {'in': 'quizzes', 'out': 'quizzes'},
        {'in': 'reach', 'out': 'reaches'},
        {'in': 'reaches', 'out': 'reaches'},
        {'in': 'remain', 'out': 'remains'},
        {'in': 'remains', 'out': 'remains'},
        {'in': 'remember', 'out': 'remembers'},
        {'in': 'remembers', 'out': 'remembers'},
        {'in': 'rend', 'out': 'rends'},
        {'in': 'rends', 'out': 'rends'},
        {'in': 'rent', 'out': 'rents'},
        {'in': 'rents', 'out': 'rents'},
        {'in': 'rid', 'out': 'rids'},
        {'in': 'rids', 'out': 'rids'},
        {'in': 'ring', 'out': 'rings'},
        {'in': 'rings', 'out': 'rings'},
        {'in': 'rise', 'out': 'rises'},
        {'in': 'rises', 'out': 'rises'},
        {'in': 'rive', 'out': 'rives'},
        {'in': 'rives', 'out': 'rives'},
        {'in': 's', 'out': 's'},
        {'in': 'saw', 'out': 'saws'},
        {'in': 'saws', 'out': 'saws'},
        {'in': 'seek', 'out': 'seeks'},
        {'in': 'seeks', 'out': 'seeks'},
        {'in': 'seem', 'out': 'seems'},
        {'in': 'seems', 'out': 'seems'},
        {'in': 'shake', 'out': 'shakes'},
        {'in': 'shakes', 'out': 'shakes'},
        {'in': 'shall', 'out': 'shall'},
        {'in': 'shave', 'out': 'shaves'},
        {'in': 'shaves', 'out': 'shaves'},
        {'in': 'shed', 'out': 'sheds'},
        {'in': 'sheds', 'out': 'sheds'},
        {'in': 'shit', 'out': 'shits'},
        {'in': 'shits', 'out': 'shits'},
        {'in': 'shoe', 'out': 'shoes'},
        {'in': 'shoes', 'out': 'shoes'},
        {'in': 'should', 'out': 'should'},
        {'in': 'show', 'out': 'shows'},
        {'in': 'shows', 'out': 'shows'},
        {'in': 'shrink', 'out': 'shrinks'},
        {'in': 'shrinks', 'out': 'shrinks'},
        {'in': 'sing', 'out': 'sings'},
        {'in': 'sings', 'out': 'sings'},
        {'in': 'sink', 'out': 'sinks'},
        {'in': 'sinks', 'out': 'sinks'},
        {'in': 'sit', 'out': 'sits'},
        {'in': 'sits', 'out': 'sits'},
        {'in': 'ski', 'out': 'skis'},
        {'in': 'skis', 'out': 'skis'},
        {'in': 'slay', 'out': 'slays'},
        {'in': 'slays', 'out': 'slays'},
        {'in': 'slide', 'out': 'slides'},
        {'in': 'slides', 'out': 'slides'},
        {'in': 'slink', 'out': 'slinks'},
        {'in': 'slinks', 'out': 'slinks'},
        {'in': 'slit', 'out': 'slits'},
        {'in': 'slits', 'out': 'slits'},
        {'in': 'smell', 'out': 'smells'},
        {'in': 'smells', 'out': 'smells'},
        {'in': 'smite', 'out': 'smites'},
        {'in': 'smites', 'out': 'smites'},
        {'in': 'sneak', 'out': 'sneaks'},
        {'in': 'sneaks', 'out': 'sneaks'},
        {'in': 'sow', 'out': 'sows'},
        {'in': 'sows', 'out': 'sows'},
        {'in': 'speak', 'out': 'speaks'},
        {'in': 'speaks', 'out': 'speaks'},
        {'in': 'speed', 'out': 'speeds'},
        {'in': 'speeds', 'out': 'speeds'},
        {'in': 'spend', 'out': 'spends'},
        {'in': 'spends', 'out': 'spends'},
        {'in': 'spit', 'out': 'spits'},
        {'in': 'spits', 'out': 'spits'},
        {'in': 'spoil', 'out': 'spoils'},
        {'in': 'spoils', 'out': 'spoils'},
        {'in': 'spring', 'out': 'springs'},
        {'in': 'springs', 'out': 'springs'},
        {'in': 'stand', 'out': 'stands'},
        {'in': 'stands', 'out': 'stands'},
        {'in': 'stave', 'out': 'staves'},
        {'in': 'staves', 'out': 'staves'},
        {'in': 'stay', 'out': 'stays'},
        {'in': 'stays', 'out': 'stays'},
        {'in': 'steal', 'out': 'steals'},
        {'in': 'steals', 'out': 'steals'},
        {'in': 'sting', 'out': 'stings'},
        {'in': 'stings', 'out': 'stings'},
        {'in': 'stink', 'out': 'stinks'},
        {'in': 'stinks', 'out': 'stinks'},
        {'in': 'stop', 'out': 'stops'},
        {'in': 'stops', 'out': 'stops'},
        {'in': 'strew', 'out': 'strews'},
        {'in': 'strews', 'out': 'strews'},
        {'in': 'stride', 'out': 'strides'},
        {'in': 'strides', 'out': 'strides'},
        {'in': 'strip', 'out': 'strips'},
        {'in': 'strips', 'out': 'strips'},
        {'in': 'strive', 'out': 'strives'},
        {'in': 'strives', 'out': 'strives'},
        {'in': 'sublet', 'out': 'sublets'},
        {'in': 'sublets', 'out': 'sublets'},
        {'in': 'sunburn', 'out': 'sunburns'},
        {'in': 'sunburns', 'out': 'sunburns'},
        {'in': 'swear', 'out': 'swears'},
        {'in': 'swears', 'out': 'swears'},
        {'in': 'sweat', 'out': 'sweats'},
        {'in': 'sweats', 'out': 'sweats'},
        {'in': 'sweep', 'out': 'sweeps'},
        {'in': 'sweeps', 'out': 'sweeps'},
        {'in': 'swell', 'out': 'swells'},
        {'in': 'swells', 'out': 'swells'},
        {'in': 'swim', 'out': 'swims'},
        {'in': 'swims', 'out': 'swims'},
        {'in': 'swing', 'out': 'swings'},
        {'in': 'swings', 'out': 'swings'},
        {'in': 'talk', 'out': 'talks'},
        {'in': 'talks', 'out': 'talks'},
        {'in': 'tear', 'out': 'tears'},
        {'in': 'tears', 'out': 'tears'},
        {'in': 'thrive', 'out': 'thrives'},
        {'in': 'thrives', 'out': 'thrives'},
        {'in': 'thrust', 'out': 'thrusts'},
        {'in': 'thrusts', 'out': 'thrusts'},
        {'in': 'tread', 'out': 'treads'},
        {'in': 'treads', 'out': 'treads'},
        {'in': 'undergo', 'out': 'undergoes'},
        {'in': 'undergoes', 'out': 'undergoes'},
        {'in': 'underlie', 'out': 'underlies'},
        {'in': 'underlies', 'out': 'underlies'},
        {'in': 'understand', 'out': 'understands'},
        {'in': 'understands', 'out': 'understands'},
        {'in': 'undertake', 'out': 'undertakes'},
        {'in': 'undertakes', 'out': 'undertakes'},
        {'in': 'upset', 'out': 'upsets'},
        {'in': 'upsets', 'out': 'upsets'},
        {'in': 'vex', 'out': 'vexes'},
        {'in': 'vexes', 'out': 'vexes'},
        {'in': 'vie', 'out': 'vies'},
        {'in': 'vies', 'out': 'vies'},
        {'in': 'wait', 'out': 'waits'},
        {'in': 'waits', 'out': 'waits'},
        {'in': 'wake', 'out': 'wakes'},
        {'in': 'wakes', 'out': 'wakes'},
        {'in': 'walk', 'out': 'walks'},
        {'in': 'walks', 'out': 'walks'},
        {'in': 'want', 'out': 'wants'},
        {'in': 'wants', 'out': 'wants'},
        {'in': 'was', 'out': 'was'},
        {'in': 'watch', 'out': 'watches'},
        {'in': 'watches', 'out': 'watches'},
        {'in': 'wear', 'out': 'wears'},
        {'in': 'wears', 'out': 'wears'},
        {'in': 'weep', 'out': 'weeps'},
        {'in': 'weeps', 'out': 'weeps'},
        {'in': 'wend', 'out': 'wends'},
        {'in': 'wends', 'out': 'wends'},
        {'in': 'were', 'out': 'was'},
        {'in': 'will', 'out': 'will'},
        {'in': 'win', 'out': 'wins'},
        {'in': 'wins', 'out': 'wins'},
        {'in': 'wis', 'out': 'wises'},
        {'in': 'wises', 'out': 'wises'},
        {'in': 'withdraw', 'out': 'withdraws'},
        {'in': 'withdraws', 'out': 'withdraws'},
        {'in': 'withhold', 'out': 'withholds'},
        {'in': 'withholds', 'out': 'withholds'},
        {'in': 'withstand', 'out': 'withstands'},
        {'in': 'withstands', 'out': 'withstands'},
        {'in': 'would', 'out': 'would'},
        {'in': 'wring', 'out': 'wrings'},
        {'in': 'wrings', 'out': 'wrings'},
    ]

    def test_convert_to_singular(self):
        for test_case in self.test_args:
            with self.subTest():
                # Expand test_case with default cases, if optional keys are not provided
                test_case = {**test_case, **{
                    "desc": f"convert_to_singular({repr(test_case['in'])}) => {repr(test_case['out'])}",
                    "kwargs": dict()
                }}
                self.assertEqual(convert_to_singular(test_case["in"], **test_case["kwargs"]), test_case["out"], test_case["desc"])

if __name__ == "__main__":
    unittest.main()

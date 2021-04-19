
#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
## NOTE: This module was autogenerated. ##
## Contains no user-servicable parts!!! ##
##########################################

import unittest

from inflex import Verb


class TestVerbIsPresPart(unittest.TestCase):
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
        {'in': 'Abiding', 'out': True},
        {'in': 'Aching', 'out': True},
        {'in': 'Arcing', 'out': True},
        {'in': 'Arising', 'out': True},
        {'in': 'Asking', 'out': True},
        {'in': 'Avalanching', 'out': True},
        {'in': 'Awakening', 'out': True},
        {'in': 'Beating', 'out': True},
        {'in': 'Becoming', 'out': True},
        {'in': 'Begetting', 'out': True},
        {'in': 'Beginning', 'out': True},
        {'in': 'Beholding', 'out': True},
        {'in': 'Being', 'out': True},
        {'in': 'Bellyaching', 'out': True},
        {'in': 'Bending', 'out': True},
        {'in': 'Betting', 'out': True},
        {'in': 'Biasing', 'out': True},
        {'in': 'Biting', 'out': True},
        {'in': 'Bleeding', 'out': True},
        {'in': 'Blitzing', 'out': True},
        {'in': 'Blowing', 'out': True},
        {'in': 'Breaking', 'out': True},
        {'in': 'Bringing', 'out': True},
        {'in': 'Building', 'out': True},
        {'in': 'Burning', 'out': True},
        {'in': 'Bursting', 'out': True},
        {'in': 'Busing', 'out': True},
        {'in': 'Busting', 'out': True},
        {'in': 'Caching', 'out': True},
        {'in': 'Caddying', 'out': True},
        {'in': 'Canvasing', 'out': True},
        {'in': 'Catching', 'out': True},
        {'in': 'Caucusing', 'out': True},
        {'in': 'Changing', 'out': True},
        {'in': 'Choosing', 'out': True},
        {'in': 'Chorusing', 'out': True},
        {'in': 'Clapping', 'out': True},
        {'in': 'Clinging', 'out': True},
        {'in': 'Coming', 'out': True},
        {'in': 'Continuing', 'out': True},
        {'in': 'Costing', 'out': True},
        {'in': 'Creching', 'out': True},
        {'in': 'Creeping', 'out': True},
        {'in': 'Daring', 'out': True},
        {'in': 'Dealing', 'out': True},
        {'in': 'Digging', 'out': True},
        {'in': 'Dissing', 'out': True},
        {'in': 'Diving', 'out': True},
        {'in': 'Doing', 'out': True},
        {'in': 'Douching', 'out': True},
        {'in': 'Dragging', 'out': True},
        {'in': 'Dreaming', 'out': True},
        {'in': 'Drinking', 'out': True},
        {'in': 'Driving', 'out': True},
        {'in': 'Dwelling', 'out': True},
        {'in': 'Dying', 'out': True},
        {'in': 'Eating', 'out': True},
        {'in': 'Expecting', 'out': True},
        {'in': 'Falling', 'out': True},
        {'in': 'Feeling', 'out': True},
        {'in': 'Fighting', 'out': True},
        {'in': 'Finding', 'out': True},
        {'in': 'Fleeing', 'out': True},
        {'in': 'Flinging', 'out': True},
        {'in': 'Flying', 'out': True},
        {'in': 'Focusing', 'out': True},
        {'in': 'Following', 'out': True},
        {'in': 'Forbidding', 'out': True},
        {'in': 'Foreseeing', 'out': True},
        {'in': 'Foretelling', 'out': True},
        {'in': 'Forgetting', 'out': True},
        {'in': 'Forgiving', 'out': True},
        {'in': 'Forsaking', 'out': True},
        {'in': 'Gassing', 'out': True},
        {'in': 'Getting', 'out': True},
        {'in': 'Gilding', 'out': True},
        {'in': 'Giving', 'out': True},
        {'in': 'Going', 'out': True},
        {'in': 'Grinding', 'out': True},
        {'in': 'Happening', 'out': True},
        {'in': 'Having', 'out': True},
        {'in': 'Helping', 'out': True},
        {'in': 'Hewing', 'out': True},
        {'in': 'Hitting', 'out': True},
        {'in': 'Hocusing', 'out': True},
        {'in': 'Holding', 'out': True},
        {'in': 'Hurting', 'out': True},
        {'in': 'Hying', 'out': True},
        {'in': 'Inlaying', 'out': True},
        {'in': 'Insisting', 'out': True},
        {'in': 'Interlaying', 'out': True},
        {'in': 'Irising', 'out': True},
        {'in': 'Keeping', 'out': True},
        {'in': 'Killing', 'out': True},
        {'in': 'Kneeling', 'out': True},
        {'in': 'Knitting', 'out': True},
        {'in': 'Knowing', 'out': True},
        {'in': 'Laying', 'out': True},
        {'in': 'Leading', 'out': True},
        {'in': 'Leaning', 'out': True},
        {'in': 'Leaping', 'out': True},
        {'in': 'Learning', 'out': True},
        {'in': 'Leaving', 'out': True},
        {'in': 'Letting', 'out': True},
        {'in': 'Liking', 'out': True},
        {'in': 'Living', 'out': True},
        {'in': 'Looking', 'out': True},
        {'in': 'Losing', 'out': True},
        {'in': 'Loving', 'out': True},
        {'in': 'Lying', 'out': True},
        {'in': 'Meaning', 'out': True},
        {'in': 'Meeting', 'out': True},
        {'in': 'Menuing', 'out': True},
        {'in': 'Misleading', 'out': True},
        {'in': 'Mistaking', 'out': True},
        {'in': 'Misunderstanding', 'out': True},
        {'in': 'Moving', 'out': True},
        {'in': 'Needing', 'out': True},
        {'in': 'Nicheing', 'out': True},
        {'in': 'Outvying', 'out': True},
        {'in': 'Overdrawing', 'out': True},
        {'in': 'Overhearing', 'out': True},
        {'in': 'Overtaking', 'out': True},
        {'in': 'Presetting', 'out': True},
        {'in': 'Providing', 'out': True},
        {'in': 'Proving', 'out': True},
        {'in': 'Psyching', 'out': True},
        {'in': 'Putting', 'out': True},
        {'in': 'Quitting', 'out': True},
        {'in': 'Quizzing', 'out': True},
        {'in': 'Reaching', 'out': True},
        {'in': 'Remaining', 'out': True},
        {'in': 'Remembering', 'out': True},
        {'in': 'Rending', 'out': True},
        {'in': 'Renting', 'out': True},
        {'in': 'Ridding', 'out': True},
        {'in': 'Ringing', 'out': True},
        {'in': 'Rising', 'out': True},
        {'in': 'Riving', 'out': True},
        {'in': 'Sawing', 'out': True},
        {'in': 'Seeking', 'out': True},
        {'in': 'Seeming', 'out': True},
        {'in': 'Shaking', 'out': True},
        {'in': 'Shaving', 'out': True},
        {'in': 'Shedding', 'out': True},
        {'in': 'Shitting', 'out': True},
        {'in': 'Shoeing', 'out': True},
        {'in': 'Showing', 'out': True},
        {'in': 'Shrinking', 'out': True},
        {'in': 'Singing', 'out': True},
        {'in': 'Sinking', 'out': True},
        {'in': 'Sitting', 'out': True},
        {'in': 'Skiing', 'out': True},
        {'in': 'Slaying', 'out': True},
        {'in': 'Sliding', 'out': True},
        {'in': 'Slinking', 'out': True},
        {'in': 'Slitting', 'out': True},
        {'in': 'Smelling', 'out': True},
        {'in': 'Smiting', 'out': True},
        {'in': 'Sneaking', 'out': True},
        {'in': 'Sowing', 'out': True},
        {'in': 'Speaking', 'out': True},
        {'in': 'Speeding', 'out': True},
        {'in': 'Spending', 'out': True},
        {'in': 'Spitting', 'out': True},
        {'in': 'Spoiling', 'out': True},
        {'in': 'Springing', 'out': True},
        {'in': 'Standing', 'out': True},
        {'in': 'Staving', 'out': True},
        {'in': 'Staying', 'out': True},
        {'in': 'Stealing', 'out': True},
        {'in': 'Stinging', 'out': True},
        {'in': 'Stinking', 'out': True},
        {'in': 'Stopping', 'out': True},
        {'in': 'Strewing', 'out': True},
        {'in': 'Striding', 'out': True},
        {'in': 'Stripping', 'out': True},
        {'in': 'Striving', 'out': True},
        {'in': 'Subletting', 'out': True},
        {'in': 'Sunburning', 'out': True},
        {'in': 'Swearing', 'out': True},
        {'in': 'Sweating', 'out': True},
        {'in': 'Sweeping', 'out': True},
        {'in': 'Swelling', 'out': True},
        {'in': 'Swimming', 'out': True},
        {'in': 'Swinging', 'out': True},
        {'in': 'Talking', 'out': True},
        {'in': 'Tearing', 'out': True},
        {'in': 'Thriving', 'out': True},
        {'in': 'Thrusting', 'out': True},
        {'in': 'Treading', 'out': True},
        {'in': 'Undergoing', 'out': True},
        {'in': 'Underlying', 'out': True},
        {'in': 'Understanding', 'out': True},
        {'in': 'Undertaking', 'out': True},
        {'in': 'Upsetting', 'out': True},
        {'in': 'Vexing', 'out': True},
        {'in': 'Vying', 'out': True},
        {'in': 'Waiting', 'out': True},
        {'in': 'Waking', 'out': True},
        {'in': 'Walking', 'out': True},
        {'in': 'Wanting', 'out': True},
        {'in': 'Watching', 'out': True},
        {'in': 'Wearing', 'out': True},
        {'in': 'Weeping', 'out': True},
        {'in': 'Wending', 'out': True},
        {'in': 'Winning', 'out': True},
        {'in': 'Wising', 'out': True},
        {'in': 'Withdrawing', 'out': True},
        {'in': 'Withholding', 'out': True},
        {'in': 'Withstanding', 'out': True},
        {'in': 'Wringing', 'out': True},
        {'in': 'abiding', 'out': True},
        {'in': 'aching', 'out': True},
        {'in': 'arcing', 'out': True},
        {'in': 'arising', 'out': True},
        {'in': 'asking', 'out': True},
        {'in': 'avalanching', 'out': True},
        {'in': 'awakening', 'out': True},
        {'in': 'beating', 'out': True},
        {'in': 'becoming', 'out': True},
        {'in': 'begetting', 'out': True},
        {'in': 'beginning', 'out': True},
        {'in': 'beholding', 'out': True},
        {'in': 'being', 'out': True},
        {'in': 'bellyaching', 'out': True},
        {'in': 'bending', 'out': True},
        {'in': 'betting', 'out': True},
        {'in': 'biasing', 'out': True},
        {'in': 'biting', 'out': True},
        {'in': 'bleeding', 'out': True},
        {'in': 'blitzing', 'out': True},
        {'in': 'blowing', 'out': True},
        {'in': 'breaking', 'out': True},
        {'in': 'bringing', 'out': True},
        {'in': 'building', 'out': True},
        {'in': 'burning', 'out': True},
        {'in': 'bursting', 'out': True},
        {'in': 'busing', 'out': True},
        {'in': 'busting', 'out': True},
        {'in': 'caching', 'out': True},
        {'in': 'caddying', 'out': True},
        {'in': 'canvasing', 'out': True},
        {'in': 'catching', 'out': True},
        {'in': 'caucusing', 'out': True},
        {'in': 'changing', 'out': True},
        {'in': 'choosing', 'out': True},
        {'in': 'chorusing', 'out': True},
        {'in': 'clapping', 'out': True},
        {'in': 'clinging', 'out': True},
        {'in': 'coming', 'out': True},
        {'in': 'continuing', 'out': True},
        {'in': 'costing', 'out': True},
        {'in': 'creching', 'out': True},
        {'in': 'creeping', 'out': True},
        {'in': 'daring', 'out': True},
        {'in': 'dealing', 'out': True},
        {'in': 'digging', 'out': True},
        {'in': 'dissing', 'out': True},
        {'in': 'diving', 'out': True},
        {'in': 'doing', 'out': True},
        {'in': 'douching', 'out': True},
        {'in': 'dragging', 'out': True},
        {'in': 'dreaming', 'out': True},
        {'in': 'drinking', 'out': True},
        {'in': 'driving', 'out': True},
        {'in': 'dwelling', 'out': True},
        {'in': 'dying', 'out': True},
        {'in': 'eating', 'out': True},
        {'in': 'expecting', 'out': True},
        {'in': 'falling', 'out': True},
        {'in': 'feeling', 'out': True},
        {'in': 'fighting', 'out': True},
        {'in': 'finding', 'out': True},
        {'in': 'fleeing', 'out': True},
        {'in': 'flinging', 'out': True},
        {'in': 'flying', 'out': True},
        {'in': 'focusing', 'out': True},
        {'in': 'following', 'out': True},
        {'in': 'forbidding', 'out': True},
        {'in': 'foreseeing', 'out': True},
        {'in': 'foretelling', 'out': True},
        {'in': 'forgetting', 'out': True},
        {'in': 'forgiving', 'out': True},
        {'in': 'forsaking', 'out': True},
        {'in': 'gassing', 'out': True},
        {'in': 'getting', 'out': True},
        {'in': 'gilding', 'out': True},
        {'in': 'giving', 'out': True},
        {'in': 'going', 'out': True},
        {'in': 'grinding', 'out': True},
        {'in': 'happening', 'out': True},
        {'in': 'having', 'out': True},
        {'in': 'helping', 'out': True},
        {'in': 'hewing', 'out': True},
        {'in': 'hitting', 'out': True},
        {'in': 'hocusing', 'out': True},
        {'in': 'holding', 'out': True},
        {'in': 'hurting', 'out': True},
        {'in': 'hying', 'out': True},
        {'in': 'inlaying', 'out': True},
        {'in': 'insisting', 'out': True},
        {'in': 'interlaying', 'out': True},
        {'in': 'irising', 'out': True},
        {'in': 'keeping', 'out': True},
        {'in': 'killing', 'out': True},
        {'in': 'kneeling', 'out': True},
        {'in': 'knitting', 'out': True},
        {'in': 'knowing', 'out': True},
        {'in': 'laying', 'out': True},
        {'in': 'leading', 'out': True},
        {'in': 'leaning', 'out': True},
        {'in': 'leaping', 'out': True},
        {'in': 'learning', 'out': True},
        {'in': 'leaving', 'out': True},
        {'in': 'letting', 'out': True},
        {'in': 'liking', 'out': True},
        {'in': 'living', 'out': True},
        {'in': 'looking', 'out': True},
        {'in': 'losing', 'out': True},
        {'in': 'loving', 'out': True},
        {'in': 'lying', 'out': True},
        {'in': 'meaning', 'out': True},
        {'in': 'meeting', 'out': True},
        {'in': 'menuing', 'out': True},
        {'in': 'misleading', 'out': True},
        {'in': 'mistaking', 'out': True},
        {'in': 'misunderstanding', 'out': True},
        {'in': 'moving', 'out': True},
        {'in': 'needing', 'out': True},
        {'in': 'nicheing', 'out': True},
        {'in': 'outvying', 'out': True},
        {'in': 'overdrawing', 'out': True},
        {'in': 'overhearing', 'out': True},
        {'in': 'overtaking', 'out': True},
        {'in': 'presetting', 'out': True},
        {'in': 'providing', 'out': True},
        {'in': 'proving', 'out': True},
        {'in': 'psyching', 'out': True},
        {'in': 'putting', 'out': True},
        {'in': 'quitting', 'out': True},
        {'in': 'quizzing', 'out': True},
        {'in': 'reaching', 'out': True},
        {'in': 'remaining', 'out': True},
        {'in': 'remembering', 'out': True},
        {'in': 'rending', 'out': True},
        {'in': 'renting', 'out': True},
        {'in': 'ridding', 'out': True},
        {'in': 'ringing', 'out': True},
        {'in': 'rising', 'out': True},
        {'in': 'riving', 'out': True},
        {'in': 'sawing', 'out': True},
        {'in': 'seeking', 'out': True},
        {'in': 'seeming', 'out': True},
        {'in': 'shaking', 'out': True},
        {'in': 'shaving', 'out': True},
        {'in': 'shedding', 'out': True},
        {'in': 'shitting', 'out': True},
        {'in': 'shoeing', 'out': True},
        {'in': 'showing', 'out': True},
        {'in': 'shrinking', 'out': True},
        {'in': 'singing', 'out': True},
        {'in': 'sinking', 'out': True},
        {'in': 'sitting', 'out': True},
        {'in': 'skiing', 'out': True},
        {'in': 'slaying', 'out': True},
        {'in': 'sliding', 'out': True},
        {'in': 'slinking', 'out': True},
        {'in': 'slitting', 'out': True},
        {'in': 'smelling', 'out': True},
        {'in': 'smiting', 'out': True},
        {'in': 'sneaking', 'out': True},
        {'in': 'sowing', 'out': True},
        {'in': 'speaking', 'out': True},
        {'in': 'speeding', 'out': True},
        {'in': 'spending', 'out': True},
        {'in': 'spitting', 'out': True},
        {'in': 'spoiling', 'out': True},
        {'in': 'springing', 'out': True},
        {'in': 'standing', 'out': True},
        {'in': 'staving', 'out': True},
        {'in': 'staying', 'out': True},
        {'in': 'stealing', 'out': True},
        {'in': 'stinging', 'out': True},
        {'in': 'stinking', 'out': True},
        {'in': 'stopping', 'out': True},
        {'in': 'strewing', 'out': True},
        {'in': 'striding', 'out': True},
        {'in': 'stripping', 'out': True},
        {'in': 'striving', 'out': True},
        {'in': 'subletting', 'out': True},
        {'in': 'sunburning', 'out': True},
        {'in': 'swearing', 'out': True},
        {'in': 'sweating', 'out': True},
        {'in': 'sweeping', 'out': True},
        {'in': 'swelling', 'out': True},
        {'in': 'swimming', 'out': True},
        {'in': 'swinging', 'out': True},
        {'in': 'talking', 'out': True},
        {'in': 'tearing', 'out': True},
        {'in': 'thriving', 'out': True},
        {'in': 'thrusting', 'out': True},
        {'in': 'treading', 'out': True},
        {'in': 'undergoing', 'out': True},
        {'in': 'underlying', 'out': True},
        {'in': 'understanding', 'out': True},
        {'in': 'undertaking', 'out': True},
        {'in': 'upsetting', 'out': True},
        {'in': 'vexing', 'out': True},
        {'in': 'vying', 'out': True},
        {'in': 'waiting', 'out': True},
        {'in': 'waking', 'out': True},
        {'in': 'walking', 'out': True},
        {'in': 'wanting', 'out': True},
        {'in': 'watching', 'out': True},
        {'in': 'wearing', 'out': True},
        {'in': 'weeping', 'out': True},
        {'in': 'wending', 'out': True},
        {'in': 'winning', 'out': True},
        {'in': 'wising', 'out': True},
        {'in': 'withdrawing', 'out': True},
        {'in': 'withholding', 'out': True},
        {'in': 'withstanding', 'out': True},
        {'in': 'wringing', 'out': True},
    ]

    def test_verb_is_pres_part(self):
        for test_case in self.test_args:
            with self.subTest():
                # Expand test_case with default cases, if optional keys are not provided
                test_case = {**test_case, **{
                    "desc": f"is_pres_part({repr(test_case['in'])}) => {repr(test_case['out'])}",
                    "kwargs": dict()
                }}
                self.assertEqual(Verb(test_case["in"]).is_pres_part(**test_case["kwargs"]), test_case["out"], test_case["desc"])


if __name__ == "__main__":
    unittest.main()

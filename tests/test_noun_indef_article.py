
#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
## NOTE: This module was autogenerated. ##
## Contains no user-servicable parts!!! ##
##########################################

import unittest

from inflex import Noun


class TestSelectIndefiniteArticle(unittest.TestCase):
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
        {'in': 'A', 'out': 'an'},
        {'in': 'A.B.C', 'out': 'an'},
        {'in': 'AGE', 'out': 'an'},
        {'in': 'AI', 'out': 'an'},
        {'in': 'Ath', 'out': 'an'},
        {'in': 'B', 'out': 'a'},
        {'in': 'B.L.T. sandwich', 'out': 'a'},
        {'in': 'BLANK', 'out': 'a'},
        {'in': 'BMW', 'out': 'a'},
        {'in': 'Bth', 'out': 'a'},
        {'in': 'Burmese restaurant', 'out': 'a'},
        {'in': 'C', 'out': 'a'},
        {'in': 'C.O.', 'out': 'a'},
        {'in': 'CAPITAL', 'out': 'a'},
        {'in': 'CCD', 'out': 'a'},
        {'in': 'COLON', 'out': 'a'},
        {'in': 'Cth', 'out': 'a'},
        {'in': 'D', 'out': 'a'},
        {'in': 'D.S.M.', 'out': 'a'},
        {'in': 'DINNER', 'out': 'a'},
        {'in': 'DNR', 'out': 'a'},
        {'in': 'Dth', 'out': 'a'},
        {'in': 'E', 'out': 'an'},
        {'in': 'E.K.G.', 'out': 'an'},
        {'in': 'ECG', 'out': 'an'},
        {'in': 'EGG', 'out': 'an'},
        {'in': 'Eth', 'out': 'an'},
        {'in': 'Euler number', 'out': 'an'},
        {'in': 'F', 'out': 'an'},
        {'in': 'F.A.Q.', 'out': 'an'},
        {'in': 'F.B.I. agent', 'out': 'an'},
        {'in': 'FACT', 'out': 'a'},
        {'in': 'FAQ', 'out': 'a'},
        {'in': 'FSM', 'out': 'an'},
        {'in': 'Fth', 'out': 'an'},
        {'in': 'G', 'out': 'a'},
        {'in': 'G-string', 'out': 'a'},
        {'in': 'GOD', 'out': 'a'},
        {'in': 'GSM phone', 'out': 'a'},
        {'in': 'Governor General', 'out': 'a'},
        {'in': 'Gth', 'out': 'a'},
        {'in': 'H', 'out': 'an'},
        {'in': 'H-Bomb', 'out': 'an'},
        {'in': 'H.A.L. 9000', 'out': 'an'},
        {'in': 'H.M.S Ark Royal', 'out': 'an'},
        {'in': 'HAL 9000', 'out': 'a'},
        {'in': 'HSL colour space', 'out': 'an'},
        {'in': 'Hough transform', 'out': 'a'},
        {'in': 'Hth', 'out': 'an'},
        {'in': 'I', 'out': 'an'},
        {'in': 'I.O.U.', 'out': 'an'},
        {'in': 'IDEA', 'out': 'an'},
        {'in': 'IQ', 'out': 'an'},
        {'in': 'Inspector General', 'out': 'an'},
        {'in': 'Ith', 'out': 'an'},
        {'in': 'J', 'out': 'a'},
        {'in': 'Jth', 'out': 'a'},
        {'in': 'K', 'out': 'a'},
        {'in': 'Kth', 'out': 'a'},
        {'in': 'L', 'out': 'an'},
        {'in': 'L.E.D.', 'out': 'an'},
        {'in': 'LCD', 'out': 'an'},
        {'in': 'LED', 'out': 'a'},
        {'in': 'Lth', 'out': 'an'},
        {'in': 'M', 'out': 'an'},
        {'in': 'M.I.A.', 'out': 'an'},
        {'in': 'MIASMA', 'out': 'a'},
        {'in': 'MTV channel', 'out': 'an'},
        {'in': 'Major General', 'out': 'a'},
        {'in': 'Mth', 'out': 'an'},
        {'in': 'N', 'out': 'an'},
        {'in': 'N.C.O.', 'out': 'an'},
        {'in': 'NATO country', 'out': 'a'},
        {'in': 'NCO', 'out': 'an'},
        {'in': 'Nth', 'out': 'an'},
        {'in': 'O', 'out': 'an'},
        {'in': 'O.K.', 'out': 'an'},
        {'in': 'OK', 'out': 'an'},
        {'in': 'OLE', 'out': 'an'},
        {'in': 'Oth', 'out': 'an'},
        {'in': 'P', 'out': 'a'},
        {'in': 'P.E.T. scan', 'out': 'a'},
        {'in': 'PET', 'out': 'a'},
        {'in': 'Ph.D.', 'out': 'a'},
        {'in': 'Pth', 'out': 'a'},
        {'in': 'Q', 'out': 'a'},
        {'in': 'Qth', 'out': 'a'},
        {'in': 'R', 'out': 'an'},
        {'in': 'R.S.V.P.', 'out': 'an'},
        {'in': 'REST', 'out': 'a'},
        {'in': 'RSVP', 'out': 'an'},
        {'in': 'Rth', 'out': 'an'},
        {'in': 'S', 'out': 'an'},
        {'in': 'S.O.S.', 'out': 'an'},
        {'in': 'SST', 'out': 'an'},
        {'in': 'SUM', 'out': 'a'},
        {'in': 'Sth', 'out': 'an'},
        {'in': 'T', 'out': 'a'},
        {'in': 'T.N.T. bomb', 'out': 'a'},
        {'in': 'TENT', 'out': 'a'},
        {'in': 'TNT bomb', 'out': 'a'},
        {'in': 'Tth', 'out': 'a'},
        {'in': 'U', 'out': 'a'},
        {'in': 'U-boat', 'out': 'a'},
        {'in': 'U.F.O.', 'out': 'a'},
        {'in': 'UFO', 'out': 'a'},
        {'in': 'UK citizen', 'out': 'a'},
        {'in': 'UNESCO representative', 'out': 'a'},
        {'in': 'Uth', 'out': 'a'},
        {'in': 'V', 'out': 'a'},
        {'in': 'V.I.P.', 'out': 'a'},
        {'in': 'VIPER', 'out': 'a'},
        {'in': 'Vth', 'out': 'a'},
        {'in': 'W', 'out': 'a'},
        {'in': 'Wth', 'out': 'a'},
        {'in': 'X', 'out': 'an'},
        {'in': 'X-ray', 'out': 'an'},
        {'in': 'X.O.', 'out': 'an'},
        {'in': 'XY chromosome', 'out': 'an'},
        {'in': 'XYLAPHONE', 'out': 'a'},
        {'in': 'Xth', 'out': 'an'},
        {'in': 'Y', 'out': 'a'},
        {'in': 'Y-shaped pipe', 'out': 'a'},
        {'in': 'Y.Z. plane', 'out': 'a'},
        {'in': 'YBLENT eye', 'out': 'an'},
        {'in': 'YMCA', 'out': 'a'},
        {'in': 'Yth', 'out': 'a'},
        {'in': 'Z', 'out': 'a'},
        {'in': 'Zth', 'out': 'a'},
        {'in': 'a-th', 'out': 'an'},
        {'in': 'agendum', 'out': 'an'},
        {'in': 'aide-de-camp', 'out': 'an'},
        {'in': 'albino', 'out': 'an'},
        {'in': 'b-th', 'out': 'a'},
        {'in': 'bacterium', 'out': 'a'},
        {'in': 'c-th', 'out': 'a'},
        {'in': 'cameo', 'out': 'a'},
        {'in': 'd-th', 'out': 'a'},
        {'in': 'dynamo', 'out': 'a'},
        {'in': 'e-th', 'out': 'an'},
        {'in': 'embryo', 'out': 'an'},
        {'in': 'erratum', 'out': 'an'},
        {'in': 'eucalyptus', 'out': 'a'},
        {'in': 'eulogy', 'out': 'a'},
        {'in': 'euphemism', 'out': 'a'},
        {'in': 'euphoria', 'out': 'a'},
        {'in': 'ewe', 'out': 'a'},
        {'in': 'ewer', 'out': 'a'},
        {'in': 'extremum', 'out': 'an'},
        {'in': 'eye', 'out': 'an'},
        {'in': 'f-th', 'out': 'an'},
        {'in': 'fish', 'out': 'a'},
        {'in': 'g-th', 'out': 'a'},
        {'in': 'genus', 'out': 'a'},
        {'in': 'h-th', 'out': 'an'},
        {'in': 'has-been', 'out': 'a'},
        {'in': 'height', 'out': 'a'},
        {'in': 'heir', 'out': 'an'},
        {'in': 'honed blade', 'out': 'a'},
        {'in': 'honest man', 'out': 'an'},
        {'in': 'honeymoon', 'out': 'a'},
        {'in': 'honorarium', 'out': 'an'},
        {'in': 'honorary degree', 'out': 'an'},
        {'in': 'honoree', 'out': 'an'},
        {'in': 'honorific', 'out': 'an'},
        {'in': 'hound', 'out': 'a'},
        {'in': 'hour', 'out': 'an'},
        {'in': 'hourglass', 'out': 'an'},
        {'in': 'houri', 'out': 'a'},
        {'in': 'house', 'out': 'a'},
        {'in': 'inferno', 'out': 'an'},
        {'in': 'j-th', 'out': 'a'},
        {'in': 'jumbo', 'out': 'a'},
        {'in': 'k-th', 'out': 'a'},
        {'in': 'knife', 'out': 'a'},
        {'in': 'l-th', 'out': 'an'},
        {'in': 'lady in waiting', 'out': 'a'},
        {'in': 'leaf', 'out': 'a'},
        {'in': 'm-th', 'out': 'an'},
        {'in': 'n-th', 'out': 'an'},
        {'in': 'note', 'out': 'a'},
        {'in': 'o-th', 'out': 'an'},
        {'in': 'octavo', 'out': 'an'},
        {'in': 'octopus', 'out': 'an'},
        {'in': 'okay', 'out': 'an'},
        {'in': 'once-and-future-king', 'out': 'a'},
        {'in': 'oncologist', 'out': 'an'},
        {'in': 'one night stand', 'out': 'a'},
        {'in': 'onerous task', 'out': 'an'},
        {'in': 'opera', 'out': 'an'},
        {'in': 'optimum', 'out': 'an'},
        {'in': 'opus', 'out': 'an'},
        {'in': 'ox', 'out': 'an'},
        {'in': 'p-th', 'out': 'a'},
        {'in': 'plateau', 'out': 'a'},
        {'in': 'q-th', 'out': 'a'},
        {'in': 'quantum', 'out': 'a'},
        {'in': 'r-th', 'out': 'an'},
        {'in': 'reindeer', 'out': 'a'},
        {'in': 's-th', 'out': 'an'},
        {'in': 'salmon', 'out': 'a'},
        {'in': 't-th', 'out': 'a'},
        {'in': 'thought', 'out': 'a'},
        {'in': 'tomato', 'out': 'a'},
        {'in': 'u-th', 'out': 'a'},
        {'in': 'ubiquity', 'out': 'a'},
        {'in': 'unicorn', 'out': 'a'},
        {'in': 'unidentified flying object', 'out': 'an'},
        {'in': 'uniform', 'out': 'a'},
        {'in': 'unimodal system', 'out': 'a'},
        {'in': 'unimpressive record', 'out': 'an'},
        {'in': 'uninformed opinion', 'out': 'an'},
        {'in': 'uninvited guest', 'out': 'an'},
        {'in': 'union', 'out': 'a'},
        {'in': 'uniplex', 'out': 'a'},
        {'in': 'uniprocessor', 'out': 'a'},
        {'in': 'unique opportunity', 'out': 'a'},
        {'in': 'unisex hairdresser', 'out': 'a'},
        {'in': 'unison', 'out': 'a'},
        {'in': 'unit', 'out': 'a'},
        {'in': 'unitarian', 'out': 'a'},
        {'in': 'united front', 'out': 'a'},
        {'in': 'unity', 'out': 'a'},
        {'in': 'univalent bond', 'out': 'a'},
        {'in': 'univariate statistic', 'out': 'a'},
        {'in': 'universe', 'out': 'a'},
        {'in': 'unordered meal', 'out': 'an'},
        {'in': 'uranium atom', 'out': 'a'},
        {'in': 'urban myth', 'out': 'an'},
        {'in': 'urbane miss', 'out': 'an'},
        {'in': 'urchin', 'out': 'an'},
        {'in': 'urea detector', 'out': 'a'},
        {'in': 'urethane monomer', 'out': 'a'},
        {'in': 'urge', 'out': 'an'},
        {'in': 'urgency', 'out': 'an'},
        {'in': 'urinal', 'out': 'a'},
        {'in': 'urn', 'out': 'an'},
        {'in': 'usage', 'out': 'a'},
        {'in': 'use', 'out': 'a'},
        {'in': 'usher', 'out': 'an'},
        {'in': 'usual suspect', 'out': 'a'},
        {'in': 'usurer', 'out': 'a'},
        {'in': 'usurper', 'out': 'a'},
        {'in': 'utensil', 'out': 'a'},
        {'in': 'utility', 'out': 'a'},
        {'in': 'utmost urgency', 'out': 'an'},
        {'in': 'utopia', 'out': 'a'},
        {'in': 'utterance', 'out': 'an'},
        {'in': 'v-th', 'out': 'a'},
        {'in': 'viper', 'out': 'a'},
        {'in': 'w-th', 'out': 'a'},
        {'in': 'x-th', 'out': 'an'},
        {'in': 'xenophobe', 'out': 'a'},
        {'in': 'y-th', 'out': 'a'},
        {'in': 'yblent eye', 'out': 'an'},
        {'in': 'yclad body', 'out': 'an'},
        {'in': 'yellowing', 'out': 'a'},
        {'in': 'yield', 'out': 'a'},
        {'in': 'youth', 'out': 'a'},
        {'in': 'ypsiliform junction', 'out': 'an'},
        {'in': 'yttrium atom', 'out': 'an'},
        {'in': 'z-th', 'out': 'a'},
        {'in': 'zoo', 'out': 'a'},
    ]

    def test_select_indefinite_article(self):
        for test_case in self.test_args:
            with self.subTest():
                # Expand test_case with default cases, if optional keys are not provided
                test_case = {**test_case, **{
                    "desc": f"indef_article({repr(test_case['in'])}) => {repr(test_case['out'])}",
                    "kwargs": {}
                }}
                self.assertEqual(Noun(test_case["in"]).indef_article(**test_case["kwargs"]), test_case["out"], test_case["desc"])


if __name__ == "__main__":
    unittest.main()

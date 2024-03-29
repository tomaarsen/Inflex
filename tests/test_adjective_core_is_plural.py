
#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
## NOTE: This module was autogenerated. ##
## Contains no user-servicable parts!!! ##
##########################################

import unittest

from inflex import Adjective


class TestAdjectiveIsSingular(unittest.TestCase):
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
        {'in': 'A', 'out': False},
        {'in': 'An', 'out': False},
        {'in': 'Her', 'out': False},
        {'in': 'His', 'out': False},
        {'in': 'Its', 'out': False},
        {'in': 'My', 'out': False},
        {'in': 'Our', 'out': True},
        {'in': 'Some', 'out': True},
        {'in': 'That', 'out': False},
        {'in': 'Their', 'out': True},
        {'in': 'These', 'out': True},
        {'in': 'This', 'out': False},
        {'in': 'Those', 'out': True},
        {'in': 'Your', 'out': True},
        {'in': 'a', 'out': False},
        {'in': 'an', 'out': False},
        {'in': 'her', 'out': False},
        {'in': 'his', 'out': False},
        {'in': 'its', 'out': False},
        {'in': 'my', 'out': False},
        {'in': 'our', 'out': True},
        {'in': 'some', 'out': True},
        {'in': 'that', 'out': False},
        {'in': 'their', 'out': True},
        {'in': 'these', 'out': True},
        {'in': 'this', 'out': False},
        {'in': 'those', 'out': True},
        {'in': 'your', 'out': True},
    ]

    def test_adjective_is_singular(self):
        for test_case in self.test_args:
            with self.subTest():
                # Expand test_case with default cases, if optional keys are not provided
                test_case = {**test_case, **{
                    "desc": f"is_plural({repr(test_case['in'])}) => {repr(test_case['out'])}",
                    "kwargs": {}
                }}
                self.assertEqual(Adjective(test_case["in"]).is_plural(**test_case["kwargs"]), test_case["out"], test_case["desc"])


if __name__ == "__main__":
    unittest.main()

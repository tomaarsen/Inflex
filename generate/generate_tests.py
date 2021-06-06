
import json

class TestWriter(object):
    def __init__(self, test_class):
        super().__init__()
        self.test_class = test_class
        self.import_folder_name = "inflex"
        # TODO: Improve paths
        self.test_folder_name = "tests"
        self.test_file_format = """
#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################
## NOTE: This module was autogenerated. ##
## Contains no user-servicable parts!!! ##
##########################################

import unittest

from {import_folder_name} import {test_class}


class Test{test_name_pascal}(unittest.TestCase):
    '''
    test_args has the format [
        {{
            "in":     ..., # (required)
            "out":    ..., # (required)
            "desc":   ..., # (optional)
            "kwargs": ...  # (optional)
        }}, ...
    ]
    '''
    test_args = {test_args}

    def test_{test_name_snake}(self):
        for test_case in self.test_args:
            with self.subTest():
                # Expand test_case with default cases, if optional keys are not provided
                test_case = {{**test_case, **{{
                    "desc": f"{test_function}({{repr(test_case['in'])}}) => {{repr(test_case['out'])}}",
                    "kwargs": {{}}
                }}}}
                self.assertEqual({test_class}(test_case["in"]).{test_function}(**test_case["kwargs"]), test_case["out"], test_case["desc"])


if __name__ == "__main__":
    unittest.main()
"""

    def _format_test_args(self, test_args):
        """
        Give test_args a nicer formatting.
        Note that we don't use json.dumps as it will eg. turn "True" into "true".

        This also removes duplicates
        """
        return "[\n" + "".join(sorted({f"        {test_case},\n" for test_case in test_args})) + "    ]"

    def write_test(self, test_path, test_function, test_name_pascal, test_args):
        with open(test_path, "w+") as f:
            f.write(self.test_file_format.format(import_folder_name=self.import_folder_name,
                                                 test_class=self.test_class,
                                                 test_name_snake="".join([f"_{char.lower()}" if char.isupper() else char for char in test_name_pascal])[1:],
                                                 test_function=test_function,
                                                 test_name_pascal=test_name_pascal,
                                                 test_args=self._format_test_args(test_args)))

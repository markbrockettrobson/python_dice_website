import unittest

import python_dice_website.src.ci_test_funtion as ci_test_funtion


class TestCIAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(4, ci_test_funtion.AddStuff.add(1, 3))

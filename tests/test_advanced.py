# -*- coding: utf-8 -*-
__author__ = 'dvirdi'

from .context import sample

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        sample.hmm()


if __name__ == '__main__':
    unittest.main()

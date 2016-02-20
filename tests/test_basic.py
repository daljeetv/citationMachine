
__author__ = 'dvirdi'

# -*- coding: utf-8 -*-

import os


import unittest
from src import citationmachine

class CitationTestCase(unittest.TestCase):
    """Basic test cases."""

    def call_citationmachine(self, web_site):
        parser = citationmachine.get_parser()
        args = vars(parser.parse_args(web_site.split(' ')))
        return citationmachine.citationmachine(args)

    def setUp(self):
        self.websites = ['www.lesswrong.com',
                        'www.gwern.net',]
        self.advanced_websites = ['news.ycombinator.com']
        self.bad_websites = ['moe',
                            'mel']

    def tearDown(self):
        pass

    def test_answers(self):
        self.assertTrue(self.call_citationmachine(self.websites[0]))


if __name__ == '__main__':
    unittest.main()
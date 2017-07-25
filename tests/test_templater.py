import unittest

from fuzza.templater import Templater


class TestTemplater(unittest.TestCase):

    def test_empty_template_renders_data_directly(self):
        config = {}
        t = Templater(config)

        data = ['1', '2', '3']

        self.assertListEqual(
            list(t.render(data)),
            data)

    def test_template_substitution(self):
        config = {}
        t = Templater(config)

        data = ['1', '2', '3']
        # Patch the templater
        t._template = ['$fuzzdata abc', 'def $fuzzdata']

        expected = [
            '1 abc', '2 abc', '3 abc',
            'def 1', 'def 2', 'def 3'
        ]

        self.assertListEqual(
            list(t.render(data)),
            expected)

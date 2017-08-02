import unittest

from fuzza.templater import render


class TestTemplater(unittest.TestCase):

    def test_empty_template_renders_data_directly(self):
        templates = []
        data = [b'1', b'2', b'3']

        self.assertListEqual(
            list(render(templates, data)),
            data
        )

    def test_template_substitution(self):
        templates = [
            b'$fuzzdata abc',
            b'def $fuzzdata'
        ]
        data = [b'1', b'2', b'3']

        expected = [
            b'1 abc', b'2 abc', b'3 abc',
            b'def 1', b'def 2', b'def 3'
        ]
        self.assertListEqual(
            list(render(templates, data)),
            expected
        )

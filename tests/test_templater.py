import unittest

from fuzza.templater import Templater


class TestTemplater(unittest.TestCase):

    def test_empty_template_renders_data_directly(self):
        config = {}
        t = Templater(config)

        data = [b'1', b'2', b'3']

        self.assertListEqual(
            list(t.render(data)),
            data
        )

    def test_template_substitution(self):
        config = {}
        t = Templater(config)

        data = [b'1', b'2', b'3']
        # Patch the templater
        t._template = [b'$fuzzdata abc', b'def $fuzzdata']

        expected = [
            b'1 abc', b'2 abc', b'3 abc',
            b'def 1', b'def 2', b'def 3'
        ]
        self.assertListEqual(
            list(t.render(data)),
            expected
        )

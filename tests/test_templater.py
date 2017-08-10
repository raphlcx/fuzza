import unittest

from pathlib import Path

from fuzza.templater import read
from fuzza.templater import render


class TestTemplater(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = Path(__file__) / '..' / '_testdata' / 'template' / '*'
        path = str(path.resolve())
        cls.template_path = path

    def test_able_to_read_template_from_files(self):
        # Involves file IO
        config = {
            'template_path': self.template_path
        }
        templates = read(config)
        expected = [
            b'This is a template $fuzzdata\n',
            b'31 32 $fuzzdata 33 34\n'
        ]
        self.assertListEqual(
            templates,
            expected
        )

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

import unittest

from pathlib import Path

from fuzza.configuration import _get_cfile_path
from fuzza.configuration import from_file
from fuzza.configuration import load
from fuzza.configuration import to_file


class TestConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = Path(__file__) / '..' / '_testdata' / 'configuration'
        path = str(path.resolve())
        cls.conf_path = path

    def test_configuration_loading(self):
        config = {
            'a': 1,
            'b': 2
        }
        conf = load(config)

        self.assertDictEqual(
            conf,
            config
        )

    def test_get_configuration_file_path(self):
        self.assertEqual(
            str(_get_cfile_path('/abc/path1', 'yaml')),
            '/abc/path1/fuzza.cfg.yaml'
        )

    def test_empty_configuration_value_is_not_included(self):
        config = {
            'a': 1,
            'b': '',
            'c': None
        }
        conf = load(config)

        self.assertDictEqual(
            conf,
            {'a': 1}
        )

    def test_configuration_to_and_from_file(self):
        # Involves file IO
        config = {
            'a': 1,
            'b': 'somestring',
            'c': True
        }
        to_file(config, self.conf_path)
        conf_from_file = from_file(self.conf_path)

        self.assertDictEqual(
            config,
            conf_from_file
        )

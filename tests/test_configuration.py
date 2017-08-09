import unittest

from fuzza.configuration import _get_cfile_path
from fuzza.configuration import load


class TestConfiguration(unittest.TestCase):

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

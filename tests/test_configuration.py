import unittest

from fuzza.configuration import Configuration
from fuzza.exception import ClassNotInstantiableError


class TestConfiguration(unittest.TestCase):

    def tearDown(self):
        Configuration.CONFIG = {}

    def test_class_instantiation_fails(self):
        with self.assertRaises(ClassNotInstantiableError):
            Configuration()

    def test_configuration_loading(self):
        config = {
            'a': 1,
            'b': 2
        }
        Configuration.load(config)

        self.assertDictEqual(
            Configuration.CONFIG,
            config)

    def test_configuration_get(self):
        config = {
            'a': 1,
            'b': 2
        }
        Configuration.load(config)

        self.assertEqual(
            Configuration.get('a'),
            config.get('a'))

    def test_get_configuration_file_path(self):
        self.assertEqual(
            str(Configuration.get_cfile_path('/abc/path1', 'yaml')),
            '/abc/path1/fuzza.conf.yaml')

    def test_empty_configuration_value_is_not_included(self):
        config = {
            'a': 1,
            'b': '',
            'c': None
        }
        Configuration.load(config)

        self.assertDictEqual(
            Configuration.CONFIG,
            {'a': 1})

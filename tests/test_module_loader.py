import unittest

from fuzza.module_loader import load_module


class ModuleLoaderTest(unittest.TestCase):

    def test_none_name_loads_default_module(self):
        module = load_module(
            None,
            '',
            'sys'
        )
        self.assertEqual(
            module.__name__,
            'sys'
        )

    def test_load_module_with_prefix_concatenation(self):
        module = load_module(
            'util',
            'importlib.',
            ''
        )
        self.assertEqual(
            module.__name__,
            'importlib.util'
        )

    def test_load_module_with_matching_name(self):
        module = load_module(
            'base64',
            '',
            ''
        )
        self.assertEqual(
            module.__name__,
            'base64'
        )

    def test_name_clash_stdlib_favors_built_in_module(self):
        module = load_module(
            'base64',
            'fuzza.transformer._',
            ''
        )
        self.assertEqual(
            module.__name__,
            'fuzza.transformer._base64'
        )

import unittest

from fuzza.protocol import init


class TestProtocol(unittest.TestCase):

    def test_dynamic_module_import_success(self):
        config = {
            'protocol': 'binary'
        }
        adapt = init(config)
        expected = 'fuzza.protocol._binary'

        self.assertEqual(
            adapt.__closure__[0].cell_contents.__name__,
            expected
        )

    def test_empty_protocol_config_defaults_to_textual(self):
        adapt = init({})
        expected = 'fuzza.protocol._textual'

        self.assertEqual(
            adapt.__closure__[0].cell_contents.__name__,
            expected
        )

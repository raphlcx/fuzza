import unittest

from fuzza.protocol import init


class TestProtocol(unittest.TestCase):

    def test_dynamic_module_import_success(self):
        proto_module = 'fuzza.protocol._binary'
        config = {
            'protocol': proto_module
        }
        adapt = init(config)

        self.assertEqual(
            adapt.__closure__[0].cell_contents.__name__,
            proto_module
        )

    def test_empty_protocol_config_defaults_to_textual(self):
        proto_module = 'fuzza.protocol._textual'
        adapt = init({})

        self.assertEqual(
            adapt.__closure__[0].cell_contents.__name__,
            proto_module
        )

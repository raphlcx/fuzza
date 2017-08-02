import unittest

from fuzza.protocol import Protocol


class TestProtocol(unittest.TestCase):

    def test_dynamic_module_import_success(self):
        proto_module = 'fuzza.protocol._binary'
        config = {
            'protocol': proto_module
        }
        proto = Protocol(config)

        self.assertEqual(
            proto._loaded_protocol_adapter.__name__,
            proto_module
        )

    def test_empty_protocol_config_defaults_to_textual(self):
        proto_module = 'fuzza.protocol._textual'
        proto = Protocol({})

        self.assertEqual(
            proto._loaded_protocol_adapter.__name__,
            proto_module
        )

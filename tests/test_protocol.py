import unittest

from fuzza.protocol import Protocol


class TestProtocol(unittest.TestCase):

    def test_textual_protocol_conversion(self):
        config = {
            'protocol': 'textual'
        }
        p = Protocol(config)
        data = b'this is string'

        self.assertEqual(
            p.convert(data),
            data)

    def test_binary_protocol_conversion(self):
        config = {
            'protocol': 'binary'
        }
        p = Protocol(config)
        data = b'7468697320697320737472696e67'
        expected = b'this is string'

        self.assertEqual(
            p.convert(data),
            expected)

    def test_default_protocol_on_empty_config(self):
        p = Protocol({})

        # Protocol shoud default to something when it is not specified
        self.assertIsNotNone(p._protocol)

    def test_binary_protocol_strip_whitespace(self):
        config = {
            'protocol': 'binary'
        }
        p = Protocol(config)
        data = b'74 68 69 73 20\n69 73 20 73\n74 72 69 6e\n67'
        expected = b'this is string'

        self.assertEqual(
            p.convert(data),
            expected)

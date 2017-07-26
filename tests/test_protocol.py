import unittest

from fuzza.protocol import Protocol


class TestProtocol(unittest.TestCase):

    def test_textual_protocol_conversion(self):
        config = {
            'protocol': 'textual'
        }
        p = Protocol(config)
        data = 'this is string'

        self.assertEqual(
            p.convert(data),
            data)

    def test_binary_protocol_conversion(self):
        config = {
            'protocol': 'binary'
        }
        p = Protocol(config)
        data = '7468697320697320737472696e67'
        expected = 'this is string'

        self.assertEqual(
            p.convert(data),
            expected)

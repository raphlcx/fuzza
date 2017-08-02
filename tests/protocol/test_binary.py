import unittest

from fuzza.protocol._binary import adapt


class TestProtocolBinary(unittest.TestCase):

    def test_binary_adapter_decodes_hex_string(self):
        data = b'7468697320697320737472696e67'
        expected = b'this is string'

        self.assertEqual(
            adapt(data),
            expected)

    def test_binary_adapter_strip_whitespace(self):
        data = b'74 68 69 73 20\n69 73 20 73\n74 72 69 6e\n67'
        expected = b'this is string'

        self.assertEqual(
            adapt(data),
            expected)

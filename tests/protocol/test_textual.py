import unittest

from fuzza.protocol._textual import adapt


class TestProtocolTextual(unittest.TestCase):

    def test_textual_adapter_returns_original_data(self):
        data = b'this is string'
        self.assertEqual(
            adapt(data),
            data
        )

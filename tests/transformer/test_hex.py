import unittest

from fuzza.transformer._hex import transform


class TestTransformerHex(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = [
            b'this is string',
            b'aaa',
            b'kkoopq'
        ]

    def test_hex_encode_correctly(self):
        expected = [
            b'7468697320697320737472696e67',
            b'616161',
            b'6b6b6f6f7071'
        ]
        self.assertListEqual(
            transform(self.data),
            expected
        )

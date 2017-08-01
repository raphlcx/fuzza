import unittest

from fuzza.encoder._hex import encode


class TestEncoderHex(unittest.TestCase):

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
            encode(self.data),
            expected
        )

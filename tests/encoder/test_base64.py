import unittest

from fuzza.encoder._base64 import encode


class TestEncoderBase64(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = [
            b'this is string',
            b'aaa',
            b'kkoopq'
        ]

    def test_base64_encode_correctly(self):
        expected = [
            b'dGhpcyBpcyBzdHJpbmc=',
            b'YWFh',
            b'a2tvb3Bx'
        ]
        self.assertListEqual(
            encode(self.data),
            expected
        )

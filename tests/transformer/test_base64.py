import unittest

from fuzza.transformer._base64 import transform


class TestTransformerBase64(unittest.TestCase):

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
            transform(self.data),
            expected
        )

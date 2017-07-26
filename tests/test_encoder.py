import unittest

from fuzza.encoder import Encoder


class TestEncoder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = [
            'this is string',
            'aaa',
            'kkoopq'
        ]

    def test_base64_encoding(self):
        config = {
            'encoding': ['base64']
        }
        e = Encoder(config)

        expected = [
            'dGhpcyBpcyBzdHJpbmc=',
            'YWFh',
            'a2tvb3Bx'
        ]
        self.assertListEqual(
            e.encode(self.data),
            expected)

    def test_hex_encoding(self):
        config = {
            'encoding': ['hex']
        }
        e = Encoder(config)

        expected = [
            '7468697320697320737472696e67',
            '616161',
            '6b6b6f6f7071'
        ]
        self.assertListEqual(
            e.encode(self.data),
            expected)

    def test_encoder_chaining(self):
        # Apply base64 encoding,
        # and then hex encoding on the resulting value
        config = {
            'encoding': ['base64', 'hex']
        }
        e = Encoder(config)

        expected = [
            '64476870637942706379427a64484a70626d633d',
            '59574668',
            '6132747662334278'
        ]
        self.assertListEqual(
            e.encode(self.data),
            expected)

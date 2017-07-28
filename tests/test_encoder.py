import unittest

from fuzza.encoder import Encoder


class TestEncoder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = [
            b'this is string',
            b'aaa',
            b'kkoopq'
        ]

    def test_base64_encoding(self):
        config = {
            'encoding': ['base64']
        }
        e = Encoder(config)

        expected = [
            b'dGhpcyBpcyBzdHJpbmc=',
            b'YWFh',
            b'a2tvb3Bx'
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
            b'7468697320697320737472696e67',
            b'616161',
            b'6b6b6f6f7071'
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
            b'64476870637942706379427a64484a70626d633d',
            b'59574668',
            b'6132747662334278'
        ]
        self.assertListEqual(
            e.encode(self.data),
            expected)

    def test_empty_encoding_config_returns_original_data(self):
        e = Encoder({})

        self.assertListEqual(
            e.encode(self.data),
            self.data)

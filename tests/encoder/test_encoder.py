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

    def test_dynamic_module_import_success(self):
        encoders = [
            'fuzza.encoder._base64',
            'fuzza.encoder._hex'
        ]
        config = {
            'encoder': encoders
        }
        enc = Encoder(config)

        self.assertListEqual(
            [ld_enc.__name__ for ld_enc in enc._loaded_encoder],
            encoders
        )

    def test_encoder_able_to_chain(self):
        encoders = [
            'fuzza.encoder._base64',
            'fuzza.encoder._hex'
        ]
        config = {
            'encoder': encoders
        }
        enc = Encoder(config)

        expected = [
            b'64476870637942706379427a64484a70626d633d',
            b'59574668',
            b'6132747662334278'
        ]
        self.assertListEqual(
            enc.encode(self.data),
            expected
        )

    def test_empty_encoder_config_returns_original_data(self):
        enc = Encoder({})

        self.assertListEqual(
            enc.encode(self.data),
            self.data
        )

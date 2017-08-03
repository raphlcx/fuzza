import unittest

from fuzza.encoder import init


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
        encode = init(config)

        self.assertListEqual(
            [
                enc_mod.__name__
                for enc_mod in encode.__closure__[0].cell_contents
            ],
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
        encode = init(config)

        expected = [
            b'64476870637942706379427a64484a70626d633d',
            b'59574668',
            b'6132747662334278'
        ]
        self.assertListEqual(
            encode(self.data),
            expected
        )

    def test_empty_encoder_config_returns_original_data(self):
        encode = init({})

        self.assertListEqual(
            encode(self.data),
            self.data
        )

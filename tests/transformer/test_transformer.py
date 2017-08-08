import unittest

from fuzza.transformer import init


class TestTransformer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = [
            b'this is string',
            b'aaa',
            b'kkoopq'
        ]

    def test_dynamic_module_import_success(self):
        config = {
            'transformer': ['base64', 'hex']
        }
        transform = init(config)
        expected = [
            'fuzza.transformer._base64',
            'fuzza.transformer._hex'
        ]

        self.assertListEqual(
            [
                tfm_mod.__name__
                for tfm_mod in transform.__closure__[0].cell_contents
            ],
            expected
        )

    def test_transformer_able_to_chain(self):
        config = {
            'transformer': ['base64', 'hex']
        }
        transform = init(config)
        expected = [
            b'64476870637942706379427a64484a70626d633d',
            b'59574668',
            b'6132747662334278'
        ]
        self.assertListEqual(
            transform(self.data),
            expected
        )

    def test_empty_transformer_config_returns_original_data(self):
        transform = init({})

        self.assertListEqual(
            transform(self.data),
            self.data
        )

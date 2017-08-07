import unittest

from fuzza.dispatcher import init


class TestDispatcher(unittest.TestCase):

    def test_dynamic_module_import_success(self):
        config = {
            'dispatcher': 'tcp'
        }
        dispatch = init(config)
        expected = 'fuzza.dispatcher._tcp'

        self.assertEqual(
            dispatch.__closure__[1].cell_contents.__name__,
            expected
        )

    def test_empty_dispatcher_config_defaults_to_tcp(self):
        dispatch = init({})
        expected = 'fuzza.dispatcher._tcp'

        self.assertEqual(
            dispatch.__closure__[1].cell_contents.__name__,
            expected
        )

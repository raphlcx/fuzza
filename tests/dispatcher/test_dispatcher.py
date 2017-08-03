import unittest

from fuzza.dispatcher import init


class TestDispatcher(unittest.TestCase):

    def test_dynamic_module_import_success(self):
        dispatcher = 'fuzza.dispatcher._tcp'
        config = {
            'dispatcher': dispatcher
        }
        dispatch = init(config)

        self.assertEqual(
            dispatch.__closure__[1].cell_contents.__name__,
            dispatcher
        )

    def test_empty_dispatcher_config_defaults_to_tcp(self):
        dispatcher = 'fuzza.dispatcher._tcp'
        dispatch = init({})

        self.assertEqual(
            dispatch.__closure__[1].cell_contents.__name__,
            dispatcher
        )

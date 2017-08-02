import unittest

from fuzza.dispatcher import Dispatcher


class TestDispatcher(unittest.TestCase):

    def test_dynamic_module_import_success(self):
        disp_module = 'fuzza.dispatcher._tcp'
        config = {
            'dispatcher': disp_module
        }
        disp = Dispatcher(config)

        self.assertEqual(
            disp._loaded_dispatcher.__name__,
            disp_module
        )

    def test_empty_dispatcher_config_defaults_to_tcp(self):
        disp_module = 'fuzza.dispatcher._tcp'
        disp = Dispatcher({})

        self.assertEqual(
            disp._loaded_dispatcher.__name__,
            disp_module
        )

    def test_dispatcher_receives_target_host_port(self):
        config = {
            'host': 'samplehost',
            'port': 1000
        }
        disp = Dispatcher(config)
        expected = ('samplehost', 1000)

        self.assertTupleEqual(
            disp._target,
            expected
        )

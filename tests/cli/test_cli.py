import unittest

from click.testing import CliRunner

from fuzza.configuration import from_file
from fuzza.cli import cli


class TestCLI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()
        cls.prompt_input = '127.0.0.1\n80\ndata/*'

    def test_init_subcommand_prompt_input(self):
        # Involves file IO

        with self.runner.isolated_filesystem() as tmpdir:
            result = self.runner.invoke(
                cli,
                ['init'],
                self.prompt_input
            )
            self.assertEqual(result.exit_code, 0)

            conf = from_file(tmpdir)
            self.assertEqual(conf.get('host'), '127.0.0.1')
            self.assertEqual(conf.get('port'), 80)
            self.assertEqual(conf.get('data_path'), 'data/*')

    def test_init_subcommand_sets_flag_argument_default_value(self):
        # Involves file IO

        with self.runner.isolated_filesystem() as tmpdir:
            result = self.runner.invoke(
                cli,
                ['init'],
                self.prompt_input
            )
            self.assertEqual(result.exit_code, 0)

            conf = from_file(tmpdir)
            self.assertFalse(conf.get('data_chunk'))
            self.assertFalse(conf.get('dispatcher_reuse'))

    def test_init_subcommand_sets_flag_argument_value_when_specified(self):
        # Invovles file IO

        with self.runner.isolated_filesystem() as tmpdir:
            result = self.runner.invoke(
                cli,
                [
                    'init',
                    '-c',
                    '-r'
                ],
                self.prompt_input
            )
            self.assertEqual(result.exit_code, 0)

            conf = from_file(tmpdir)
            self.assertTrue(conf.get('data_chunk'))
            self.assertTrue(conf.get('dispatcher_reuse'))

    def test_init_subcommand_sets_single_value_argument_options(self):
        # Invovles file IO

        with self.runner.isolated_filesystem() as tmpdir:
            result = self.runner.invoke(
                cli,
                [
                    'init',
                    '--host', '127.0.0.1',
                    '--port', '80',
                    '--data-path', 'data/*',
                    '--template-path', 'sample.template',
                    '--dispatcher', 'tcp',
                    '--protocol', 'binary'
                ]
            )
            self.assertEqual(result.exit_code, 0)

            conf = from_file(tmpdir)
            self.assertEqual(conf.get('host'), '127.0.0.1')
            self.assertEqual(conf.get('port'), 80)
            self.assertEqual(conf.get('data_path'), 'data/*')
            self.assertEqual(conf.get('template_path'), 'sample.template')
            self.assertEqual(conf.get('dispatcher'), 'tcp')
            self.assertEqual(conf.get('protocol'), 'binary')

    def test_init_subcommand_sets_multi_value_argument_options(self):
        # Involves file IO

        with self.runner.isolated_filesystem() as tmpdir:
            result = self.runner.invoke(
                cli,
                [
                    'init',
                    '--transformer', 'hex,base64'
                ],
                self.prompt_input
            )
            self.assertEqual(result.exit_code, 0)

            conf = from_file(tmpdir)
            self.assertListEqual(
                conf.get('transformer'),
                [
                    'hex', 'base64'
                ]
            )

import io

from pathlib import Path

from ruamel import yaml

from .exception import ClassNotInstantiableError


class Configuration(object):
    """
    A static object for storing operational configurations.
    """

    CONFIG = {}
    FILENAME = 'fuzza.conf'

    def __new__(cls):
        raise ClassNotInstantiableError(
            "Attempting to initialize non-instantiable class `{}'"
            .format(cls.__name__))

    @staticmethod
    def get_cfile_path(directory, extension):
        """
        Returns the path to configuration file.

        Args:
            directory: Directory containing the configuration file.
            extension: The extension of the configuration file.

        Returns:
            Resolved path to the configuration file.
        """
        return (
            Path(directory) /
            (Configuration.FILENAME + '.' + extension)
        ).resolve()

    @staticmethod
    def load(config):
        """
        Load configuration into the static configuration object.

        Args:
            config: A `dict` containing the configurtions.
        """
        Configuration.CONFIG.update(config)

    @staticmethod
    def get(key):
        """
        Retrieve configuration value.

        Args:
            key: Key to access the configuration value.

        Returns:
            The value associated with the supplied key.
        """
        return Configuration.CONFIG.get(key)

    @staticmethod
    def to_file(directory='', extension='yaml'):
        """
        Store configurations to file.

        Args:
            directory: Directory to store the configuration file.
                Defaults to empty string, which is the current
                directory of script execution.
            extension: The extension determining the configuration
                file format. Defaults to 'yaml'.
        """
        cfile = Configuration.get_cfile_path(directory, extension)

        with io.open(cfile, 'w') as f:
            if extension == 'yaml':
                yaml.dump(Configuration.CONFIG,
                          f,
                          Dumper=yaml.RoundTripDumper,
                          allow_unicode=True,
                          explicit_start=True)

    @staticmethod
    def from_file(directory='', extension='yaml'):
        """
        Load configuration from file.

        Args:
            directory: Directory containing the configuration file.
                Defaults to empty string, which is the current
                directory of script execution.
            extension: The extension determining the configuration
                file format. Defaults to 'yaml'.
        """
        cfile = Configuration.get_cfile_path(directory, extension)

        conf = {}
        with io.open(cfile, 'r') as f:
            if extension == 'yaml':
                conf = yaml.load(f, Loader=yaml.RoundTripLoader)
                conf = dict(conf)

        Configuration.load(conf)

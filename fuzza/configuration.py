from pathlib import Path

from ruamel.yaml import YAML

from .exception import ClassNotInstantiableError


class Configuration(object):
    """
    A static object for storing operational configurations.

    This class is essentially a global object holding the configuration
    values. Hence, it should never be mutated after it has benn set
    initially.

    Future improvemnet may use an immutable `dict` to hold the
    configuration values.

    Raises:
        ClassNotInstantiableError: If this class is attempted to be
            instantiated.
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
            Path to the configuration file.
        """
        return (
            Path(directory) /
            (Configuration.FILENAME + '.' + extension)
        )

    @staticmethod
    def load(config):
        """
        Load configuration into the static configuration object.

        Args:
            config: A `dict` containing the configurations.
        """
        for key, value in config.items():
            if value is not None and value != '':
                Configuration.CONFIG[key] = value

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

        if extension == 'yaml':
            yaml = YAML(pure=True)
            yaml.dump(Configuration.CONFIG, cfile)

    @staticmethod
    def from_file(directory='', extension='yaml'):
        """
        Read configurations from file.

        Args:
            directory: Directory containing the configuration file.
                Defaults to empty string, which is the current
                directory of script execution.
            extension: The extension determining the configuration
                file format. Defaults to 'yaml'.

        Returns:
            The configurations read from file.
        """
        cfile = Configuration.get_cfile_path(directory, extension)

        conf = {}
        if extension == 'yaml':
            yaml = YAML(typ='safe', pure=True)
            conf = yaml.load(cfile)

        return conf

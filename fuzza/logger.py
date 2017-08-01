import logging
import logging.config

from pathlib import Path

from ruamel.yaml import YAML


class Logger(object):
    """
    A static logging class.
    """

    _cfile = Path(__file__) / '..' / '..' / 'config' / 'logging.conf.yaml'
    _yaml = YAML(typ='safe', pure=True)
    logging.config.dictConfig(
        _yaml.load(_cfile.resolve())
    )

    @staticmethod
    def get_logger(name=None):
        """
        Return a configured logger.

        Args:
            name: The module name.

        Returns:
            The logger instance.
        """
        return logging.getLogger(name)

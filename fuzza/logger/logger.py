"""
fuzza.logger.logger
-------------------

The module is used as a helper to retrieve a configured logger.
"""
import logging
import logging.config

from pathlib import Path

from ruamel.yaml import YAML

logging.config.dictConfig(
    YAML(typ='safe', pure=True).load(
        (
            Path(__file__) /
            '..' /
            'logger.cfg.yaml'
        ).resolve()
    )
)


def get_logger(name=None):
    """
    Return a configured logger.

    Args:
        name (str): The module name.

    Returns:
        The logger instance.
    """
    return logging.getLogger(name)

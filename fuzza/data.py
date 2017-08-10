"""
fuzza.data
----------

This module is used to handle operations related loading and reading of
fuzz data.
"""
import glob
import io
import logging

from .logger import get_logger

LOG = get_logger(__name__)
IS_DEBUG = LOG.isEnabledFor(logging.DEBUG)


def read(config):
    """
    Read data from data files.

    The file contents are currently loaded eagerly when this function is
    invoked. Therefore, a large memory space may be required if there
    are a lot of data.

    Args:
        config (dict): The fuzzer configuration.

    Returns:
        list: The list of data.
    """
    data_chunk = config.get('data_chunk') or False
    LOG.info(
        'Read data in chunk: %s', data_chunk
    )

    data_path = config.get('data_path')
    data = []

    for dfile in glob.iglob(data_path):
        with io.open(dfile, 'rb') as f:
            if data_chunk:
                data.append(f.read())
            else:
                data += f.read().splitlines()

    LOG.info(
        'Found %d data from %s',
        len(data),
        data_path
    )

    return data

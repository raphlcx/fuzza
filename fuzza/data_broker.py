import glob
import io
import logging

from .logger import Logger

LOGGER = Logger.get_logger(__name__)
IS_DEBUG = LOGGER.isEnabledFor(logging.DEBUG)


class DataBroker(object):
    """
    Read data from data files.

    Args:
        config: A `dict` containing the fuzzer configurations.

    Attributes:
        _data_path: Path to data files as specified in configuration.
        _data: A list of data loaded from data files.
    """

    def __init__(self, config):
        self._data_path = config.get('data_path')
        self._data = []

    def scan(self):
        """
        Scan data path data files and store the data file content to
        a data store.

        The contents are currently loaded eagerly when this method is
        invoked. Therefore, a large memory space may be required if
        there are numerous data.
        """
        for df in glob.iglob(self._data_path):
            with io.open(df, 'rb') as f:
                self._data += f.read().splitlines()

        LOGGER.info(
            'Found %d data from %s',
            len(self._data),
            self._data_path
        )

    @property
    def data(self):
        """The list containing loaded data contents."""
        return self._data

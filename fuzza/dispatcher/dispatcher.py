"""
fuzza.dispatcher.dispatcher
---------------------------

This module is used to dynamically import dispatcher modules.
"""
import importlib
import logging

from ..logger import get_logger

LOGGER = get_logger(__name__)
IS_DEBUG = LOGGER.isEnabledFor(logging.DEBUG)


class Dispatcher(object):
    """
    A generic dispatcher class that loads relevant dispatchers.

    This currently supports only the use of one dispatcher in a single
    fuzzing session.

    Args:
        config (dict): The fuzzer configuration.
    """

    def __init__(self, config):

        #: Dispatcher specified in configuration, default to
        #: using TCP dispatcher
        self._dispatcher = config.get('dispatcher') or \
            __package__ + '._tcp'

        #: Imported module for dispatcher
        self._loaded_dispatcher = importlib.import_module(self._dispatcher)

        LOGGER.info(
            'Dispatcher to use: %s',
            self._loaded_dispatcher.__name__
        )

        #: Dispatcher target
        self._target = (
            config.get('host'),
            config.get('port')
        )

        LOGGER.info(
            'Dispatch target: %s',
            self._target
        )

        #: Connection instance
        self._con = None

    def connect(self):
        """
        Establish a connection with the target.
        """
        self._con = self._loaded_dispatcher.connect(self._target)

    def dispatch(self, payload):
        """
        Dispatch payload to target.

        Args:
            payload (str): The payload in bytes literals.

        Returns:
            str: The received responses, in bytes literals, from after
                the dispatching.
        """
        return self._loaded_dispatcher.dispatch(self._con, payload)

    def close(self):
        """
        Close the connection to the target.
        """
        self._loaded_dispatcher.close(self._con)

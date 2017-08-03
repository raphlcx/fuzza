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


def init(config):
    """
    Load relevant dispatcher module.

    Args:
        config (dict): The fuzzer configuration.

    Returns:
        function: The dispatching function.
    """

    # Dispatcher specified in configuration, default to
    # using TCP dispatcher
    dispatcher = config.get('dispatcher') or (__package__ + '._tcp')

    # Imported module for dispatcher
    dispatcher_module = importlib.import_module(dispatcher)

    LOGGER.info(
        'Dispatcher to use: %s',
        dispatcher_module.__name__
    )

    # Dispatcher target
    target = (
        config.get('host'),
        config.get('port')
    )

    LOGGER.info(
        'Dispatch target: %s',
        target
    )

    # # Connection instance
    # con = None

    def dispatch(payload):
        """
        Dispatch payload to target.

        Args:
            payload (str): The payload in bytes literals.

        Returns:
            str: The received responses, in bytes literals, from after
                the dispatching.
        """
        LOGGER.info('Sending > %s', payload)

        con = dispatcher_module.connect(target)
        response = dispatcher_module.dispatch(con, payload)
        dispatcher_module.close(con)

        LOGGER.info('Received > %s', response)

    return dispatch

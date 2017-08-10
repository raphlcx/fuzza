"""
fuzza.dispatcher.dispatcher
---------------------------

This module is used to dynamically import dispatcher modules.
"""
import logging

from ..logger import get_logger
from ..module_loader import load_module

LOG = get_logger(__name__)
IS_DEBUG = LOG.isEnabledFor(logging.DEBUG)


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
    dispatcher = config.get('dispatcher')

    # Imported module for dispatcher
    dispatcher_module = load_module(
        dispatcher,
        __package__ + '._',
        __package__ + '._tcp'
    )

    LOG.info(
        'Dispatcher to use: %s',
        dispatcher_module.__name__
    )

    # Option of whether dispatcher connection should be reused,
    # default to ``False``
    reuse = config.get('dispatcher_reuse') or False

    LOG.info(
        'Dispatcher connection reuse: %s',
        reuse
    )

    # Dispatcher target
    target = (
        config.get('host'),
        config.get('port')
    )
    LOG.info(
        'Dispatch target: %s',
        target
    )

    # Connection instance
    con = None

    def dispatch(payload, ensure_close=False):
        """
        Dispatch payload to target. Target connection is established
        and closed on every session if connection reuse is not enabled.

        Args:
            payload (str): The payload in bytes literals.
            ensure_close (bool): ``True`` if connection has to be
                closed, ``False`` otherwise. Defaults to ``False``.

        Returns:
            str: The received responses, in bytes literals, from after
                the dispatching.
        """
        LOG.info('Sending %d bytes > %s', len(payload), payload)

        nonlocal con

        # Establish the connection,
        # if connection reuse is disabled
        # or it is the first session being established
        if not reuse or con is None:
            con = dispatcher_module.connect(target)

        # Dispatch payload and retrieve the response
        response = dispatcher_module.dispatch(con, payload)

        # Close the connection
        # if connection reuse is disabled
        # or it is ensured to be closed
        if not reuse or ensure_close:
            dispatcher_module.close(con)

        LOG.info('Received %d bytes > %s', len(response), response)

    return dispatch

"""
fuzza.protocol.protocol
-----------------------

This module is used to dynamically import protocol adapter modules.
"""
import importlib
import logging

from ..logger import Logger

LOGGER = Logger.get_logger(__name__)
IS_DEBUG = LOGGER.isEnabledFor(logging.DEBUG)


class Protocol(object):
    """
    A generic protocol class that loads relevant protocol adapters.

    Args:
        config (dict): The fuzzer configuration.
    """

    def __init__(self, config):

        #: Communication protocol type of target communication,
        #: default to using textual adapter
        self._protocol = config.get('protocol') or \
            __package__ + '._textual'

        #: Imported module for protocol adapter
        self._loaded_protocol_adapter = importlib.import_module(
            self._protocol
        )

        LOGGER.info(
            'Target communication protocol: %s',
            self._loaded_protocol_adapter.__name__
        )

    def adapt(self, payload):
        """
        Adapt the payload to bytes representation.

        Args:
            payload (str): Payload in bytes literals.

        Returns:
            str: Bytes reprsentation of payload.
        """
        return self._loaded_protocol_adapter.adapt(payload)

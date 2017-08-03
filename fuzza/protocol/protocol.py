"""
fuzza.protocol.protocol
-----------------------

This module is used to dynamically import protocol adapter modules.
"""
import importlib
import logging

from ..logger import get_logger

LOGGER = get_logger(__name__)
IS_DEBUG = LOGGER.isEnabledFor(logging.DEBUG)


def init(config):
    """
    Load relevant protocol adapter module.

    Args:
        config (dict): The fuzzer configuration.

    Returns:
        function: The protocol adapter function.
    """

    # Communication protocol type of target communication,
    # default to using textual adapter
    protocol = config.get('protocol') or (__package__ + '._textual')

    # Imported module for protocol adapter
    protocol_module = importlib.import_module(protocol)

    LOGGER.info(
        'Target communication protocol: %s',
        protocol_module.__name__
    )

    def adapt(payload):
        """
        Adapt the payload to bytes representation.

        Args:
            payload (str): Payload in bytes literals.

        Returns:
            str: Bytes reprsentation of payload.
        """
        return protocol_module.adapt(payload)

    return adapt

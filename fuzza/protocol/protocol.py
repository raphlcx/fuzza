"""
fuzza.protocol.protocol
-----------------------

This module is used to dynamically import protocol adapter modules.
"""
import logging

from ..logger import get_logger
from ..module_loader import load_module

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
    protocol = config.get('protocol')

    # Imported module for protocol adapter
    protocol_module = load_module(
        protocol,
        __package__ + '._',
        __package__ + '._textual'
    )

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

"""
fuzza.encoder.encoder
---------------------

This module is used to dynamically import encoder modules.
"""
import importlib
import logging

from copy import deepcopy

from ..logger import get_logger

LOGGER = get_logger(__name__)
IS_DEBUG = LOGGER.isEnabledFor(logging.DEBUG)


def init(config):
    """
    Load relevant encoder modules.

    Args:
        config (dict): The fuzzer configuration.

    Returns:
        function: The encoding function.
    """

    # Encoders specified in configuration
    encoder = config.get('encoder') or []

    # Imported modules for each of the encoder
    encoder_modules = [
        importlib.import_module(enc)
        for enc in encoder
    ]

    LOGGER.info(
        'Encoders to apply: %s',
        [enc_mod.__name__ for enc_mod in encoder_modules]
    )

    def encode(data):
        """
        Chain encode data using the encoders specified.

        Args:
            data (list): A list of data in bytes literals.

        Returns:
            list: A list of encoded data in bytes literals.
        """
        data_tmp = deepcopy(data)

        for enc_mod in encoder_modules:
            data_tmp = enc_mod.encode(data_tmp)

        return data_tmp

    return encode

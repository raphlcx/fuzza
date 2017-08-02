"""
fuzza.encoder.encoder
---------------------

This module is used to dynamically import encoder modules.
"""
import importlib
import logging

from copy import deepcopy

from ..logger import Logger

LOGGER = Logger.get_logger(__name__)
IS_DEBUG = LOGGER.isEnabledFor(logging.DEBUG)


class Encoder(object):
    """
    A generic encoder class that loads relevant encoders.

    Args:
        config (dict): The fuzzer configuration.
    """

    def __init__(self, config):

        #: Encoders specified in configuration
        self._encoder = config.get('encoder') or []

        #: Imported modules for each of the encoder
        self._loaded_encoder = [
            importlib.import_module(enc)
            for enc in self._encoder
        ]

        LOGGER.info(
            'Encoders to apply: %s',
            [ld_enc.__name__ for ld_enc in self._loaded_encoder]
        )

    def encode(self, data):
        """
        Encode data in a chain using the encoders specified.

        Args:
            data (list): A list of data in bytes literals.

        Returns:
            list: A list of encoded data in bytes literals.
        """
        data_tmp = deepcopy(data)

        for ld_enc in self._loaded_encoder:
            data_tmp = ld_enc.encode(data_tmp)

        return data_tmp

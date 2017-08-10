"""
fuzza.transformer.transformer
-----------------------------

This module is used to dynamically import transformer modules.
"""
import logging

from copy import deepcopy

from ..logger import get_logger
from ..module_loader import load_module

LOG = get_logger(__name__)
IS_DEBUG = LOG.isEnabledFor(logging.DEBUG)


def init(config):
    """
    Load relevant transformer modules.

    Args:
        config (dict): The fuzzer configuration.

    Returns:
        function: The transformation function.
    """

    # Transformers specified in configuration
    transformer = config.get('transformer') or []

    # Imported modules for each of the transformer
    transformer_modules = [
        load_module(
            tfm,
            __package__ + '._',
            ''
        )
        for tfm in transformer
    ]

    LOG.info(
        'Transformers to apply: %s',
        [tfm_mod.__name__ for tfm_mod in transformer_modules]
    )

    def transform(data):
        """
        Chain data transformation using the transformers specified.

        Args:
            data (list): A list of data in bytes literals.

        Returns:
            list: A list of transformed data in bytes literals.
        """
        data_tmp = deepcopy(data)

        for tfm_mod in transformer_modules:
            data_tmp = tfm_mod.transform(data_tmp)

        return data_tmp

    return transform

import base64
import binascii
import logging

from .logger import Logger

LOGGER = Logger.get_logger(__name__)
IS_DEBUG = LOGGER.isEnabledFor(logging.DEBUG)


class Encoder(object):
    """
    Encode data based on the list of encodings specified.

    Args:
        config: A `dict` containing the fuzzer configurations.

    Attributes:
        _encoding: A list containing the specified encodings.
    """
    ACCEPTED_ENCODING = (
        'base64',
        'hex'
    )

    def __init__(self, config):
        self._encoding = config.get('encoding')

        LOGGER.info('Encodings to apply: %s', self._encoding or [])

    def encode(self, data):
        """
        Encode data in a chain based on the encodings specified.

        Args:
            data: The list of data to be encoded.

        Returns:
            The list of data which have gone through encoding.
        """
        if self._encoding is None:
            return data

        data_tmp = data

        for enc in self._encoding:
            if enc == 'base64':
                data_tmp = [base64.b64encode(d) for d in data_tmp]

            if enc == 'hex':
                data_tmp = [binascii.hexlify(d) for d in data_tmp]

        return data_tmp

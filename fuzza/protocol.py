import binascii
import logging
import re

from .logger import Logger

LOGGER = Logger.get_logger(__name__)
IS_DEBUG = LOGGER.isEnabledFor(logging.DEBUG)


class Protocol(object):
    """
    Adapt payload to be transmitted to the type of communication
    protocol used.

    For instance, byte literal containing hex string is converted to
    a byte literal with its binary representation.

    Args:
        config: A `dict` containing the fuzzer configurations.

    Attributes:
        _protocol: The type of communication protocol of the target to
            be fuzzed.
        _re_whitespace: Compiled regular expression pattern for
            whitespace.
    """
    ACCEPTED_PROTOCOL = (
        'textual',  # First one is the default value if none is specified
        'binary'
    )

    def __init__(self, config):
        self._protocol = config.get('protocol') or \
            Protocol.ACCEPTED_PROTOCOL[0]
        self._re_whitespace = re.compile(b'\s')

        LOGGER.info('Target communication protocol: %s', self._protocol)

    def convert(self, data):
        """
        Convert the supplied data to its bianry representation.

        Args:
            data: The string to be converted.

        Returns:
            The converted string in binary representation.
        """
        if self._protocol == 'textual':
            # Payloads for textual protocol are in bytes literals,
            # hence no conversion is needed
            return data

        elif self._protocol == 'binary':
            # When protocol is binary, it is assumed that template
            # and data are both in hex string format, hence conversion
            # is required. Whitespaces are strip prior to conversion
            return binascii.unhexlify(
                re.sub(self._re_whitespace, b'', data)
            )

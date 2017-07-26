import binascii


class Protocol(object):
    """
    Convert non-textual string representation of data to its textual
    representation, e.g. hex string to textual string.

    Args:
        config: A `dict` containing the fuzzer configurations.

    Attributes:
        _protocol: The type of communication protocol of the target to
            be fuzzed.
    """
    ACCEPTED_PROTOCOL = (
        'textual',
        'binary'
    )

    def __init__(self, config):
        self._protocol = config.get('protocol') or 'textual'

    def convert(self, data):
        """
        Convert the supplied string to its textual representation, if
        it is not one.

        Args:
            data: The string to be converted.

        Returns:
            The converted string in textual representation.
        """
        if self._protocol == 'textual':
            # No conversion needed
            return data

        elif self._protocol == 'binary':
            # When protocol is binary, it is assumed that template
            # and data are both in hex string format, hence conversion
            # is required
            return str(
                binascii.unhexlify(bytes(data, 'utf-8')),
                'utf-8'
            )

import base64
import binascii


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
                data_tmp = [
                    str(
                        base64.b64encode(bytes(d, 'utf-8')),
                        'utf-8'
                    )
                    for d in data_tmp
                ]

            if enc == 'hex':
                data_tmp = [
                    str(
                        binascii.hexlify(bytes(d, 'utf-8')),
                        'utf-8'
                    )
                    for d in data_tmp
                ]

        return data_tmp

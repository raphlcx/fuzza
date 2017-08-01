"""
fuzza.encoder._hex
------------------

The hex encoder module.
"""
import binascii


def encode(data):
    """
    Encode data using hex encoding.

    Args:
        data (list): A list of data in bytes literals.

    Returns:
        list: A list of hex-encoded data in bytes literals.
    """
    return [binascii.hexlify(d) for d in data]

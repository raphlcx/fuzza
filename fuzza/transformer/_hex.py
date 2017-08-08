"""
fuzza.transformer._hex
----------------------

The hex encoding transformer module.
"""
import binascii


def transform(data):
    """
    Transform data using hex encoding.

    Args:
        data (list): A list of data in bytes literals.

    Returns:
        list: A list of hex-encoded data in bytes literals.
    """
    return [binascii.hexlify(d) for d in data]

"""
fuzza.protocol._binary
----------------------

The binary protocol adapter module.
"""
import binascii
import re


def adapt(payload):
    """
    Convert hex string to its bytes representation. Whitespaces in the
    hex string are removed prior to conversion.

    Args:
        payload (str): Payload in bytes literals.

    Returns:
        str: The payload in its bytes representation form.
    """
    return binascii.unhexlify(
        re.sub(b'\s', b'', payload)
    )

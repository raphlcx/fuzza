"""
fuzza.protocol._textual
-----------------------

The textual protocol adapter module.
"""


def adapt(payload):
    """
    Return original payload. No adaptation is required as data in
    ``bytes`` type is already a bytes representation.

    Args:
        payload (str): Payload in bytes literals.

    Returns:
        str: The original payload.
    """
    return payload

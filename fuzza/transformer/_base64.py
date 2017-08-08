"""
fuzza.transformer._base64
-------------------------

The base64 encoding transformer module.
"""
import base64


def transform(data):
    """
    Transform data using base64 encoding.

    Args:
        data (list): A list of data in bytes literals.

    Returns:
        list: A list of base64-encoded data in bytes literals.
    """
    return [base64.b64encode(d) for d in data]

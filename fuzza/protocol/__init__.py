"""
fuzza.protocol
--------------

The protocol module for adapting payload to its bytes representation.

For instance, payload containing hex string in bytes literals is
converted to its binary representation in bytes literals.

The naming of this module can be quite a misnomer, since what it does
mainnly is executing encoding conversion on payload to retrieve its
bytes representation.
"""
from .protocol import Protocol

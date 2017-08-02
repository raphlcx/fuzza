"""
fuzza.dispatcher._tcp
---------------------

The TCP dispatcher module.
"""
import socket

#: Socket receive buffer size
BUF_SIZE = 4096


def connect(target):
    """
    Open a TCP connection to the target.

    Args:
        target (tuple): A tuple containing the host in `str` and port
            in `int`.

    Returns:
        The TCP socket object.
    """
    _socket = socket.socket()
    _socket.connect(target)
    return _socket


def dispatch(sock, payload):
    """
    Dispatch payload to the target.

    Args:
        sock: The TCP socket object.
        payload (str): The TCP payload in bytes literals.

    Returns:
        str: The received TCP response in bytes literals.
    """
    sock.send(
        payload + b'\n' if not payload.endswith(b'\n') else payload
    )

    resp = b''
    while True:
        resp_t = sock.recv(BUF_SIZE)
        if not resp_t:
            break
        resp += resp_t

    return resp


def close(sock):
    """
    Close the TCP connection to target.

    Args:
        sock: The TCP socket object.
    """
    sock.close()

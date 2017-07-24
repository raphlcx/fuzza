import socket


class Dispatcher(object):
    """
    Dispatch fuzzing payload to system under test.

    Args:
        config: A `dict` containing the configurations.
    """

    def __init__(self, config):
        self._host = config.get('host')
        self._port = config.get('port')
        self._s = None
        self._buffsize = 4096

    def open(self):
        """
        Create a TCP connection to the target using its host and port.
        """
        self._s = socket.socket()
        self._s.connect(
            (self._host, self._port)
        )

    def dispatch(self, payload):
        """
        Dispatch the payload to target.

        Args:
            payload: The payload string to send to target.

        Returns:
            The response received from target after the dispatch.
        """
        self._s.send(payload + b'\n')
        return self._s.recv(self._buffsize)

    def close(self):
        """
        Close the TCP connection to target.
        """
        self._s.close()

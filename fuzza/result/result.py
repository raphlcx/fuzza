"""
fuzza.result.result
-------------------

This module is used to output a result file containing dispatch
payloads and responses.
"""

# The filename of result file
FILENAME = 'fuzza.result'

def init():

    def store(payload, response):
        """
        Args:
            payload (str): The payload in bytes literals.
            response (str): The response from after the payload dispatching
                in bytes literals.
        """
        pass

    return store

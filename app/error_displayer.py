# errors.py

# # Imports

from flask import jsonify

# # Errors


class InvalidUsage(Exception):
    """Raised upon invalid usage of the API."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Initializes an InvalidUsage exception.

        Arguments:
        - `message`: the error message.
        - `status_code`: the status code.
        - `payload`: an optional payload of the error object.
        """

        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Returns a dictionary representation of the error."""

        d = {'error': {}}
        d['error'] = self.payload or {}
        d['error']['message'] = self.message
        d['error']['status_code'] = self.status_code
        return d

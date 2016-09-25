"""
Custom Exceptions
"""

class MissingFile(Exception):
    """
    Exception raised request is missing the image field
    """
    message = 'Missing image file.'

    def __init__(self, message=None):
        message = message or self.message
        super(MissingFile, self).__init__(message)

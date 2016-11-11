class FCMError(Exception):
    """
    General Error
    """
    pass

class AuthenticationError(FCMError):
    """
    There was an error authenticating the sender
    """
    pass


class FCMServerError(FCMError):
    """
    Internal server error or timeout error on Firebase cloud messaging server
    """
    pass


class FCMBadRequest(FCMError):
    """
    Invalid input
    """
    pass

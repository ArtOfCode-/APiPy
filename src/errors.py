class APIBaseException(BaseException):
    """
    The base exception for any error representing something that went wrong with
    the API itself. Errors encountered in any circumstance not involving an API
    response do not use this base.
    """
    def __init__(self, error_id, error_name, error_message):
        self.id = error_id
        self.name = error_name
        self.message = error_message

    def get_message(self):
        """
        Gets the exception message.
        """
        return "API error #{0} ('{1}'): {2}.".format(self.id, self.name, self.message)


class UnauthorizedAccessException(APIBaseException):
    """
    An API error, representing that the required credentials weren't supplied.
    Usually, this means you need an access token.
    """
    def get_message(self):
        """
        Gets the exception message.
        """
        return "The request was not authorized to take the requested action."


class InvalidRequestTypeException(BaseException):
    """
    Indicated that the given request type was not available for the current
    situation.
    """
    def __init__(self, provided, allowed=None):
        self.allowed_types = ["get", "post"] if allowed is None else allowed
        self.provided_type = provided

    def get_message(self):
        """
        Gets the exception message.
        """
        return "The provided request type '{0}' was not a member of the allowed request types."\
            .format(self.provided_type)

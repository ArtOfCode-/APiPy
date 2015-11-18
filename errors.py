class APIBaseException(BaseException):
    def __init__(self, error_id, error_name, error_message):
        self.id = error_id
        self.name = error_name
        self.message = error_message

class APIUnauthorizedAccessException(APIBaseException):
    pass

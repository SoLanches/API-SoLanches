class SolanchesException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class SolanchesNotFoundError(SolanchesException):
    def __init__(self, message):
        super().__init__(message)


class SolanchesBadRequestError(SolanchesException):
    def __init__(self, message):
        super().__init__(message)


class SolanchesNotAuthorizedError(SolanchesException):
    def __init__(self, message):
        super().__init__(message)


class SolanchesInternalServerError(SolanchesException):
    def __init__(self, message):
        super().__init__(message)

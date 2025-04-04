
class AccessForbiddenException(Exception): 
    def __init__(self, message: str, code: str = "access_forbidden") -> None:
        self.code = code
        self.message = message


class ApplicationException(Exception):
    def __init__(self, message: str, code: str = "application_error") -> None:
        self.code = code
        self.message = message


class InvalidProjectException(Exception):
    def __init__(self, message: str, code: str = "invalid_project") -> None:
        self.code = code
        self.message = message


class InvalidNationException(Exception):
    def __init__(self, message: str, code: str = "invalid_nation") -> None:
        self.code = code
        self.message = message
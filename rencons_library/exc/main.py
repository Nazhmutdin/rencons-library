
class AccessForbiddenException(Exception): 
    def __init__(self, message: str, code: str = "access_forbidden") -> None:
        self.code = code
        self.message = message

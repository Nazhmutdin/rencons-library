
class AccessForbiddenException(Exception): 
    def __init__(self, code: str = "access_forbidden") -> None:
        self.code = code

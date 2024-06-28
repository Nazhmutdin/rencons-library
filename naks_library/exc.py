from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase


__all__ = [
    "CreateDBException",
    "GetDBException",
    "GetManyDBException",
    "UpdateDBException",
    "DeleteDBException",
    "DBServiceException"
]


class CreateDBException(Exception):
    def __init__[Model: DeclarativeBase](self, exc: IntegrityError, model: Model) -> None:
        self.exception = exc
        self.model = model
        self.detail = exc.detail
        
        super().__init__(exc.detail)

    
    @property
    def message(self) -> str:
        return f"already exists in {self._get_item_type()}"

    
    def _get_item_type(self) -> str:
        return self.model.__tablename__


class GetDBException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class GetManyDBException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class UpdateDBException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class DeleteDBException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)


class DBServiceException(Exception):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)

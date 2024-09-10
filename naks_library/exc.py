from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase


__all__ = [
    "CreateDBException",
    "GetDBException",
    "GetManyDBException",
    "UpdateDBException",
    "DeleteDBException"
]


class DBExeption(Exception):
    def __init__[Model: DeclarativeBase](self, orig_exception: IntegrityError, model: Model) -> None:
        self.orig_exception = orig_exception
        self.model = model


    @property
    def message(self) -> str:
        raise self.orig_exception._message()


class CreateDBException(DBExeption): ...


class GetDBException(DBExeption): ...


class GetManyDBException(DBExeption): ...


class UpdateDBException(DBExeption): ...


class DeleteDBException(DBExeption): ...
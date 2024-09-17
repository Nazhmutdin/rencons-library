import typing as t

from sqlalchemy.exc import IntegrityError


__all__ = [
    "InsertDBException",
    "SelectDBException",
    "UpdateDBException",
    "DeleteDBException"
]


_DBException = t.TypeVar("_DBException", bound=IntegrityError)


class DBExeption(Exception):
    def __init__(self, orig_exception: _DBException) -> None:
        self.orig_exception = orig_exception


    @property
    def message(self) -> str:
        return self.orig_exception._message()


class InsertDBException(DBExeption): ...


class SelectDBException(DBExeption): ...


class UpdateDBException(DBExeption): ...


class DeleteDBException(DBExeption): ...

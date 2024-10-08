import typing as t

from sqlalchemy.orm import DeclarativeBase

from naks_library.interfaces import ICrudGateway
from naks_library.common import BaseSelectShema


_CreateDTO = t.TypeVar("_CreateDTO")
_UpdateDTO = t.TypeVar("_UpdateDTO")
_SelectShema = t.TypeVar("_SelectShema", bound=BaseSelectShema)
_DTO = t.TypeVar("_DTO")

_Model = t.TypeVar("_Model", bound=DeclarativeBase)

_Gateway = t.TypeVar("_Gateway", bound=ICrudGateway[_DTO, _CreateDTO, _UpdateDTO])

import typing as t

from sqlalchemy.orm import DeclarativeBase

from naks_library.base_shema import BaseSelectShema
from naks_library.crud_mapper import ICrudGateway

_SelectShema = t.TypeVar("_SelectShema", bound=BaseSelectShema)
_Model = t.TypeVar("_Model", bound=DeclarativeBase)
_DTO = t.TypeVar("_DTO")

_Gateway = t.TypeVar("_Gateway", bound=ICrudGateway)

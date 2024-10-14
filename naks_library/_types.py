import typing as t

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ColumnClause, FromClause

from naks_library.common import BaseSelectShema
from naks_library.selector_filters import AbstractFilter


type FiltersMapKey = str
type FilterArgsDict = dict[str, t.Any]
type FiltersMapType = dict[FiltersMapKey, AbstractFilter]
type SelectAttrsType = list[ColumnClause]
type SelectFromAttrsType = list[FromClause]

_CreateDTO = t.TypeVar("_CreateDTO")
_UpdateDTO = t.TypeVar("_UpdateDTO")
_SelectShema = t.TypeVar("_SelectShema", bound=BaseSelectShema)
_DTO = t.TypeVar("_DTO")

_Model = t.TypeVar("_Model", bound=DeclarativeBase)


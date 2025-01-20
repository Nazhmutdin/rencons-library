import typing as t

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ColumnClause, FromClause, UnaryExpression

from naks_library.common import BaseSelectShema
from naks_library.selector_filters import AbstractFilter


type FiltersMapKey = str
type FiltersMapType = dict[FiltersMapKey, AbstractFilter]
type SelectAttrsType = list[ColumnClause]
type SelectFromAttrsType = list[FromClause]
type OrderByAttrs = list[ColumnClause | UnaryExpression]

_CreateDTO = t.TypeVar("_CreateDTO")
_SelectShema = t.TypeVar("_SelectShema", bound=BaseSelectShema)
_DTO = t.TypeVar("_DTO")

_Model = t.TypeVar("_Model", bound=DeclarativeBase)


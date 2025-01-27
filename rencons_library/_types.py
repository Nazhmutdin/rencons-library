import typing as t

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ColumnClause, FromClause, UnaryExpression

from rencons_library.selector_filters import AbstractFilter


type FiltersMapKey = str
type FiltersMapType = dict[FiltersMapKey, AbstractFilter]
type SelectAttrsType = list[ColumnClause]
type SelectFromAttrsType = list[FromClause]
type OrderByAttrs = list[ColumnClause | UnaryExpression]


_Model = t.TypeVar("_Model", bound=DeclarativeBase)

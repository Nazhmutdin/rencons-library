import typing as t

from sqlalchemy.orm import attributes
import sqlalchemy as sa

from abc import ABC, abstractmethod


DATE_STRING_FORMAT = "%d.%m.%Y"

DATETIME_STRING_FORMAT = "%d.%m.%Y %H:%M:%S.%f%z"


class AbstractFilter(ABC): 

    def __init__(self, column: attributes.InstrumentedAttribute):
        self.column = column


    @abstractmethod
    def dump_expression(self, arg: t.Any) -> sa.BinaryExpression: ...
            

class LikeFilter(AbstractFilter):

    def dump_expression(self, arg: str) -> sa.BinaryExpression:

        return self.column.like(f"%{arg}%")
            

class ILikeFilter(AbstractFilter):

    def dump_expression(self, arg: str) -> sa.BinaryExpression:

        return self.column.ilike(f"%{arg}%")


class LikeAnyFilter(AbstractFilter):

    def dump_expression(self, arg: t.Iterable[str]) -> sa.BinaryExpression:

        return self.column.like(sa.any_([f"%{el}%" for el in arg]))


class ILikeAnyFilter(AbstractFilter):

    def dump_expression(self, arg: t.Iterable[str]) -> sa.BinaryExpression:

        return self.column.ilike(sa.any_([f"%{el}%" for el in arg]))
    

class InFilter(AbstractFilter):

    def dump_expression(self, arg: t.Iterable[t.Any]) -> sa.BinaryExpression:

        return self.column.in_(arg)


class EqualFilter(AbstractFilter):

    def dump_expression(self, arg: t.Any) -> sa.BinaryExpression:

        return self.column == arg


class FromFilter(AbstractFilter):

    def dump_expression(self, arg: t.Any) -> sa.BinaryExpression:

        return self.column > arg


class BeforeFilter(AbstractFilter):

    def dump_expression(self, arg: t.Any) -> sa.BinaryExpression:

        return self.column < arg

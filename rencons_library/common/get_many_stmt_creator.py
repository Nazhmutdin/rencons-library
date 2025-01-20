import typing as t

from sqlalchemy import BinaryExpression, Select, select

from naks_library._types import _Model, FiltersMapType, SelectAttrsType, SelectFromAttrsType, OrderByAttrs


class IGetManyStmtCreator[T: _Model](t.Protocol):
    def __call__(
        self, 
        filter_args: dict
    ) -> Select[T]: ...


class StandartSqlAlchemyGetManyStmtCreator:

    def __init__(
            self,
            filters_map: FiltersMapType,
            select_attrs: SelectAttrsType, 
            select_from_attrs: SelectFromAttrsType,
            order_by_attrs: OrderByAttrs | None = None
        ) -> None:
        self._filters_map = filters_map
        self.select_attrs = select_attrs
        self.select_from_attrs = select_from_attrs
        self.order_by_attrs = order_by_attrs
    

    def __call__(self, filter_args: dict):

        stmt = select(*self.select_attrs).distinct().select_from(
            *self.select_from_attrs
        )

        if self.order_by_attrs:
            stmt = stmt.order_by(*self.order_by_attrs)


        if filter_args:
            stmt = stmt.where(
                *self._get_binary_expressions(filter_args)
            )
        
        return stmt
    

    def _get_binary_expressions(self, filter_args: dict) -> list[BinaryExpression]:
        expressions = []

        for arg_key, arg_value in filter_args.items():
            if arg_key in self._filters_map:
                expressions.append(self._filters_map[arg_key].dump_expression(arg_value)) 
        
        return expressions

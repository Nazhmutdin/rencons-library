import typing as t

from sqlalchemy import ColumnClause, FromClause, BinaryExpression, Select, select, and_, or_, ColumnExpressionArgument
from sqlalchemy.orm.attributes import InstrumentedAttribute

from naks_library._types import _Model
from naks_library.selector_filters import AbstractFilter


type FiltersMapKey = str
type FilterArgsDict = dict[str, t.Any]
type FiltersMapType = dict[FiltersMapKey, AbstractFilter]
type SelectAttrsType = list[ColumnClause]
type SelectFromAttrsType = list[FromClause]


class IGetManyStmtCreator[T: _Model](t.Protocol):
    def __call__(
        self, 
        filter_args: FilterArgsDict, 
        select_attrs: SelectAttrsType,
        select_from_attrs: SelectFromAttrsType
    ) -> Select[T]: ...


class StandartSqlAlchemyGetManyStmtCreator:

    def __init__(
            self,
            filters_map: FiltersMapType,
            and_model_columns: list[InstrumentedAttribute],
            or_model_columns: list[InstrumentedAttribute]
        ) -> None:
        
        self._filters_map = filters_map
        self._and_model_columns = and_model_columns
        self._or_model_columns = or_model_columns
    

    def __call__(
        self, 
        filter_args: FilterArgsDict, 
        select_attrs: SelectAttrsType, 
        select_from_attrs: SelectFromAttrsType 
    ):
        where_expression = self._dump_where_expression(
            self._get_binary_expressions(filter_args)
        )

        stmt = select(*select_attrs).distinct().select_from(
            *select_from_attrs
        )

        if where_expression is not None:
            return stmt.where(where_expression)
        
        return stmt
    

    def _get_binary_expressions(self, filter_args: FilterArgsDict) -> dict[InstrumentedAttribute, BinaryExpression]:
        expressions = {}

        for arg_key, arg_value in filter_args.items():
            if arg_key in self._filters_map:
                expressions[arg_key] = self._filters_map[arg_key].dump_expression(arg_value)
        
        return expressions


    def _dump_where_expression(self, birary_expressions: list[BinaryExpression]) -> ColumnExpressionArgument | None:
        and_expressions, or_expressions = self._sort_expressions(
            birary_expressions
        )
        
        if and_expressions and or_expressions:
            return and_(
                or_(*or_expressions),
                *and_expressions
            )
        
        elif and_expressions:
            return and_(*and_expressions)
        
        elif or_expressions:
            return or_(*or_expressions)
        
        else:
            return None


    def _sort_expressions(self, expressions: dict[str, BinaryExpression]) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
        and_expressions, or_expressions = ([], [])

        for key, expression in expressions.items():
            column = self._filters_map[key].column
            
            if column in self._and_model_columns:
                and_expressions.append(expression)

            elif column in self._or_model_columns:
                or_expressions.append(expression)

            else:
                continue

        return and_expressions, or_expressions

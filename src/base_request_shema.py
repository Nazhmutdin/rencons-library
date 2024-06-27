import typing as t

from pydantic_core import core_schema
from sqlalchemy.orm import DeclarativeBase, attributes
from pydantic import GetCoreSchemaHandler, ValidationInfo, Field
from sqlalchemy import BinaryExpression, ColumnElement, any_, and_, or_

from rencons_library.base_shema import BaseShema


__all__ = [
    "BaseFilter",
    "BaseListFilter",
    "ILikeAnyFilter",
    "InFilter",
    "EqualFilter",
    "FromFilter",
    "BeforeFilter",
    "BaseRequestShema"
]


class BaseFilter: 
    arg: t.Any

    def __init__(self, arg: t.Any) -> None:
        self.arg = arg

        
    def dump_expression(self, column: attributes.InstrumentedAttribute) -> BinaryExpression: ...


    @classmethod
    def validate(cls, value: t.Any, info: ValidationInfo):

        return cls(value)


    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: t.Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls.validate, handler(t.Any), field_name=handler.field_name
        )


class BaseListFilter(BaseFilter): ...
            

class ILikeAnyFilter(BaseListFilter):

    def dump_expression(self, column: attributes.InstrumentedAttribute) -> BinaryExpression:

        return column.ilike(any_(self.arg))
    

class InFilter(BaseListFilter):


    def dump_expression(self, column: attributes.InstrumentedAttribute) -> BinaryExpression:

        return column.in_(self.arg)


class EqualFilter(BaseFilter):


    def dump_expression(self, column: attributes.InstrumentedAttribute) -> BinaryExpression:

        return column == self.arg


class FromFilter(BaseFilter):


    def dump_expression(self, column: attributes.InstrumentedAttribute) -> BinaryExpression:

        return column > self.arg


class BeforeFilter(BaseFilter):
        

    def dump_expression(self, column: attributes.InstrumentedAttribute) -> BinaryExpression:

        return column < self.arg


class BaseRequestShema[Base: DeclarativeBase](BaseShema):
    __and_model_columns__: list[str] = []
    __or_model_columns__: list[str] = []
    __models__: list[type[Base]]

    limit: int = Field(default=100, gt=-1)
    offset: int = Field(default=0, gt=-1)


    def dump_expression(self) -> ColumnElement:
        and_expressions = []
        or_expressions = []

        for key, info in self.model_fields.items():
            if info.serialization_alias:
                model_field: attributes.InstrumentedAttribute | None = self._get_model_field(info.serialization_alias)

                if not model_field:
                    raise ValueError("serialization_alias must be one of model columns name")
                
                shema_value: BaseFilter = getattr(self, key)

                if shema_value == None:
                    continue

                if model_field.name in self.__and_model_columns__:
                    and_expressions.append(
                        shema_value.dump_expression(model_field)
                    )

                elif model_field.name in self.__or_model_columns__:
                    or_expressions.append(
                        shema_value.dump_expression(model_field)
                    )
                else:
                    continue
            
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
            return True
        

    def _get_model_field(self, serialization_alias) -> attributes.InstrumentedAttribute | None:

        for model in self.__models__:

            model_field = getattr(model, serialization_alias, None)

            if isinstance(model_field, attributes.InstrumentedAttribute):
                return model_field
        
        return None

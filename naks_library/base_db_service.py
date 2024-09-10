from uuid import UUID
import typing as t

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import attributes, DeclarativeBase
import sqlalchemy as sa

from naks_library.base_shema import BaseShema
from naks_library.utils import AbstractFilter
from naks_library.exc import *


type FiltersMapKey = str
type FilterArgsDict = dict[str, t.Any]


class BaseDBService[
    DTO, 
    Model: DeclarativeBase, 
    SelectShema: BaseShema,
    CreateShema: BaseShema,
    UpdateShema: BaseShema
]:
    __dto__: type[DTO]
    __model__: type[Model]
    _filters_map: dict[FiltersMapKey, AbstractFilter]
    _select_attrs: list[sa.ColumnClause | Model]
    _select_from_attrs: list[sa.FromClause]
    _and_model_columns: list[attributes.InstrumentedAttribute]
    _or_model_columns: list[attributes.InstrumentedAttribute]


    async def get(self, session: AsyncSession, ident: str | UUID) -> DTO | None:
        try:
            return await self._get(session, ident)
        except IntegrityError as e:
            raise GetDBException(e)
        
    
    async def get_many(self, session: AsyncSession, filters: SelectShema | None = None, limit: int | None = None, offset: int | None = None) -> list[DTO]:
        try:
            return await self._get_many(session, filters, limit, offset)
        except IntegrityError as e:
            raise GetManyDBException(e, self.__model__)


    async def insert(self, session: AsyncSession, *data: CreateShema) -> None:
        try:
            await self._insert(session, data)
        except IntegrityError as e:
            raise CreateDBException(e, self.__model__)


    async def update(self, session: AsyncSession, ident: str | UUID, data: UpdateShema) -> None:
        try:
            await self._update(
                session, 
                ident, 
                data.model_dump(exclude_unset=True)
            )
        except IntegrityError as e:
            raise UpdateDBException(e)


    async def delete(self, session: AsyncSession, *idents: str | UUID) -> None:
        try:
            await self._delete(session, idents)
        except IntegrityError as e:
            raise DeleteDBException(e)


    async def count(self, session: AsyncSession, filters: SelectShema | None = None) -> int:
        try:
            return await self._count(session, filters)
        except IntegrityError as e:
            raise GetDBException(e)


    async def _get(self, session: AsyncSession, ident: UUID | str) -> DTO | None:
        async with session as session:
            stmt = sa.select(self.__model__).where(
                self.ident_column == ident
            )

            res = (await session.execute(stmt)).scalar_one_or_none()
 
            if res:
                return self.__dto__(**res.__dict__)
            
    
    async def _get_many(self, session: AsyncSession, filters: SelectShema | None, limit: int | None, offset: int | None) -> list[DTO]:
        async with session as session:
            stmt = self.dump_base_get_many_stmt(
                filters.model_dump(exclude_none=True, exclude_unset=True) if filters else {}, 
                self._select_attrs,
                self._select_from_attrs
            )

            if limit:
                stmt = stmt.limit(limit)

            if offset:
                stmt = stmt.offset(offset)

            res = (await session.execute(stmt))

            return [self.__dto__(**el[0].__dict__) for el in res]


    async def _insert(self, session: AsyncSession, data: t.Sequence[CreateShema]) -> None:
        async with session as session:
            stmt = sa.insert(self.__model__).values(
                [el.model_dump() for el in data]
            )

            await session.execute(stmt)

            await session.commit()


    async def _update(self, session: AsyncSession, ident: str | UUID, data: dict) -> None:
        async with session as session:
            stmt = sa.update(self.__model__).where(
                self.ident_column == ident
            ).values(
                **data
            )

            await session.execute(stmt)

            await session.commit()


    async def _delete(self, session: AsyncSession, idents: list[str | UUID]) -> None:
        async with session as session:

            for ident in idents:
                stmt = sa.delete(self.__model__).where(
                    self.ident_column == ident
                )
                await session.execute(stmt)
            
            await session.commit()
            
    
    async def _count(self, session: AsyncSession, filters: SelectShema | None):
        async with session as session:
            stmt = self.dump_base_get_many_stmt(
                filters.model_dump(exclude_none=True, exclude_unset=True) if filters else {}, 
                [self.ident_column],
                self._select_from_attrs
            )

            stmt = sa.select(sa.func.count()).select_from(
                stmt.subquery()
            )
 
            return (await session.execute(stmt)).scalar_one()

    
    @property
    def ident_column(self):
        return sa.inspect(self.__model__).primary_key[0]
    

    def _get_binary_expressions(self, filter_args: FilterArgsDict) -> dict[attributes.InstrumentedAttribute, sa.BinaryExpression]:
        expressions = {}

        for arg_key, arg_value in filter_args.items():
            if arg_key in self._filters_map:
                expressions[arg_key] = self._filters_map[arg_key].dump_expression(arg_value)
        
        return expressions


    def dump_where_expression(self, birary_expressions: list[sa.BinaryExpression]) -> sa.ColumnExpressionArgument | None:
        and_expressions, or_expressions = self.sort_expressions(
            birary_expressions
        )
        
        if and_expressions and or_expressions:
            return sa.and_(
                sa.or_(*or_expressions),
                *and_expressions
            )
        
        elif and_expressions:
            return sa.and_(*and_expressions)
        
        elif or_expressions:
            return sa.or_(*or_expressions)
        
        else:
            return None


    def sort_expressions(self, expressions: dict[str, sa.BinaryExpression]) -> tuple[list[sa.BinaryExpression], list[sa.BinaryExpression]]:
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
    

    def dump_base_get_many_stmt(
        self, 
        filter_args: FilterArgsDict, 
        select_attrs: list,
        select_from_attrs: list[sa.FromClause]
    ):
        where_expression = self.dump_where_expression(
            self._get_binary_expressions(filter_args)
        )

        if not filter_args:
            select_from_attrs = [self.__model__]

        stmt = sa.select(*select_attrs).distinct().select_from(
            *select_from_attrs
        )

        if where_expression is not None:
            return stmt.where(where_expression)
        
        return stmt

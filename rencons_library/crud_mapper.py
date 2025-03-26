from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

from rencons_library._types import _Model
from rencons_library.common.get_many_stmt_creator import IGetManyStmtCreator


class SqlAlchemyCrudMapper[T](ABC):
    def __init__[Model: _Model](self, model: type[Model], session: AsyncSession):
        self.__model__ = model
        self.session = session


    async def insert(self, data: dict) -> T:
        stmt = sa.insert(self.__model__).values(**data).returning(self.__model__)

        return self._convert((await self.session.execute(stmt)).scalars().one_or_none())
    

    async def get_by(
        self,
        filter: sa.ColumnElement
    ):
        stmt = sa.select(self.__model__).where(filter)

        return (await self.session.execute(stmt))


    async def get(self, ident: UUID) -> T | None:
        result = (await self.get_by(self.ident_column == ident)).scalars().one_or_none()

        if result:
            return self._convert(result)

        return None
    

    async def get_many(
        self, 
        create_stmt: IGetManyStmtCreator,
        limit: int | None, 
        offset: int | None, 
        filters: dict = {}
    ) -> list[T]:
        stmt = create_stmt(filters)

        if limit:
            stmt = stmt.limit(limit)

        if offset:
            stmt = stmt.offset(offset)

        res = (await self.session.execute(stmt)).scalars().all()

        return [self._convert(el) for el in res]
 

    async def count(self, create_stmt: IGetManyStmtCreator, filters: dict = {}) -> int:
        stmt = create_stmt(filters)

        stmt = sa.select(sa.func.count()).select_from(
            stmt.subquery()
        )

        return (await self.session.execute(stmt)).scalar_one()


    async def update(self, ident: UUID | str, data: dict) -> T:
        stmt = sa.update(self.__model__).where(
            self.ident_column == ident
        ).values(**data).returning(self.__model__)

        return self._convert((await self.session.execute(stmt)).scalars().one_or_none())


    async def delete(self, ident: UUID):
        stmt = sa.delete(self.__model__).where(
            self.ident_column == ident
        )

        await self.session.execute(stmt)


    @property
    def ident_column(self):
        return sa.inspect(self.__model__).primary_key[0]


    @abstractmethod
    def _convert(self, data: _Model) -> T:
        pass

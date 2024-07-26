import typing as t
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa


class CRUDMixin: 

    @classmethod
    async def get(cls, conn: AsyncSession, ident: uuid.UUID | str):
        stmt = cls._dump_get_stmt(ident)
        response = await conn.execute(stmt)
        result = response.scalar_one_or_none()
        return result
        

    @classmethod
    async def get_many(cls, conn: AsyncSession, expression: sa.ColumnExpressionArgument, limit: int, offset: int):
        stmt = cls._dump_get_many_stmt(expression)

        amount = await cls.count(conn, expression)

        if limit:
            stmt = stmt.limit(limit)

        if offset:
            stmt = stmt.offset(offset)
        
        response = await conn.execute(stmt)

        result = response.scalars().all()
        
        return (result, amount)
        

    @classmethod
    async def create(cls, data: list[dict], conn: AsyncSession):
        stmt = cls._dump_create_stmt(
            data
        )

        await conn.execute(stmt)


    @classmethod
    async def update(cls, conn: AsyncSession, ident: uuid.UUID | str, data: dict[str, t.Any]):
        stmt = cls._dump_update_stmt(ident, data)
        await conn.execute(stmt)


    @classmethod
    async def delete(cls, conn: AsyncSession, ident: uuid.UUID | str):
        stmt = cls._dump_delete_stmt(ident)
        await conn.execute(stmt)


    @classmethod
    async def count(cls, conn: AsyncSession, expression: sa.ColumnExpressionArgument | None = None):
        if isinstance(expression, sa.ColumnElement):

            stmt = sa.select(sa.func.count()).select_from(cls).where(expression)

            return (await conn.execute(stmt)).scalar_one()

        else:
            return (await conn.execute(sa.select(sa.func.count()).select_from(cls).distinct())).scalar_one()


    @classmethod
    def _get_column(cls, ident: str | uuid.UUID):
        return sa.inspect(cls).primary_key[0]


    @classmethod
    def _dump_create_stmt(cls, data: list[dict[str, t.Any]]):
        return sa.insert(cls).values(
            data
        )


    @classmethod
    def _dump_get_stmt(cls, ident: str | uuid.UUID):
        return sa.select(cls).where(
            cls._get_column(ident) == ident
        )


    @classmethod
    def _dump_get_many_stmt(cls, expression: sa.ColumnExpressionArgument):
        return sa.select(cls).filter(expression)
    

    @classmethod
    def _dump_update_stmt(cls, ident: str | uuid.UUID, data: dict[str, t.Any]):
        return sa.update(cls).where(
            cls._get_column(ident) == ident
        ).values(
            **data
        )


    @classmethod
    def _dump_delete_stmt(cls, ident: str | uuid.UUID):
        return sa.delete(cls).where(
            cls._get_column(ident) == ident
        )

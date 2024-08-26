import typing as t
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa


class CRUDMixin: 

    @classmethod
    async def get(cls, conn: AsyncSession, ident: uuid.UUID | str):
        stmt = cls.dump_get_stmt(ident)
        response = await conn.execute(stmt)
        result = response.scalar_one_or_none()
        return result
        

    @classmethod
    async def get_many(cls, conn: AsyncSession, expression: sa.ColumnExpressionArgument, limit: int, offset: int):
        stmt = cls.dump_get_many_stmt(expression)

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
        stmt = cls.dump_create_stmt(
            data
        )

        await conn.execute(stmt)


    @classmethod
    async def update(cls, conn: AsyncSession, ident: uuid.UUID | str, data: dict[str, t.Any]):
        stmt = cls.dump_update_stmt(ident, data)
        await conn.execute(stmt)


    @classmethod
    async def delete(cls, conn: AsyncSession, ident: uuid.UUID | str):
        stmt = cls.dump_delete_stmt(ident)
        await conn.execute(stmt)


    @classmethod
    async def count(cls, conn: AsyncSession, expression: sa.ColumnExpressionArgument | None = None):
    
        if expression is not None:

            stmt = cls.get_base_count_stmt(expression).where(expression).distinct()

        else:
            stmt = cls.get_base_count_stmt(expression).distinct()

        return (await conn.execute(stmt)).scalar_one()


    @classmethod
    def get_column(cls, ident: str | uuid.UUID):
        return sa.inspect(cls).primary_key[0]


    @classmethod
    def dump_create_stmt(cls, data: list[dict[str, t.Any]]):
        return sa.insert(cls).values(
            data
        )


    @classmethod
    def dump_get_stmt(cls, ident: str | uuid.UUID):
        return sa.select(cls).where(
            cls.get_column(ident) == ident
        )


    @classmethod
    def dump_get_many_stmt(cls, expression: sa.ColumnExpressionArgument):
        return sa.select(cls).filter(expression)
    

    @classmethod
    def dump_update_stmt(cls, ident: str | uuid.UUID, data: dict[str, t.Any]):
        return sa.update(cls).where(
            cls.get_column(ident) == ident
        ).values(
            **data
        )


    @classmethod
    def dump_delete_stmt(cls, ident: str | uuid.UUID):
        return sa.delete(cls).where(
            cls.get_column(ident) == ident
        )
    

    @classmethod
    def get_base_count_stmt(cls, expression: sa.ColumnExpressionArgument | None):
        return sa.select(sa.func.count()).select_from(cls)

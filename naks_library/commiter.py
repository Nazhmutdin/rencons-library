from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyCommitter:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()


    async def flush(self):
        await self.session.flush()


    async def rollback(self):
        await self.session.rollback()

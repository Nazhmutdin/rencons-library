from typing import Protocol
from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

class ICommitter(Protocol):
    
    @abstractmethod
    async def commit(self):
        raise NotImplementedError


    @abstractmethod
    async def flush(self):
        raise NotImplementedError


    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class SqlAlchemyCommitter(ICommitter):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()


    async def flush(self):
        await self.session.flush()


    async def rollback(self):
        await self.session.rollback()

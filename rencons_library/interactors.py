from uuid import UUID
from typing import TypeVar

from rencons_library.interfaces import ICommitter, ICrudGateway
from rencons_library.common.get_many_stmt_creator import IGetManyStmtCreator


_Gateway = TypeVar("_Gateway", bound=ICrudGateway)


class BaseCreateInteractor[T]:
    def __init__(
        self,
        gateway: _Gateway,
        committer: ICommitter
    ):
        self.gateway = gateway
        self.committer = committer

    
    async def __call__(self, data: T):
        await self.gateway.insert(data.__dict__)

        await self.committer.commit()


class BaseGetInteractor[T]:
    def __init__(
        self,
        gateway: _Gateway
    ):
        self.gateway = gateway

    
    async def __call__(self, ident: UUID) -> T | None:

        return (await self.gateway.get(ident))
    

class BaseSelectInteractor[T]:

    def __init__(
            self,
            create_stmt: IGetManyStmtCreator,
            gateway: _Gateway
        ) -> None:
        self.create_stmt = create_stmt
        self.gateway = gateway


    async def __call__(self, filters: dict | None, limit: int | None, offset: int | None) -> tuple[list[T], int]:

        res = await self.gateway.get_many(
            create_stmt=self.create_stmt,
            limit=limit,
            offset=offset,
            filters=filters
        )

        count = await self.gateway.count(
            create_stmt=self.create_stmt,
            filters=filters
        )

        return (res, count)


class BaseUpdateInteractor:
    def __init__(
        self,
        gateway: _Gateway,
        committer: ICommitter
    ):
        self.gateway = gateway
        self.committer = committer


    async def __call__(self, ident: UUID, data: dict):
        await self.gateway.update(ident, data)

        await self.committer.commit()


class BaseDeleteInteractor:
    def __init__(
        self,
        gateway: _Gateway,
        committer: ICommitter
    ):
        self.gateway = gateway
        self.committer = committer

    
    async def __call__(self, ident: UUID):
        await self.gateway.delete(ident)

        await self.committer.commit()

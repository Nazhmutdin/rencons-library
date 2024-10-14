from uuid import UUID

from naks_library.interfaces import ICommitter, _Gateway
from naks_library._types import _CreateDTO, _UpdateDTO, _DTO, FilterArgsDict
from naks_library.common.get_many_stmt_creator import IGetManyStmtCreator


class BaseCreateInteractor[T: _CreateDTO]:
    def __init__(
        self,
        gateway: _Gateway,
        commiter: ICommitter
    ):
        self.gateway = gateway
        self.commiter = commiter

    
    async def __call__(self, data: T):
        await self.gateway.insert(data)

        await self.commiter.commit()


class BaseGetInteractor[T: _DTO]:
    def __init__(
        self,
        gateway: _Gateway
    ):
        self.gateway = gateway

    
    async def __call__(self, ident: UUID) -> T | None:

        return (await self.gateway.get(ident))
    

class BaseSelectInteractor[T: _DTO]:

    def __init__(
            self,
            create_stmt: IGetManyStmtCreator,
            gateway: _Gateway
        ) -> None:
        self.create_stmt = create_stmt
        self.gateway = gateway


    async def __call__(self, filters: FilterArgsDict | None, limit: int | None, offset: int | None) -> tuple[list[T], int]:

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


class BaseUpdateInteractor[T: _UpdateDTO]:
    def __init__(
        self,
        gateway: _Gateway,
        commiter: ICommitter
    ):
        self.gateway = gateway
        self.commiter = commiter


    async def __call__(self, ident: UUID, data: T):
        await self.gateway.update(ident, data)

        await self.commiter.commit()


class BaseDeleteInteractor:
    def __init__(
        self,
        gateway: _Gateway,
        commiter: ICommitter
    ):
        self.gateway = gateway
        self.commiter = commiter

    
    async def __call__(self, ident: UUID):
        await self.gateway.delete(ident)

        await self.commiter.commit()

from uuid import UUID

from naks_library.interfaces import ICommitter
from naks_library._types import _CreateDTO, _UpdateDTO, _Gateway, _DTO


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

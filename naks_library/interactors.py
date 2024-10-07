from typing import Any
from uuid import UUID

from naks_library.commiter import ICommitter
from naks_library._types import _Gateway


class Interactor[Input, Output]:
    async def __call__(self, input: Input) -> Output: ...


class BaseCreateInteractor:
    def __init__(
        self,
        gateway: _Gateway,
        commiter: ICommitter
    ):
        self.gateway = gateway
        self.commiter = commiter

    
    async def __call__(self, data: Any):
        await self.gateway.insert(data)

        await self.commiter.commit()


class BaseGetInteractor:
    def __init__(
        self,
        gateway: _Gateway
    ):
        self.gateway = gateway

    
    async def __call__(self, ident: UUID):

        return await self.gateway.get(ident)


class BaseUpdateInteractor:
    def __init__(
        self,
        gateway: _Gateway,
        commiter: ICommitter
    ):
        self.gateway = gateway
        self.commiter = commiter

    
    async def __call__(self, ident: UUID, data: Any):
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

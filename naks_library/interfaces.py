from typing import Protocol
from abc import abstractmethod
from uuid import UUID


class ICommitter(Protocol):
    
    @abstractmethod
    async def commit(self): ...


    @abstractmethod
    async def flush(self): ...


    @abstractmethod
    async def rollback(self): ...


class ICrudGateway[DTO, CreateDTO, UpdateDTO](Protocol):
    @abstractmethod
    async def insert(self, data: CreateDTO): ...


    @abstractmethod
    async def get(self, ident: UUID) -> DTO | None: ...


    @abstractmethod
    async def update(self, ident: UUID | str, data: UpdateDTO): ...


    @abstractmethod
    async def delete(self, ident: UUID): ...

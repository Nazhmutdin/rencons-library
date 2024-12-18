from typing import Protocol
from abc import abstractmethod
from uuid import UUID

from naks_library.common.get_many_stmt_creator import IGetManyStmtCreator


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


    async def get_many(
        self, 
        create_stmt: IGetManyStmtCreator,
        limit: int | None, 
        offset: int | None, 
        filters: dict = {}
    ) -> list[DTO]: ...


    async def count(
        self, 
        create_stmt: IGetManyStmtCreator,
        filters: dict = {}
    ) -> int: ...


    @abstractmethod
    async def update(self, ident: UUID | str, data: UpdateDTO): ...


    @abstractmethod
    async def delete(self, ident: UUID): ...

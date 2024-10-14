from typing import Protocol, TypeVar
from abc import abstractmethod
from uuid import UUID

from naks_library._types import FilterArgsDict, _DTO, _CreateDTO, _UpdateDTO
from naks_library.common.get_many_stmt_creator import IGetManyStmtCreator


_Gateway = TypeVar("_Gateway", bound="ICrudGateway[_DTO, _CreateDTO, _UpdateDTO]")


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
        filters: FilterArgsDict = {}
    ) -> list[DTO]: ...


    async def count(
        self, 
        create_stmt: IGetManyStmtCreator,
        filters: FilterArgsDict = {}
    ) -> int: ...


    @abstractmethod
    async def update(self, ident: UUID | str, data: UpdateDTO): ...


    @abstractmethod
    async def delete(self, ident: UUID): ...

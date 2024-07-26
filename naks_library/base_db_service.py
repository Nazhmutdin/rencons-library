from uuid import UUID
import typing as t

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from naks_library.base_request_shema import BaseRequestShema
from naks_library.base_model import CRUDMixin
from naks_library import BaseShema
from naks_library.uows import UOW
from naks_library.exc import *


__all__: list[str] = [
    "BaseDBService"
]


class BaseDBService[
    DTO, 
    Model: CRUDMixin, 
    RequestShema: BaseRequestShema, 
    CreateShema: BaseShema, 
    UpdateShema: BaseShema 
]:
    __dto__: type[DTO]
    __model__: type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.uow = UOW(self.session)


    async def get(self, ident: str | UUID) -> DTO | None:
        try:
            return await self._get(ident)
        except IntegrityError as e:
            raise GetDBException(e)


    async def get_many(self, request_shema: RequestShema) -> tuple[list[DTO], int]:
        try:
            return await self._get_many(request_shema)
        except IntegrityError as e:
            raise GetManyDBException(e)


    async def add(self, *data: CreateShema) -> None:
        try:
            await self._add(data)
        except IntegrityError as e:
            raise CreateDBException(e, self.__model__)


    async def update(self, ident: str | UUID, data: UpdateShema) -> None:
        try:
            await self._update(ident, data)
        except IntegrityError as e:
            raise UpdateDBException(e)


    async def delete(self, *idents: str | UUID) -> None:
        try:
            await self._delete(idents)
        except IntegrityError as e:
            raise DeleteDBException(e)

    
    async def count(self) -> int:
        async with self.uow as uow:

            return await self.__model__.count(uow.session)
            

    async def _get(self, ident: UUID | str) -> DTO | None:
        async with self.uow as uow:

            res = await self.__model__.get(uow.session, ident)

            if res:
                return self.__dto__(**res.__dict__)


    async def _get_many(self, request_shema: RequestShema) -> tuple[list[DTO], int]:
        async with self.uow as uow:
            expression = request_shema.dump_expression()

            result, amount = await self.__model__.get_many(uow.session, expression, request_shema.limit, request_shema.offset)

            if result:
                result = [self.__dto__(**el.__dict__) for el in result]
            
            return (result, amount)


    async def _add(self, data: t.Sequence[CreateShema]) -> None:
        async with self.uow as uow:
            await self.__model__.create(
                [el.model_dump() for el in data], 
                uow.session
            )

            await uow.commit()


    async def _update(self, ident: str | UUID, data: UpdateShema) -> None:
        async with self.uow as uow:
            await self.__model__.update(uow.session, ident, data.model_dump(exclude_unset=True))

            await uow.commit()


    async def _delete(self, idents: list[str | UUID]) -> None:
        async with self.uow as uow:
            for ident in idents:
                await self.__model__.delete(uow.session, ident)
            
            await uow.commit()

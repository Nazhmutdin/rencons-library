from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError

from naks_library.base_model import CRUDMixin
from naks_library.uows import UOW


class BaseTestModel[DTO]:
    __model__: type[CRUDMixin]
    __dto__: type[DTO]

    uow: UOW

    async def test_create(self, items: list[DTO]) -> None:
        async with self.uow as uow:

            insert_data = [
                el.__dict__ for el in items
            ]
            
            await self.__model__.create(
                insert_data,
                conn=uow.session
            )

            for el in items:
                res = await self.__model__.get(uow.session, el.ident)
                result = self.__dto__(**res.__dict__)
                assert result == el

            assert await self.__model__.count(uow.session) == len(items)

            await uow.commit()


    async def test_create_existing(self, item: DTO) -> None:

        async with self.uow as uow:

            with pytest.raises(IntegrityError):
                await self.__model__.create(
                    item.__dict__,
                    conn=uow.session
                )

            await uow.commit()


    async def test_get(self, ident: UUID | str, item: DTO) -> None:

        async with self.uow as uow:
            res = await self.__model__.get(uow.session, ident)

            assert self.__dto__(**res.__dict__) == item


    async def test_update(self, ident: UUID | str, data: dict) -> None:
        async with self.uow as uow:

            data_dict = self.__dto__(**data).__dict__

            del data_dict["ident"]

            await self.__model__.update(uow.session, ident, data_dict)

            res = await self.__model__.get(uow.session, ident)

            el = self.__dto__(**res.__dict__)

            for key, value in data_dict.items():
                assert getattr(el, key) == value

            await uow.commit()


    async def test_delete(self, ident: str | UUID, item: DTO) -> None:
        async with self.uow as uow:

            await self.__model__.delete(uow.session, ident)

            assert not await self.__model__.get(uow.session, ident)

            await self.__model__.create(item.__dict__, conn=uow.session)

            await uow.commit()

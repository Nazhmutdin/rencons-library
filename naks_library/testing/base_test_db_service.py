from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from naks_library.base_db_service import BaseDBService
from naks_library.base_shema import BaseShema


class BaseTestDBService[DTO, Model, Shema: BaseShema, CreateShema: BaseShema, UpdateShema: BaseShema]:
    service: BaseDBService[DTO, Model, Shema, CreateShema, UpdateShema]
    session: AsyncSession
    __dto__: DTO
    __create_shema__: type[CreateShema]
    __update_shema__: type[UpdateShema]


    async def test_insert(self, items: list[dict]) -> None:
        data = [self.__create_shema__.model_validate(item, from_attributes=True) for item in items]

        await self.service.insert(self.session, *data)


    async def test_get(self, ident: UUID | str, item: DTO) -> None:

        assert await self.service.get(self.session, ident) == item


    async def test_update(self, ident: str, data_dict: dict) -> None:

        assert await self.service.get(self.session, ident)

        data = self.__dto__(**data_dict)

        data.ident = ident

        update_data = self.__update_shema__.model_validate(data_dict)

        await self.service.update(self.session, ident, update_data)
        assert await self.service.get(self.session, ident) == data


    async def test_delete(self, ident: str | UUID, item: dict) -> None:

        await self.service.delete(self.session, ident)

        assert not bool(await self.service.get(self.session, ident))

        await self.service.insert(self.session, self.__create_shema__.model_validate(item, from_attributes=True))

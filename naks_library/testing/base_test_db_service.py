from uuid import UUID

from naks_library.base_db_service import BaseDBService
from naks_library.base_shema import BaseShema


class BaseTestDBService[DTO, Model, Shema: BaseShema, CreateShema: BaseShema, UpdateShema: BaseShema]:
    service: BaseDBService[DTO, Model, Shema, CreateShema, UpdateShema]
    __dto__: DTO
    __create_shema__: type[CreateShema]
    __update_shema__: type[UpdateShema]


    async def test_add(self, items: list[dict]) -> None:
        data = [self.__create_shema__.model_validate(item, from_attributes=True) for item in items]

        await self.service.add(*data)


    async def test_get(self, ident: UUID | str, item: DTO) -> None:

        assert await self.service.get(ident) == item


    async def test_update(self, ident: str, data: dict) -> None:

        assert await self.service.get(ident)

        data_dict = self.__dto__(**data).__dict__

        del data_dict["ident"]

        update_data = self.__update_shema__.model_validate(data)

        await self.service.update(ident, update_data)
        item = await self.service.get(ident)

        for key, value in data_dict.items():
            assert getattr(item, key) == value


    async def test_delete(self, ident: str | UUID, item: dict) -> None:

        await self.service.delete(ident)

        assert not bool(await self.service.get(ident))

        await self.service.add(self.__create_shema__.model_validate(item, from_attributes=True))

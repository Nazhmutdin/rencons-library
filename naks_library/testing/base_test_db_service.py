from datetime import date, datetime

from naks_library.base_db_service import BaseDBService
from naks_library.funcs import str_to_datetime
from naks_library.base_shema import BaseShema
import pytest


class BaseTestDBService[DTO, Model, Shema: BaseShema, CreateShema: BaseShema, UpdateShema: BaseShema]:
    service: BaseDBService[DTO, Model, Shema, CreateShema, UpdateShema]
    __dto__: DTO
    __create_shema__: type[CreateShema]
    __update_shema__: type[UpdateShema]


    async def test_add(self, items: list[Shema]) -> None:
        data = [self.__create_shema__.model_validate(item, from_attributes=True) for item in items]

        await self.service.add(*data)


    async def test_get(self, attr: str, item: Shema) -> None:

        assert await self.service.get(getattr(item, attr)) == self.__dto__(**item.model_dump())


    async def test_update(self, ident: str, data: dict) -> None:

        assert await self.service.get(ident)

        update_data = self.__update_shema__.model_validate(data)

        await self.service.update(ident, update_data)
        item = await self.service.get(ident)

        for key, value in data.items():
            if isinstance(getattr(item, key), datetime):
                assert getattr(item, key) == str_to_datetime(value)
                continue
            elif isinstance(getattr(item, key), date):
                assert getattr(item, key) == str_to_datetime(value).date()
                continue

            assert getattr(item, key) == value


    async def test_fail_update(self, ident: str, data: dict, exception) -> None:
        with pytest.raises(exception):
            await self.service.update(ident, self.__update_shema__.model_validate(data, from_attributes=True))


    async def test_delete(self, item: Shema) -> None:

        await self.service.delete(item.ident)

        assert not bool(await self.service.get(item.ident))

        await self.service.add(self.__create_shema__.model_validate(item, from_attributes=True))

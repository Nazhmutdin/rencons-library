from sqlalchemy import select, func
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from naks_library.commiter import SqlAlchemyCommitter
from naks_library.crud_mapper import ICrudMapper
from naks_library.testing.fake_data_generator import BaseFakeDataGenerator


_FakeDataGenerator = TypeVar("_FakeDataGenerator", bound=BaseFakeDataGenerator)


class BaseCrudTests:
    session: AsyncSession
    commiter: SqlAlchemyCommitter
    crud_mapper: ICrudMapper
    data_generator: _FakeDataGenerator
    
    test_data: list[dict]


    async def test_insert(self):

        async with self.session:

            for item in self.test_data:
                await self.crud_mapper.insert(item)

            count_stmt = select(func.count()).select_from(self.crud_mapper.__model__)

            assert (await self.session.execute(count_stmt)).scalar_one() == len(self.test_data)

            await self.commiter.commit()
            await self.commiter.rollback()


    async def test_get(self):

        async with self.session:

            for item in self.test_data[:5]:
                res = await self.crud_mapper.get(item["ident"])

                assert res.__dict__ == item
            
            await self.commiter.commit()
            await self.commiter.rollback()


    async def test_update(self):

        async with self.session:

            data = self.test_data[0]
            update_data = self.data_generator.generate(1)[0]

            del update_data['ident']

            updated_data = data | update_data

            await self.crud_mapper.update(data["ident"], update_data)

            assert (await self.crud_mapper.get(data["ident"])).__dict__ == updated_data

            await self.commiter.commit()
            await self.commiter.rollback()


    async def test_delete(self):

        async with self.session:
            for item in self.test_data[:5]:
                await self.crud_mapper.delete(item["ident"])

                assert not (await self.crud_mapper.get(item["ident"]))

            await self.commiter.commit()
            await self.commiter.rollback()

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from utils import ADBService, CreateAShema, UpdateAShema, SelectAShema, AData, test_data, engine


@pytest.mark.asyncio
class TestBaseDBService:
    
    session = AsyncSession(engine)

    a_service = ADBService()


    async def test_insert(self):

        await self.a_service.insert(
            self.session,
            *[CreateAShema.model_validate(el, from_attributes=True) for el in test_data.fake_a]
        )

        assert len(await self.a_service.get_many(self.session, SelectAShema())) == len(test_data.fake_a)


    async def test_get(self):
        ident = test_data.get_random_a_ident()

        assert (await self.a_service.get(self.session, ident)) == test_data.get_a_by_ident(ident)


    async def test_update(self): 
        ident = test_data.get_random_a_ident()
        update_data = test_data.fake_a_generator.generate(1)[0]

        update_data["ident"] = ident

        updated = AData(**update_data)

        await self.a_service.update(
            self.session, 
            ident, 
            UpdateAShema.model_validate(
                update_data
            )
        )

        assert (await self.a_service.get(self.session, ident)) == updated


    async def test_delete(self):
        ident = test_data.get_random_a_ident()

        await self.a_service.delete(self.session, ident)

        assert not (await self.a_service.get(self.session, ident))

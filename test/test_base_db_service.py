import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from utils import ADBService, BDBService, CreateAShema, CreateBShema, UpdateAShema, UpdateBShema, SelectAShema, SelectBShema, AData, BData, test_data, engine


@pytest.mark.asyncio
class TestBaseDBService:
    
    session = AsyncSession(engine)

    a_service = ADBService()
    b_service = BDBService()


    async def test_insert(self):

        await self.a_service.insert(
            self.session,
            *[CreateAShema.model_validate(el, from_attributes=True) for el in test_data.fake_a]
        )

        await self.b_service.insert(
            self.session,
            *[CreateBShema.model_validate(el, from_attributes=True) for el in test_data.fake_b]
        )

        assert len(await self.a_service.get_many(self.session, SelectAShema())) == len(test_data.fake_a)
        assert len(await self.b_service.get_many(self.session, SelectBShema())) == len(test_data.fake_b)


    async def test_get(self):
        ident = test_data.get_random_a_ident()

        assert (await self.a_service.get(self.session, ident)) == test_data.get_a_by_ident(ident)

        ident = test_data.get_random_b_ident()

        assert (await self.b_service.get(self.session, ident)) == test_data.get_b_by_ident(ident)


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

        
        ident = test_data.get_random_b_ident()
        update_data = test_data.fake_b_generator.generate(1)[0]

        update_data["ident"] = ident

        updated = BData(**update_data)

        await self.b_service.update(
            self.session, 
            ident, 
            UpdateBShema.model_validate(
                update_data
            )
        )

        assert (await self.b_service.get(self.session, ident)) == updated


    async def test_delete(self):
        ident = test_data.get_random_a_ident()

        await self.a_service.delete(self.session, ident)

        assert not (await self.a_service.get(self.session, ident))

        ident = test_data.get_random_b_ident()

        await self.b_service.delete(self.session, ident)

        assert not (await self.b_service.get(self.session, ident))

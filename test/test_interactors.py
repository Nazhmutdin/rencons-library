from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from naks_library.commiter import SqlAlchemyCommitter
from utils import GetAInteractor, CreateAInteractor, UpdateAInteractor, DeleteAInteractor, ACrudMapper, AData, UpdateADTO, engine, test_data


def get_mapper_commiter() -> tuple[AsyncSession, SqlAlchemyCommitter, ACrudMapper]:
    session = AsyncSession(engine)
    commiter = SqlAlchemyCommitter(session)

    crud_mapper = ACrudMapper(session)

    return session, commiter, crud_mapper


@pytest.mark.asyncio
class TestInteractors:

    async def test_create_interactor(self): 
        session, commiter, mapper = get_mapper_commiter()

        create_a = CreateAInteractor(mapper, commiter)

        for data in test_data.fake_a:
            await create_a(data)


    async def test_update_interactor(self): 
        session, commiter, mapper = get_mapper_commiter()

        get_a = GetAInteractor(mapper, commiter)
        update_a = UpdateAInteractor(mapper, commiter)

        data = test_data.get_random_a()
        update_data = test_data.fake_a_generator.generate(1)[0]

        del update_data['ident']

        updated_data = data.__dict__ | update_data

        await update_a(data.ident, UpdateADTO(**update_data))

        assert (await get_a(data.ident)) == AData(**updated_data)

        await session.close()


    async def test_get_interactor(self): 
        session, commiter, mapper = get_mapper_commiter()

        get_a = GetAInteractor(mapper, commiter)

        data = test_data.get_random_a()

        assert (await get_a(data.ident)) == data

        await session.close()


    async def test_delete_interactor(self): 
        session, commiter, mapper = get_mapper_commiter()

        delete_a = DeleteAInteractor(mapper, commiter)
        get_a = GetAInteractor(mapper, commiter)

        data = test_data.get_random_a()

        await delete_a(data.ident)
        assert not (await get_a(data.ident))

        await session.close()

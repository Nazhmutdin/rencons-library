from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from naks_library.committer import SqlAlchemyCommitter
from utils import GetAInteractor, CreateAInteractor, UpdateAInteractor, DeleteAInteractor, ACrudMapper, AData, UpdateADTO, engine, test_data


def get_mapper_committer() -> tuple[AsyncSession, SqlAlchemyCommitter, ACrudMapper]:
    session = AsyncSession(engine)
    committer = SqlAlchemyCommitter(session)

    crud_mapper = ACrudMapper(session)

    return session, committer, crud_mapper


@pytest.mark.asyncio
class TestInteractors:

    async def test_create_interactor(self): 
        session, committer, mapper = get_mapper_committer()

        create_a = CreateAInteractor(mapper, committer)

        for data in test_data.fake_a:
            await create_a(data)


    async def test_update_interactor(self): 
        session, committer, mapper = get_mapper_committer()

        get_a = GetAInteractor(mapper)
        update_a = UpdateAInteractor(mapper, committer)

        data = test_data.get_random_a()
        update_data = test_data.fake_a_generator.generate(1)[0]

        del update_data['ident']

        updated_data = data.__dict__ | update_data

        await update_a(data.ident, UpdateADTO(**update_data).__dict__)

        assert (await get_a(data.ident)) == AData(**updated_data)

        await session.close()


    async def test_get_interactor(self): 
        session, committer, mapper = get_mapper_committer()

        get_a = GetAInteractor(mapper)

        data = test_data.get_random_a()

        assert (await get_a(data.ident)) == data

        await session.close()


    async def test_delete_interactor(self): 
        session, committer, mapper = get_mapper_committer()

        delete_a = DeleteAInteractor(mapper, committer)
        get_a = GetAInteractor(mapper)

        data = test_data.get_random_a()

        await delete_a(data.ident)
        assert not (await get_a(data.ident))

        await session.close()

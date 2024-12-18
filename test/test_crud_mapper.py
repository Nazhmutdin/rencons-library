from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from naks_library.committer import SqlAlchemyCommitter
from utils import ACrudMapper, CreateADTO, UpdateADTO, AData, engine, test_data


def get_mapper_commiter() -> tuple[AsyncSession, SqlAlchemyCommitter, ACrudMapper]:
    session = AsyncSession(engine)
    commiter = SqlAlchemyCommitter(session)

    crud_mapper = ACrudMapper(session)

    return session, commiter, crud_mapper


@pytest.mark.asyncio
class TestSqlAlchemyCrudMapper:

    async def test_insert(self):
        session, commiter, crud_mapper = get_mapper_commiter()

        for data in test_data.fake_a:
            await crud_mapper.insert(CreateADTO(**data.__dict__))

        await commiter.commit()
        await session.close()

    
    async def test_get(self):
        session, commiter, crud_mapper = get_mapper_commiter()

        data = test_data.get_random_a()

        ident = data.ident

        assert (await crud_mapper.get(ident)) == data

        await session.close()


    async def test_update(self): 
        session, commiter, crud_mapper = get_mapper_commiter()

        data = test_data.get_random_a()
        update_data = test_data.fake_a_generator.generate(1)[0]

        del update_data['ident']

        updated_data = data.__dict__ | update_data

        await crud_mapper.update(data.ident, UpdateADTO(**update_data))

        assert (await crud_mapper.get(data.ident)) == AData(**updated_data)

        await commiter.commit()
        await session.close()
    

    async def test_delete(self):
        session, commiter, crud_mapper = get_mapper_commiter()

        data = test_data.get_random_a()

        ident = data.ident

        await crud_mapper.delete(ident)

        assert not (await crud_mapper.get(ident))

        await session.close()

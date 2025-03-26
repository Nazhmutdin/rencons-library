from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from rencons_library.committer import SqlAlchemyCommitter
from utils import ACrudMapper, UpdateADTO, AData, test_data


def get_mapper_committer(session: AsyncSession) -> tuple[AsyncSession, SqlAlchemyCommitter, ACrudMapper]:
    committer = SqlAlchemyCommitter(session)

    crud_mapper = ACrudMapper(session)

    return session, committer, crud_mapper


class TestSqlAlchemyCrudMapper:
    @pytest.mark.anyio
    async def test_insert(self, session: AsyncSession):
        session, committer, crud_mapper = get_mapper_committer(session)

        for data in test_data.fake_a:
            await crud_mapper.insert(data.__dict__)

        await committer.commit()
        await session.close()


    @pytest.mark.anyio
    async def test_get(self, session: AsyncSession):
        session, committer, crud_mapper = get_mapper_committer(session)

        data = test_data.get_random_a()

        ident = data.ident

        assert (await crud_mapper.get(ident)) == data

        await session.close()


    @pytest.mark.anyio
    async def test_update(self, session: AsyncSession): 
        session, committer, crud_mapper = get_mapper_committer(session)

        data = test_data.get_random_a()
        update_data = test_data.fake_a_generator.generate(1)[0]

        del update_data['ident']

        updated_data = data.__dict__ | update_data

        await crud_mapper.update(data.ident, UpdateADTO(**update_data).__dict__)

        assert (await crud_mapper.get(data.ident)) == AData(**updated_data)

        await committer.commit()
        await session.close()
    

    @pytest.mark.anyio
    async def test_delete(self, session: AsyncSession):
        session, committer, crud_mapper = get_mapper_committer(session)

        data = test_data.get_random_a()

        ident = data.ident

        await crud_mapper.delete(ident)

        assert not (await crud_mapper.get(ident))

        await session.close()

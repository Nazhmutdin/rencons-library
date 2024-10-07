from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from naks_library.testing.base_crud_tests import BaseCrudTests
from naks_library.commiter import SqlAlchemyCommitter
from utils import ACrudMapper, engine, test_data


def get_mapper_commiter() -> tuple[AsyncSession, ACrudMapper, SqlAlchemyCommitter]:
    session = AsyncSession(engine)
    commiter = SqlAlchemyCommitter(session)

    crud_mapper = ACrudMapper(session)

    return session, commiter, crud_mapper


@pytest.mark.asyncio
class TestCrudMapper(BaseCrudTests):
    session, commiter, crud_mapper = get_mapper_commiter()

    data_generator = test_data.fake_a_generator

    test_data = test_data.fake_a_dicts

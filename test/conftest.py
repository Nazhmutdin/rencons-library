import os

import pytest

from utils import ADict, BDict, AData, BData, Base, test_data, engine
from asyncio import run


@pytest.fixture(scope="module", autouse=True)
def prepare_db():
    assert os.getenv("DATABASE_NAME") == "test_db"

    async def start_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    run(start_db())


@pytest.fixture
def fake_a_dicts() -> list[ADict]:
    return test_data.fake_a_dicts


@pytest.fixture
def fake_a() -> list[AData]:
    return test_data.fake_a


@pytest.fixture
def fake_b_dicts() -> list[BDict]:
    return test_data.fake_b_dicts


@pytest.fixture
def fake_b() -> list[BData]:
    return test_data.fake_b

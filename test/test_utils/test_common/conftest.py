import pytest

from rencons_library.common.get_many_stmt_creator import StandartSqlAlchemyGetManyStmtCreator
from utils import A_FILTERS_MAP, A_SELECT_ATTRS, A_SELECT_FROM_ATTRS


@pytest.fixture()
def a_stmt_creator():
    return StandartSqlAlchemyGetManyStmtCreator(
        filters_map=A_FILTERS_MAP,
        select_attrs=A_SELECT_ATTRS,
        select_from_attrs=A_SELECT_FROM_ATTRS
    )
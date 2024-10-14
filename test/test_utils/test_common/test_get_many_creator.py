from uuid import UUID
from datetime import date

import pytest
from sqlalchemy import select

from naks_library.common.get_many_stmt_creator import StandartSqlAlchemyGetManyStmtCreator
from utils import AModel, BModel, A_SELECT_FROM_ATTRS, A_SELECT_ATTRS


@pytest.mark.parametrize(
    "filters, stmt",
    [
        (
            {
                "idents": [UUID("5a5c0cff0ac94ac0bd081d5dea9bae3f")],
                "foo1_from": 1,
                "b_foo3_before": date(2000, 1, 1)
            },
            select(*A_SELECT_ATTRS).distinct().select_from(*A_SELECT_FROM_ATTRS).where(
                AModel.ident.in_([UUID("5a5c0cff0ac94ac0bd081d5dea9bae3f")]),
                AModel.foo1 > 1,
                BModel.foo3 < date(2000, 1, 1)
            )
        )
    ]
)
def test_create(filters, stmt, a_stmt_creator: StandartSqlAlchemyGetManyStmtCreator):
    new_stmt = a_stmt_creator(filters)

    assert new_stmt.compare(stmt)

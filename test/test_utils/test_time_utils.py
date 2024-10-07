from datetime import datetime, date

import pytest

from naks_library.utils.time_utils import *


@pytest.mark.parametrize(
    "datetime_string, result",
    [
        ("01.01.2000T14:31:15", datetime(2000, 1, 1, 14, 31, 15)),
        ("17.01.2034 11:31:15", datetime(2034, 1, 17, 11, 31, 15)),
        ("1caewe15", None)
    ]
)
def test_str_to_datetime(datetime_string: str, result: datetime):
    _datetime = str_to_datetime(datetime_string)

    assert _datetime == result


@pytest.mark.parametrize(
    "datetime_string, result",
    [
        ("01.01.2000T14:31:15", datetime(2000, 1, 1, 14, 31, 15)),
        ("17.01.2034 11:31:15", datetime(2034, 1, 17, 11, 31, 15))
    ]
)
def test_to_datetime(datetime_string: str, result: datetime):
    _datetime = to_datetime(datetime_string)

    assert _datetime == result


@pytest.mark.parametrize(
    "datetime_string",
    [
        "hdvweed",
        None
    ]
)
def test_faild_to_datetime(datetime_string: str):
    with pytest.raises(ValueError):
        to_datetime(datetime_string)


@pytest.mark.parametrize(
    "datetime_string, result",
    [
        ("01.01.2000T14:31:15", date(2000, 1, 1)),
        ("17.01.2034", date(2034, 1, 17))
    ]
)
def test_to_date(datetime_string: str, result: date):
    _datetime = to_date(datetime_string)

    assert _datetime == result


@pytest.mark.parametrize(
    "datetime_string",
    [
        "hdvweed",
        None
    ]
)
def test_faild_to_date(datetime_string: str):
    with pytest.raises(ValueError):
        to_date(datetime_string)

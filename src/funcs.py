import typing as t
from uuid import UUID

from datetime import datetime, date
from dateutil.parser import parser


__all__ = [
    "to_uuid",
    "str_to_datetime",
    "to_date"
]


def to_uuid(v: str | UUID) -> UUID:
    if isinstance(v, UUID):
        return v
    
    return UUID(v)


def str_to_datetime(date_string, dayfirst: bool = False) -> datetime | None:
    try:
        return parser().parse(date_string, dayfirst=dayfirst)
    except:
        return None


def to_date(date_data: str | date | datetime | t.Iterable[int] | None, dayfirst: bool = False) -> date:
    if not date_data:
        raise ValueError(f"NoneType cannot be converted to date'")
    
    if isinstance(date_data, date):
        return date_data
    
    if isinstance(date_data, datetime):
        return date_data.date()
    
    if isinstance(date_data, str):
        _datetime = str_to_datetime(date_data, dayfirst)

        if not _datetime:
            raise ValueError(f"Invalid date data '{date_data}'")

        return _datetime.date()
    
    if isinstance(date_data, t.Iterable) and len(date_data) == 3:
        return date(*date_data)
    
    raise ValueError(f"Invalid date data '{date_data}'")

import typing as t
from uuid import UUID
from re import fullmatch

from datetime import datetime, date
from dateutil.parser import parser


__all__ = [
    "to_uuid",
    "str_to_datetime",
    "to_date",
    "is_float",
    "is_kleymo",
    "is_uuid",
    "to_datetime"
]


def is_float(v: str) -> bool:
    try:
        float(v)
        return True
    except:
        return False


def is_kleymo(v: str) -> bool:
    if fullmatch(r"[A-Z0-9]{4}", v):
        return True
    
    return False


def is_uuid(uuid: str | UUID) -> True:
    try:
        UUID(uuid)
        return True
    except:
        return False


def to_uuid(v: str | UUID) -> UUID:
    if isinstance(v, UUID):
        return v
    
    return UUID(v)


def str_to_datetime(date_string, dayfirst: bool = False) -> datetime | None:
    try:
        return parser().parse(date_string, dayfirst=dayfirst)
    except:
        return None
    

def to_datetime(datetime_data: str | datetime | t.Iterable[int] | None, dayfirst: bool = False) -> datetime:
    if not datetime_data:
        raise ValueError(f"NoneType cannot be converted to datetime'")
    
    if isinstance(datetime_data, datetime):
        return datetime_data
    
    if isinstance(datetime_data, str):
        _datetime = str_to_datetime(datetime_data, dayfirst)

        if not _datetime:
            raise ValueError(f"Invalid datetime data '{datetime_data}'")

        return _datetime
    
    if isinstance(datetime_data, t.Iterable) and 3 < len(datetime_data) < 7:
        return datetime(*datetime_data)
    
    raise ValueError(f"Invalid datetime data '{datetime_data}'")


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

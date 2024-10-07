from datetime import datetime, date

from dateutil.parser import parser


__all__ = [
    "str_to_datetime",
    "to_datetime",
    "to_date"
]


def str_to_datetime(datetime_string, dayfirst: bool = True) -> datetime | None:
    try:
        return parser().parse(datetime_string, dayfirst=dayfirst)
    except:
        return None
    

def to_datetime(datetime_data: str | datetime | None, dayfirst: bool = True) -> datetime:
    if not datetime_data:
        raise ValueError(f"NoneType cannot be converted to date/datetime'")
    
    if isinstance(datetime_data, datetime):
        return datetime_data
    
    if isinstance(datetime_data, date):
        return datetime.fromordinal(datetime_data.toordinal())
    
    if isinstance(datetime_data, str):
        _datetime = str_to_datetime(datetime_data, dayfirst)

        if _datetime:
            return _datetime
    
    raise ValueError(f"Invalid date/datetime data '{datetime_data}'")


def to_date(date_data: str | date | datetime | None, dayfirst: bool = True) -> date:
    
    _datetime = to_datetime(date_data, dayfirst)

    return _datetime.date()

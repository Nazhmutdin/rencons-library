from datetime import date, datetime
from uuid import UUID

from pydantic import BeforeValidator, PlainSerializer

from naks_library.funcs import to_date, to_datetime, to_uuid
from naks_library.utils import DATE_STRING_FORMAT, DATETIME_STRING_FORMAT


__all__ = [
    "before_date_validator",
    "before_optional_date_validator",
    "plain_date_serializer",
    "plain_optional_date_serializer",
    "before_datetime_validator",
    "before_optional_datetime_validator",
    "plain_datetime_serializer",
    "plain_optional_datetime_serializer",
    "before_uuid_validator",
    "before_optional_uuid_validator",
    "plain_uuid_serializer",
    "plain_optional_uuid_serializer"
]


def _date_validator_func(v) -> date:
    return to_date(v)


def _optional_date_validator_func(v) -> date | None:
    try:
        return to_date(v)
    except:
        return None


def _datetime_validator_func(v) -> date:
    return to_datetime(v)


def _optional_datetime_validator_func(v) -> date | None:
    try:
        return to_datetime(v)
    except:
        return None


def _uuid_validator_func(v) -> UUID:
    try:
        return to_uuid(v)
    except:
        return None


def _optional_uuid_validator_func(v) -> UUID | None:
    try:
        return to_uuid(v)
    except:
        return None


before_date_validator = BeforeValidator(_date_validator_func)
before_optional_date_validator = BeforeValidator(_optional_date_validator_func)

plain_date_serializer = PlainSerializer(lambda v: date.strftime(v, DATE_STRING_FORMAT), when_used="json")
plain_optional_date_serializer = PlainSerializer(lambda v: date.strftime(v, DATE_STRING_FORMAT) if v is not None else None, when_used="json")

before_datetime_validator = BeforeValidator(_datetime_validator_func)
before_optional_datetime_validator = BeforeValidator(_optional_datetime_validator_func)

plain_datetime_serializer = PlainSerializer(lambda v: datetime.strftime(v, DATETIME_STRING_FORMAT), when_used="json")
plain_optional_datetime_serializer = PlainSerializer(lambda v: datetime.strftime(v, DATETIME_STRING_FORMAT) if v is not None else None, when_used="json")

before_uuid_validator = BeforeValidator(_uuid_validator_func)
before_optional_uuid_validator = BeforeValidator(_optional_uuid_validator_func)

plain_uuid_serializer = PlainSerializer(lambda v: str(v), when_used="json")
plain_optional_uuid_serializer = PlainSerializer(lambda v: str(v) if v is not None else None, when_used="json")
